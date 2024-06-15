import relationalai as rai
from relationalai.clients.snowflake import Snowflake, PrimaryKey
from relationalai.std import aggregates
from relationalai.std.graphs import Graph

# Get the model for the "power_transmission_network" schema.
model = rai.Model("power_transmission_network")

# Get the 'Snowflake' object for the model.
# You'll use this to access objects imported from the model's schema.
sf = Snowflake(model)

# Assign objects from the 'nodes' table to the 'NetworkNode' type
# and objects from the 'powerlines' table to the 'PowerLine' type.
# Tables are accessed as attributes of the 'sf' object via the
# pattern 'sf.<database_name>.<schema_name>.<table_name>'. Names
# are case-insensitive.
NetworkNode = sf.rai_getting_started.power_transmission_network.nodes
PowerLine = sf.rai_getting_started.power_transmission_network.powerlines

NetworkNode.describe(id=PrimaryKey)
PowerLine.describe(
    source_node_id=(NetworkNode, "source"),
    target_node_id=(NetworkNode, "target"),
)

# Define a type for nodes that need repair.
NeedsRepair = model.Type("NeedsRepair")

# Assign nodes with status "fail" to the NeedsRepair type.
with model.rule():
    node = NetworkNode()
    node.status == "fail"
    node.set(NeedsRepair)

# Loads critical to public safety and security are given higher priority.
with model.rule():
    node = NeedsRepair(type="load")
    with model.match():
        # Nodes with a description of "hospital", "military", or
        # "government" are given the highest priority.
        with node.description.in_(["hospital", "military", "government"]):
            node.set(load_priority=2)
        # "Load" nodes with other descriptions are given a lower priority.
        with model.case():
            node.set(load_priority=1)

# Get a new graph object. By default graphs are directed.
graph = Graph(model)

# Add 'NeedsRepair' nodes to the `graph.Node` type.
with model.rule():
    repair_node = NeedsRepair()
    graph.Node.add(repair_node)

# Add edges between `NeedsRepair` nodes that are connected by a 'PowerLine'.
with model.rule():
    line = PowerLine()
    graph.Edge.add(from_=NeedsRepair(line.source), to=NeedsRepair(line.target))

# Nodes upstream of critical loads are given higher priority,
# as are nodes with more downstream connections.
with model.rule():
    upstream, downstream = NeedsRepair(), NeedsRepair()
    graph.compute.is_reachable(upstream, downstream)
    upstream.set(
        load_priority=aggregates.max(downstream.load_priority.or_(0), per=[upstream]),
        connection_priority=aggregates.count(downstream, per=[upstream])
    )

# Prioritize nodes by ranking them in descendeing order first by load priority,
# then by connection priority, and finally by the node ID to break ties.
with model.rule():
    node = NeedsRepair()
    node.set(priority=aggregates.rank_desc(
        node.load_priority.or_(0),
        node.connection_priority.or_(0),
        node.id
    ))

# Query the model for the repair priority of each node.
with model.query() as select:
    node = NeedsRepair()
    node.priority <= 10  # Limit the results to the top 10 nodes.
    response = select(node.priority, node.id, node.type, node.description.or_(""))

print(response.results)
#     priority         type  description
# 0          1  transformer
# 1          2  transformer
# 2          3  transformer
# 3          4  transformer
# 4          5         load     hospital
# 5          6  transformer
# 6          7         load   commercial
# 7          8         load  residential
# 8          9  transformer
# 9         10  transformer

# Pass properties of 'NeedsRepair' objects to the graph so they can be
# displayed in the visualization.
with model.rule():
    repair = NeedsRepair()
    # Get the graph's 'Node' object for each 'NeedsRepair' object and
    # set the properties that will be displayed in the visualization.
    graph.Node(repair).set(
        id=repair.id,
        type=repair.type,
        description=repair.description,
        priority=repair.priority,
    )

# Visualie the graph. The 'visualize()' method accepts a style dictionary
# that lets you customize the appearance of nodes and edges in the graph.
graph.visualize(
    style={
        "node": {
            # Color load nodes red and all other nodes black.
            "color": lambda n: {"load": "red"}.get(n["type"], "black"),
            # Label nodes by their priority.
            "label": lambda n: n["priority"],
            # Include additional information when hovering over a node.
            "hover": lambda n: f"ID: {n['id']}\nType: {n['type']}\nDescription: {n.get('description', 'none')}",
        },
    },
).display()  # In Jupyter notebooks, .display() is not required.

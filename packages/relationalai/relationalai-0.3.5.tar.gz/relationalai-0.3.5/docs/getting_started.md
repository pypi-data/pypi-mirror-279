# Getting Started with RelationalAI

RelationalAI (RAI) augments your Snowflake data cloud with a powerful toolkit for turning data into decisions.

At RAI's core is a **model**: an executable knowledge graph that captures the
rules and logic that govern your organization's decision-making processes.
Models are written using the `relationalai` Python package
and run securely in your Snowflake account on Snowpark Container Services.

## Install the `relationalai` Python Package

RelationalAI requires Python 3.10 or later.
Use `pip` or your favorite Python package manager to install the `relationalai` package:

```sh
# Create a virtual environment. For example, using venv:
python -m venv .venv
# Activate the virtual environment. On Linux and macOS:
source .venv/bin/activate
# Or, on Windows:
.venv\Scripts\activate

pip install relationalai
```

Before you can use `relationalai`, your Snowflake account administrator must:

1. Install the RelationalAI Native App from the Snowflake Marketplace.
2. Grant your user access to a Snowflake role with the privileges required to
   import data from Snowflake into a RelationalAI model.

See [Administration](TODO) for details.

## Load Data into Snowflake

In this guide, you'll explore a scenario in which an electrical utility company
must prioritize repairs to its power grid after a storm.
The dataset consists of two CSV files: [`nodes.csv`](TODO) and [`powerlines.csv`](TODO).

1. Download the dataset using the following commands (TODO: Replace URLS):
   ```sh
   curl -O https://raw.githubusercontent.com/relationalai/relationalai-python/main/docs/nodes.csv
   curl -O https://raw.githubusercontent.com/relationalai/relationalai-python/main/docs/powerlines.csv
   ```
2. Create or use an existing database and schema to store the data for the model.
   In this guide, we use a database named `rai_getting_started` and a schema named `power_transmission_network`.
3. Then, [load the data](https://docs.snowflake.com/en/user-guide/data-load-web-ui)
   from the `nodes.csv` and `powerlines.csv` files into tables named `node` and `powerlines`.

RelationalAI models are built on top of Snowflake schemas.
In the next step, you'll initialize a RelationalAI model for the `power_transmission_network` schema.

## Create a RelationalAI Model

Bundled with the `relationalai` package is a command-line interface (CLI) that
you can use to perform various tasks, such as configuring a new model, managing imports, and more.
Access the CLI by running `rai` in your terminal.

### Configure Your Model

Run `rai init` to connect to your Snowflake account and select the database and schema containing the data for the model:

```sh
rai init
```

Follow the interactive prompts to enter your Snowflake credentials, as well as the:

- Snowflake role and warehouse to use.
  You must use a role with the necessary privileges to
  import data into RAI from the schema selected in the next step.
- Snowflake database and schema that contains the `nodes` and `powerlines` tables.
  The name of the schema is used as the name of the model.
- RelationalAI compute engine to use with the model.
  Select `[CREATE NEW ENGINE]` if none exist.
  You're prompted to give the engine a name and select its size and compute pool.
  (TODO: Size? Compute pool?)

> **Important:**
> `rai init` saves your model's configuration to a file named `raiconfig.toml` in the current directory.
> This file contains sensitive information, so be sure to exclude it from version control!

### Import Data into Your Model

Next, import your data using the `rai imports:stream` CLI command:

```sh
rai imports:stream --source rai_getting_started.power_transmission_network.nodes --model power_transmission_network
rai imports:stream --source rai_getting_started.power_transmission_network.powerlines --model power_transmission_network
```

Data from the `nodes` and `powerlines` tables are loaded into the
`power_transmission_network` model and refreshed once every minute.
It may take a few minutes for the data to become available in the model.
Use `rai imports:list` to check the status of the imports:

```sh
rai imports:list --model power_transmission_network
```

When both imports report the status `LOADED`, the data is ready for use in the model.

### Define Your Model in Python

In your favorite Python editor, create a new Python script named `repair_priority.py` and add the following code:

```python
# repair_priority.py

import relationalai as rai
from relationalai.clients.snowflake import Snowflake, PrimaryKey

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
```

Models are made up of three main components:

1. **Objects** represent entities in the model.
   The `power_transmission_network` model has two kinds of objects:
   nodes, which represent things like transformers and substations, and
   power lines, which represent the connections between nodes.
2. **Types** are collections of objects.
   `NetworkNode` is a type containing all the node objects,
   and `PowerLine` is a type containing all the power line objects.
   Objects may have multiple types.
   In a bit, you'll add a third type for `NetworkNode` objects that need repair.
3. **Rules** define the logic that governs the model.
   In the next section, you'll write some rules to determine the repair priority
   of nodes that have been damaged in a storm.

Objects have properties.
For objects imported from Snowflake, properties are derived from the columns in the corresponding table.
For instance, `NetworkNode` and `PowerLine` objects have the following properties:

<!-- markdownlint-disable MD033 -->

<table>
    <thead>
        <tr>
            <th colspan="2">NetworkNode</th>
            <th colspan="2">PowerLine</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>id</strong></td>
            <td>The unique numeric identifier of the node.</td>
            <td><strong>source_node_id</strong></td>
            <td>The ID of the node on the transmitting side of the line.</td>
        </tr>
        <tr>
            <td><strong>type</strong></td>
            <td>The type of the node (e.g., "substation" or "transformer").</td>
            <td><strong>target_node_id</strong></td>
            <td>The ID of the node on the receiving side of the line.</td>
        </tr>
        <tr>
            <td><strong>description</strong></td>
            <td>A description of the node (e.g., "hospital", "commercial", "residential").</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><strong>status</strong></td>
            <td>The status of the node (e.g., "ok" or "fail").</td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
</table>

<!-- markdownlint-enable MD033 -->

`PowerLine.source_node_id` and `.target_node_id` are foreign keys that reference the `NetworkNode.id` property.
But often, it's more convenient to reference the source and target `NetworkNode` objects directly.
Use the `.describe()` method to set `NetworkNode.id` as the primary key and
define new properties named `source` and `target` that reference
the source and target node _objects_ that the IDs refer to:

```python
NetworkNode.describe(id=PrimaryKey)
PowerLine.describe(
    source_node_id=(NetworkNode, "source"),
    target_node_id=(NetworkNode, "target"),
)
```

In this case, you must specify the primary key for the `NetworkNode` type
because the `nodes` table has no `PRIMARY KEY` constraint in Snowflake.
If a table has primary keys, RAI automatically detects them from the table schema.

Next, use `model.Type()` to define a type for nodes that need repair:

```python
NeedsRepair = model.Type("NeedsRepair")
```

`NeedsRepair` exists only in the model and is not associated with any Snowflake table.
It's also empty!
Let's populate it and determine the repair priority of each node.

## Add Rules to Your Model

Rules are written using the RAI query-builder syntax, which lets you describe rules as
a sort of pipeline that objects pass through when the model is executed.

In our scenario, some of the power grid nodes have been damaged in a storm and need repair.
Add the following rule to your Python file to assign nodes with a status of `"fail"` to the `NeedsRepair` type:

```python
with model.rule():
    node = NetworkNode()
    node.status == "fail"
    node.set(NeedsRepair)
```

Rules do not run immediately.
The `model.rule()` [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers)
translates query-builder code in the `with` block into a query plan, which the system executes when you query the model.
As the model executes, objects flow through the rule:

- `NetworkNode()` produces objects of type `NetworkNode`.
- `node.status == "fail"` filters out objects with a status other than `"fail"`.
- `node.set(NeedsRepair)` assigns the filtered objects to the `NeedsRepair` type.

The primary purpose of rules is to capture knowledge for decision-making.

In our dataset, nodes have a `description` property that indicates the type of load attached to the node.
Some nodes in the power grid are more critical than others.
For example, nodes that supply power to critical infrastructure need to be repaired first.

The next rule prioritizes nodes based on their `description` property:

```python
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
```

Here's how objects flow through this rule:

- `NeedsRepair(type="load")` produces `NeedsRepair` objects with a `type` property set to `"load"`.
- `with model.match()` acts like a Python `match` or a SQL `CASE` statement.
  Objects flow through the first `with` block that filters them:
  - The first matches `"hospital"`, `"military"`, and `"government"` objects
    and sets their `load_priority` to `2`.
  - The second block catches all objects not filtered by the first.
    These are loads connected to commercial or residential buildings, which are given a lower priority of `1`.

You might wonder: "Why not use a simple `if` statement?"

You can't use `if` in a rule because objects and their property values aren't known at your Python program's runtime.
Instead, they are determined at query execution time.
This principle extends to other Python constructs, like `in`, which are substituted by RAI query-builder methods,
such as `node.description.in_()` for checking if a node's description is in a list of values.

The underlying structure of a model is a graph.
Entities in the model are the nodes, and properties that connect entities are the edges.
You can tap into this structure, or create entirely new graphs, to power your rules with more advanced logic.
For example, we can use the graph structure of the power grid in our scenario to prioritize nodes
that are upstream of critical loads or have more downstream connections.

Let's build a graph from `NeedsRepair` nodes and the power lines that connect them:

```python
from relationalai.std.graphs import Graph

# Get a new graph object. By default graphs are directed.
graph = Graph(model)

# Add 'NeedsRepair' nodes to the `graph.Node` type.
with model.rule():
    repair_node = NeedsRepair()
    graph.Node.add(repair_node)

# Add edges between `NeedsRepair` nodes that are connected by a 'PowerLine'.
with model.rule():
    line = PowerLine()
    # `NeedsRepair(line.source)` and `NeedsRepair(line.target)` filter
    # `PowerLine` objects, only adding edges where both endpoints need repair.
    graph.Edge.add(from_=NeedsRepair(line.source), to=NeedsRepair(line.target))
```

Next, add a rule that increases the `load_prority` property of nodes that are upstream of critical loads,
and sets the `connection_priority` property to the number of downstream connections:

```python
from relationalai.std import aggregates

with model.rule():
    upstream, downstream = NeedsRepair(), NeedsRepair()
    graph.compute.is_reachable(upstream, downstream)
    upstream.set(
        load_priority=aggregates.max(downstream.load_priority.or_(0), per=[upstream]),
        connection_priority=aggregates.count(downstream, per=[upstream])
    )
```

In this rule:

- `NeedsRepair(), NeedsRepair()` produces pairs of `NeedsRepair` objects.
  All possible pairs of objects flow through the rule.
- `graph.compute.is_reachable()` filters pairs where `upstream` is connected
  by a path of power lines to `downstream`.
- `aggregates.max()` finds the maximum `load_priority` of all objects downstream
  of `upstream`, which is set as the `load_priority` property of the node.
  `.or_(0)` provides a default value of `0` for objects without a `load_priority` property.
- `aggregates.count()` counts the number of downstream connections for each
  `upstream` object, which is set as the `connection_priority` property of the node.

Finally, combine the `load_priority` and `connection_priority` properties to create a single `priority` property:

```python

# Prioritize nodes by ranking them in descendeing order first by load priority,
# then by connection priority, and finally by the node's ID to break ties.
with model.rule():
    node = NeedsRepair()
    node.set(priority=aggregates.rank_desc(
        node.load_priority.or_(0),
        node.connection_priority.or_(0),
        node.id
    ))
```

The `aggregates.rank_desc()` method assigns a rank to each `NeedsRepair` node
based on the values of the `load_priority` and `connection_priority` properties.
Nodes are ranked in descending order first by `load_priority`,
then by `connection_priority`, and finally by the node's `id` to break ties.

## Query Your Model

Let's take a look and see how well our model is prioritizing nodes for repair.
Use the `model.query()` context manager to query the model:

```python
with model.query() as select:
    node = NeedsRepair()
    node.priority <= 10  # Limit the results to the top 10 nodes.
    response = select(node.priority, node.id, node.type, node.description.or_(""))
```

In this query:

- `model.query() as select` creates a new query context and assigns it to the `select` variable.
  `select` chooses which objects and properties to include in the query results,
  and is called at the end of the query.
- `NeedsRepair()` produces all `NeedsRepair` objects.
- `select()` picks the `priority`, `id`, `type`, and `description` properties
  to be returned in the results.
  The `.or_()` method provides a default value of `""` for objects with no `description` value.
- `response` contains the query results as a pandas DataFrame assigned to its `.results` attribute.

Here are the results:

```python
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
```

The top load node is a hospital, which makes sense given that we said
nodes supplying critical infrastructure should be repaired first.
You can get a better sense for how the nodes are prioritized by visualizing the graph:

```python
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

# Visualize the graph. The 'visualize()' method accepts a style dictionary
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
```

The `.visualize()` method generates an interactive graph visualization of the model.
When called in a Jupyter notebook, the visualization is displayed inline.
In other environments, use `.display()` to open the visualization in a new browser window.

Trace the path through the power lines from the top priority node to the least,
and hover over nodes to see their type and descriptions.
Our model has not only identified that the hospital load is the most critical,
but also the sequence of repairs for the transformers upstream of the hospital!

TODO: Insert interactive graph visualization.

![TODO](./repair_priority_graph.png)

## Conclusion and Next Steps

In just a few lines of code, you've built a RelationalAI model over power grid data in Snowflake,
defined rules to prioritize repairs to the grid after a storm, and visualized the results.
But you've only just scratched the surface of what's possible with RelationalAI!

Whether you're managing critical infrastructure, optimizing operational flows,
predicting market trends, or identifying fraudulent activity,
RelationalAI provides the secure, scalable, and dynamic modeling environment you need
to power every decision with intelligence.

TODO: Links to other resources and more advanced topics.

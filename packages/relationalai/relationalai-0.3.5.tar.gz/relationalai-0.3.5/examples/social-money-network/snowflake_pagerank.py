#pyright: reportUnusedExpression=false
from typing import Tuple
import rich
import relationalai as rai
from relationalai.std import aggregates
from relationalai.std.graphs import Graph

model = rai.Model("SFPagerank")

#--------------------------------------------------
# Initialize Snowflake data
#--------------------------------------------------

Account = model.Type("Account", source="sandbox.public.accounts")

Transaction = model.Type("Transaction", source="sandbox.public.transactions")
Transaction.define(
    from_ = (Account, "from_account", "account_id"),
    to = (Account, "to_account", "account_id")
)

#--------------------------------------------------
# Add types
#--------------------------------------------------

Merchant = model.Type("Merchant")
Person = model.Type("Person")

with model.rule():
    a = Account()
    with a.account_type == "Merchant":
        a.set(Merchant)
    with a.account_type == "User":
        a.set(Person)

#--------------------------------------------------
# Create a graph
#--------------------------------------------------

graph = Graph(model)
Node, Edge = graph.Node, graph.Edge

Node.extend(Account, name=Account.name)
Node.extend(Person, kind="person")
Node.extend(Merchant, kind="merchant", label=Merchant.name)

with model.rule():
    t = Transaction()
    Edge.add(t.from_, t.to, amount=t.amount)

with model.rule():
    m = Merchant()
    rank = graph.compute.pagerank(m)
    Node(m).set(rank=rank)
    m.set(rank=rank)

#--------------------------------------------------
# Visualize the graph
#--------------------------------------------------

graph.visualize(
    three=True,
    node_label_size_factor=1.2,
    use_links_force=True,
    links_force_distance=140,
    node_hover_neighborhood=True,
    style={
        "node": {
            "size": lambda n: (n.get("rank", 0.01) * 100) ** 2.2 + 10,
            "color": lambda n: "green" if n["kind"] == "merchant" else "#bbb",
            "hover": lambda n: f'{n["name"]} ({n.get("rank", 0):,.3f})' if n.get("rank") else n["name"]
        },
        "edge": {
            "opacity": 0.3,
            "color": "#ccc",
            "size": lambda t: t["amount"] / 50
        }
    }
).display()

#--------------------------------------------------
# Export the analysis
#--------------------------------------------------

@model.export("sandbox.public")
def merchant_rank(minimum: float) -> Tuple[str, float, int]:
    m = Merchant()
    m.rank >= minimum
    t = Transaction(to=m)
    total = aggregates.sum(t, t.amount, per=[m])
    return m.name, m.rank, total #type: ignore

print("\nCalling merchant rank from Snowflake!\n")
for row in model.resources._exec("call sandbox.public.merchant_rank(0.04);"):
    rich.print(row)

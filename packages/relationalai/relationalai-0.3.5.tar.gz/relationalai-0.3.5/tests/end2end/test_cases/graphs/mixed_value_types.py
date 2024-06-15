# pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.std.graphs import Graph
from relationalai.std.aggregates import sum
from relationalai.std import alias

#--------------------------------------------------
# Types
#--------------------------------------------------

model = rai.Model(
    name=globals().get("name", "test_mixed_value_types"), config=globals().get("config")
)
model._config.set("compiler.use_value_types", True)
model._config.set("compiler.use_multi_valued", True)

Person = model.Type("Person")
Criminal = model.Type("Criminal")
Transaction = model.Type("Transaction")
Dude = model.Type("Dude")

#--------------------------------------------------
# Load data
#--------------------------------------------------

with model.rule():
    joe = Person.add(name="Joe")
    jane = Person.add(name="Jane")
    bob = Person.add(name="Bob")
    dylan = Person.add(Criminal, name="Dylan")
    dave = Person.add(name="Dave")

    joe.knows.add(jane)
    jane.knows.add(bob)
    bob.knows.extend([joe, dylan])
    dylan.knows.add(joe)

    dude = Dude.add(name="Woop")
    dude.knows.add(dylan)

    Transaction.add(from_=joe, to=jane, amount=100)
    Transaction.add(from_=joe, to=jane, amount=1000)
    Transaction.add(from_=joe, to=jane, amount=10)
    Transaction.add(from_=joe, to=bob, amount=10)

#--------------------------------------------------
# Graph
#--------------------------------------------------

graph = Graph(model, with_isolated_nodes=True)
Node, Edge = graph.Node, graph.Edge

Node.extend(Person, label=Person.name)
Node.extend(Criminal, criminal=True, label=Criminal.name)
Node.extend(Dude, criminal=True, label=Dude.name)
Edge.extend(Person.knows, label="knows")
Edge.extend(Dude.knows, label="knows")

with model.rule():
    t = Transaction()
    weight = sum(t, t.amount, per=[t.from_, t.to])
    Edge.add(t.from_, t.to, label="Transfer", weight=weight)

with model.query() as select:
    n = Node()
    component = graph.compute.weakly_connected_component(n)
    Node(component)
    z = select(alias(n, "node"), alias(component, "component"))

print(z.results)
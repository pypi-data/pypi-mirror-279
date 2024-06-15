#pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.std import rel

model = rai.Model(name=globals().get("name", "test_numeric_outputs"), config=globals().get("config"))
Person = model.Type("Person")
Adult = model.Type("Adult")

with model.rule():
    Person.add(name="Joe", age=74)
    Person.add(name="Bob", age=400000000000000000000000)
    Person.add(name="Jane", age=10)

with model.rule():
    p = Person()
    p.age >= 18
    p.set(Adult)

with model.query() as select:
    a = Adult()
    z = select(a.name, rel.int(128, a.age))

print(z.results)

with model.query() as select:
    z = select(rel.decimal(64, 8, rel.sqrt(2)), rel.decimal(128, 20, rel.sqrt(2)))

print(z.results)

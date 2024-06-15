# pyright: reportUnusedExpression=false
import relationalai as rai

model = rai.Model(name=globals().get("name", "test_smoke"), config=globals().get("config"))
Person = model.Type("Person")
Adult = model.Type("Adult")

with model.rule():
    Person.add(name="Joe", age=74)
    Person.add(name="Bob", age=40)
    Person.add(name="Jane", age=10)

with model.rule():
    p = Person()
    p.age >= 18
    p.set(Adult)

with model.rule():
    p = Person()
    with p.age == 10:
        p.set(coolness=100)

with model.query() as select:
    a = Adult()
    10 <= a.age <= 80
    z = select(a, a.name, a.age)
print(z.results.dtypes)

with model.query() as select:
    p = Person()
    with model.found():
        p.coolness
    z = select(p, p.coolness)

print(z.results.dtypes)

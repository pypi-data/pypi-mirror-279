import relationalai as rai

model = rai.Model(name=globals().get("name", "test_first"), config=globals().get("config"))

Person = model.Type("Person")

with model.rule():
    Person.add(name="Sam Watson")
    Person.add(name="Pete Vilter")
    Person.add(name="Josh Cole")

with model.query() as select:
    p = Person()
    z = select(
        p.name
    )  # @NOTE: we don't actually need to use the result, it'll get snapshotted all the same

print(z.results)

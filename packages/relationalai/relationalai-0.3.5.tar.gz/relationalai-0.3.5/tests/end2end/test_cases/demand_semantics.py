# pyright: reportUnusedExpression=false
import relationalai as rai
# from relationalai.std import rel

model = rai.Model(name=globals().get("name", "test_demand_driven"), config=globals().get("config"))
Person = model.Type("Person")
Adult = model.Type("Adult")
Pet = model.Type("Pet")
Foo = model.Type("Foo")

with model.rule():
    joe = Person.add(name="Joe", age=74, zomg=10, woop=1, swoop=1)
    joe.pets.extend([
        Pet.add(name="Fluffy", species="cat"),
        Pet.add(name="Spot", species="dog"),
        Pet.add(name="Goldie", species="fish"),
    ])
    joe.foos.extend([
        Foo.add(name="zomg", s=10),
        Foo.add(name="cool", s=100)
    ])
    bob = Person.add(name="Bob", age=40, woop=1)

    Person.add(name="Jane", age=10, boop=100, woop=2, swoop=2)

with model.rule():
    p = Person()
    p.age >= 18
    p.set(Adult, coolness=p.zomg)

with model.rule():
    p = Person()
    p.woops.add(p.pets)

#--------------------------------------------------
# Only joe has coolness
#--------------------------------------------------

with model.query() as select:
    a = Adult()
    z = select(a, a.name, a.coolness)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Multiple accesses shouldn't filter
#--------------------------------------------------

with model.query() as select:
    a = Adult()
    a.coolness
    z = select(a, a.name, a.coolness)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Combinations of Joe's pets
#--------------------------------------------------

with model.query() as select:
    a = Adult()
    p1, p2 = a.pets.choose(2)
    z = select(a.name, p1, p2)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Cross product of pets and foos, but Bob has neither
#--------------------------------------------------

with model.query() as select:
    a = Adult()
    z = select(a, a.name, a.coolness, a.foos, a.pets)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Cross product of pets and foos, but filtered by props
#--------------------------------------------------

with model.query() as select:
    a = Adult()
    z = select(a, a.name, a.coolness, a.pets.name, a.foos.name, a.foos.s)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Match - match filters out empty properties
#--------------------------------------------------

with model.query() as select:
    p = Person()
    with model.match() as m:
        with model.case():
            m.add(p.pets)
        with model.case():
            m.add(p.boop)
    z = select(p.name, m)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Match multiple (Union) - match filters out empty properties
#--------------------------------------------------

with model.query() as select:
    a = Adult()
    with model.match(multiple=True) as m:
        with model.case():
            m.add(a.pets)
        with model.case():
            m.add(a.foos)
    z = select(a.name, m)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Using a rule to pass a collection to another prop
# shouldn't add missing values
#--------------------------------------------------

with model.query() as select:
    p = Person()
    z = select(p.name, p.woops.name)

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# has_value()
#--------------------------------------------------

with model.query() as select:
    p = Person()
    z = select(p.name, p.swoop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    p = Person()
    z = select(p.name, p.swoop.has_value())

print("\n--------------------------------\n")
print(z.results)

#--------------------------------------------------
# Check to make sure that we respect set semantics
# including with nulls
#--------------------------------------------------

with model.query() as select:
    a = Person()
    z = select.distinct(a, a.woop, a.swoop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select.distinct(a.woop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select.distinct(a.swoop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select.distinct(a.woop, a.swoop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select.distinct(a.swoop, a.woop)

print("\n--------------------------------\n")
print(z.results)


#--------------------------------------------------
# Check to make sure that we respect bag select
#--------------------------------------------------

with model.query() as select:
    a = Person()
    z = select(a, a.woop, a.swoop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select(a.woop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select(a.swoop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select(a.woop, a.swoop)

print("\n--------------------------------\n")
print(z.results)

with model.query() as select:
    a = Person()
    z = select(a.swoop, a.woop)

print("\n--------------------------------\n")
print(z.results)
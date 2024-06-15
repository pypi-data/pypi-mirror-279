#pyright: reportUnusedExpression=false
import relationalai as rai

model = rai.Model(name=globals().get("name", "test_union"), config=globals().get("config"))
Person = model.Type("Person")
Adult = model.Type("Adult")

with model.rule():
    Person.add(name="Joe", age=84)
    Person.add(name="Bob", age=40)
    Person.add(name="Jane", age=10)

#--------------------------------------------------
# Make sure shared vars between match branches stay
# in their respective branches - this would previously
# error in dsl.py
#--------------------------------------------------

with model.rule():
    p = Person()
    m = p.age
    with model.match():
        with m.name == "Per Unit":
            m.set(calculated_surcharge_rate=100)
        with m.name == "By Percentage":
            m.set(calculated_surcharge_rate=1000)

#--------------------------------------------------
# Basic union
#--------------------------------------------------

with model.query() as select:
    p = Person()
    with model.match(multiple=True) as cool:
        with p.age > 80:
            cool.add("amazing", rating=1000)
        with p.age > 60:
            cool.add("rad", rating=100)
        with p.age > 18:
            cool.add("awesome", rating=10)
    z = select(p.name, cool, cool.rating)

print(z.results)

#--------------------------------------------------
# Basic ordered choice
#--------------------------------------------------

with model.query() as select:
    p = Person()
    with model.match() as cool:
        with p.age > 80:
            cool.add("amazing", rating=1000)
        with p.age > 60:
            cool.add("rad", rating=100)
        with p.age > 18:
            cool.add("awesome", rating=10)
    z = select(p.name, cool, cool.rating)

print(z.results)

#--------------------------------------------------
# Ordered choice with effects and no returns
#--------------------------------------------------

with model.rule():
    p = Person()
    with model.match() as w:
        with model.case():
            p.age > 10
            p.set(zomg=10)
        with model.case():
            # p.age <= 10
            p.set(zomg=1)

with model.query() as select:
    p = Person()
    z = select(p, p.zomg)

print(z.results)
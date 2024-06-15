# pyright: reportUnusedExpression=false
import relationalai as rai

model = rai.Model(name=globals().get("name", "test_effects"), config=globals().get("config"))

Person = model.Type("Person")
Adult = model.Type("Adult")
Woop = model.Type("Woop")
Zomg = model.Type("Zomg")

with model.rule():
    joe = Person.add(name="Joe", age=74, key=10, source=100, description="Joe is a cool guy", subbrand=1)
    bob = Person.add(name="Bob", age=40, key=20, source=200, description="Bob is a cool guy", subbrand=2)
    jane = Person.add(name="Jane", age=10, key=30, source=300, description="Jane is a cool gal", subbrand=3)

with model.rule():
    raw = Person()
    i = Adult.add(id=raw.key, source = raw.source).set(Zomg)
    Woop.add(id = raw.subbrand, type= 'raw2').set(Zomg)
    Woop.add(id = raw.subbrand, type= 'raw3').set(Zomg)
    Woop.add(id = raw.subbrand, type= 'raw4').set(Zomg)
    Woop.add(id = raw.subbrand, type= 'raw5').set(Zomg)

with model.query() as select:
    w = Woop()
    z = select(w, w.id, w.type)
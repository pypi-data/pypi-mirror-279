#pyright: reportUnusedExpression=false

# This tests that after we receive an error during query execution, that
# we still restore the temporary rule that captures things like Types
# being added to the model

import relationalai as rai

model = rai.Model(name=globals().get("name", "test_after_errors"), config=globals().get("config"))
model._config.set("compiler.use_value_types", True)

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


try:
    with model.query() as select:
        a = Adult()
        a.foo > 0 # this will cause the rel to fail, since foo doesn't exist
        z = select(a, a.name, a.age)
except Exception:
    pass

# adding a type when value types are on causes initialization code to be added
# to the model's temporary rule
woop = model.Type("Woop")

with model.rule():
    p = Person()
    p.age >= 18
    p.set(Adult)

with model.query() as select:
    a = Adult()
    z = select(a, a.name, a.age)

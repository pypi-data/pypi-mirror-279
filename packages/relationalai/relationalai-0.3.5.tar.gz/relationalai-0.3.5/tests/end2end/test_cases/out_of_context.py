# pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.std import rel
from relationalai.errors import RAIException
import pytest

model = rai.Model(name=globals().get("name", "test_out_of_context"), config=globals().get("config"))
Person = model.Type("Person")
Adult = model.Type("Adult")

with model.rule():
    p = Person()
    p.age >= 18
    woop = p.woop
    d = p.age + 10
    v = rel.sin(3)
    p.set(Adult)

with pytest.raises(RAIException):
    with model.query() as select:
        a = Adult()
        p.foo
        select(a)

with pytest.raises(RAIException):
    with model.query() as select:
        a = Adult()
        select(a, a.name, a.age, p)

with pytest.raises(RAIException):
    with model.query() as select:
        a = Adult()
        select(a, a.name, a.age, woop)

with pytest.raises(RAIException):
    with model.query() as select:
        a = Adult()
        z = d + 10
        select(a, z)

with pytest.raises(RAIException):
    with model.query() as select:
        a = Adult()
        select(a, v)
import pytest

import relationalai as rai
from relationalai import std

model = rai.Model(name=globals().get("name", ""), config=globals().get("config"))
Point = model.Type("Point")

with model.rule():
    Point.add(x=1.1, y=-1, z=0)

# Check that the abs function works
with model.query(tag="abs") as select:
    p = Point(y=-1)
    abs1 = std.math.abs(p.y)
    abs2 = std.math.abs(-1.0)
    select(p, abs1, abs2)

# Check that the isclose function works
with model.query(tag="isclose") as select:
    p = Point(z=0)
    std.math.isclose(p.z, 1e-10)
    select(p, p.z)

# Check that the isclose function works with a tolerance
with model.query(tag="isclose_tolerance") as select:
    p = Point(z=0)
    std.math.isclose(p.z, 1e-8, 1e-9)
    select(p, p.z)  # Should return empty dataframe

# Check that the ceil function works
with model.query(tag="ceil") as select:
    p = Point(x=1.1)
    ceil1 = std.math.ceil(p.x)
    ceil2 = std.math.ceil(0.5)
    select(p, ceil1, ceil2)

# Check that the floor function works
with model.query(tag="floor") as select:
    p = Point(x=1.1)
    floor1 = std.math.floor(p.x)
    floor2 = std.math.floor(0.5)
    select(p, floor1, floor2)

# Check that the cbrt function works
with model.query(tag="cbrt") as select:
    p = Point(y=-1)
    cbrt1 = std.math.cbrt(p.y)
    cbrt2 = std.math.cbrt(8)
    select(p, cbrt1, cbrt2)

# Check that the sqrt function works
with model.query(tag="sqrt") as select:
    p = Point(z=0)
    sqrt1 = std.math.sqrt(p.z)
    sqrt2 = std.math.sqrt(4)
    select(p, sqrt1, sqrt2)

# Check that the sqrt function raises an error when given a negative number
with pytest.raises(ValueError):
    with model.query(tag="sqrt"):
        std.math.sqrt(-1)

# Check that the log function works
with model.query(tag="log") as select:
    p = Point(z=0)
    log1 = std.math.log(p.z)
    log2 = std.math.log(100, 10)
    select(p, log1, log2)

# Check that the log function raises an error when given a negative number
with pytest.raises(ValueError):
    with model.query(tag="log"):
        std.math.log(-1)

# Check that the sign function works
with model.query(tag="sign") as select:
    p = Point(x=1.1, y=-1)
    sign1 = std.math.sign(p.x)
    sign2 = std.math.sign(p.y)
    sign3 = std.math.sign(0)
    select(p, sign1, sign2, sign3)

# Check that the trunc_divide function works
with model.query(tag="trunc_divide") as select:
    p = Point(x=1.1)
    trunc_divide1 = std.math.trunc_divide(p.x, 2)
    trunc_divide2 = std.math.trunc_divide(-5, 2)
    select(p, trunc_divide1, trunc_divide2)

# Check that the sin, cos functions works
for func in [
    std.math.sin,
    std.math.cos,
    std.math.tan,
    std.math.acos,
    std.math.asin,
    std.math.atan,
    std.math.radians,
    std.math.degrees,
]:
    with model.query(tag=func.__name__) as select:
        p = Point()
        select(p, func(p.z), func(0))

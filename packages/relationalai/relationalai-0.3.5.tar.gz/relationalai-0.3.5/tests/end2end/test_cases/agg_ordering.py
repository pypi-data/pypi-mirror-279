#pyright: reportUnusedExpression=false

import relationalai as rai
from relationalai.std import rel, aggregates

model = rai.Model(name=globals().get("name", "test_agg_ordering"), config=globals().get("config"))
Foo = model.Type("Foo")
Bar = model.Type("Bar")

with model.rule():
    Foo.add(name="A", value=100)
    Foo.add(name="B", value=25)
    Foo.add(name="C", value=50)

#--------------------------------------------------
# Simple aggregate
#--------------------------------------------------

with model.query() as select:
    f = Foo()
    z = select(aggregates.count(f))

print(z.results)

#--------------------------------------------------
# Aggregate result used in calculation
#--------------------------------------------------

with model.query() as select:
    f = Foo()
    z = select(rel.minimum(2, aggregates.count(f)))

print(z.results)

#--------------------------------------------------
# Aggregate inputs indirectly referenced after
#--------------------------------------------------

with model.rule():
    b = Foo()
    aggregates.rank_desc(b.value) == 3
    b.set(Bar)

with model.query() as select:
    b = Bar()
    z = select(b.name)

print(z.results)

#--------------------------------------------------
# Ensure variables unify down through multiple aggs
#--------------------------------------------------

with model.rule():
    node = Foo()
    prop = node.value
    prop_rank = aggregates.rank_asc(prop)
    max_rank = aggregates.max(prop_rank)
    min_rank = aggregates.min(prop_rank)
    node.set(color=((prop_rank - min_rank) / (max_rank - min_rank)))

with model.query() as select:
    f = Foo()
    z = select(f.name, f.color)

print(z.results)



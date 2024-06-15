import relationalai as rai
from relationalai.std import rel, aggregates

model = rai.Model(name=globals().get("name", "test_hector"), config=globals().get("config"))

DemandBundle = model.Type("DemandBundle")
Centroid = model.Type("Centroid")
AssignedCentroid = model.Type("AssignedCentroid")
DemandRegion = model.Type("DemandRegion")
Foo = model.Type("Foo")

with model.rule():
    DemandBundle.add(name="Bundle1").set(max_sources=10)

    c0 = Centroid.add(iter=0, cidx=0)
    c0.foo.extend([1, 2])
    c1 = Centroid.add(iter=0, cidx=1)
    c1.foo.add(1)

    DemandRegion.add(name=0,  demand=5, x=2)
    DemandRegion.add(name=1,  demand=8, x=2)
    DemandRegion.add(name=1,  demand=3, x=3)

with model.rule():
    bundles = DemandBundle()
    foo = Foo.add(name="foo")
    with model.scope():
        count_values = aggregates.count(bundles, bundles.max_sources, per=[bundles])
        count_rows = aggregates.count(bundles)
        v = aggregates.sum(bundles, bundles.max_sources, per=[bundles])
        with count_values == count_rows:
            foo.set(value=v)

with model.query() as select:
    tmp = Foo()
    response = select(tmp.name, tmp.value)

print(response.results)

with model.query() as select:
    c0 = Centroid(iter=0)
    new_x = aggregates.sum(c0.foo, per=[c0])
    new_d = rel.sqrt(new_x**2)
    res = select(c0.cidx, new_x, new_d)

print(res.results)

with model.query() as select:
    c0 = Centroid(iter=0)
    r = DemandRegion(name=c0.cidx)
    total_demand = aggregates.sum(r.demand, per=[c0])
    new_x = aggregates.sum(r, r.x * r.demand / total_demand, per=[c0])
    # 16/11 + 9/11 = 25/11 = 2.2727

    res = select(c0.cidx, new_x)

print(res.results)

with model.query() as select:
    c0 = Centroid(iter=0)
    r = DemandRegion(name=c0.cidx)
    total_demand = aggregates.sum(r.demand, per=[c0])
    new_x = aggregates.sum(r, r.x * r.demand / total_demand, per=[c0])
    # 16/11 + 9/11 = 25/11 = 2.2727

    res = select(c0.cidx, r.demand, new_x)

print(res.results)



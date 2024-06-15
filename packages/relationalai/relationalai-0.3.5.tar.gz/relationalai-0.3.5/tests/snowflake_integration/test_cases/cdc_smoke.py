#pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.clients.snowflake import Snowflake

# This test expects the model to already be present, with the data loaded into it.
# It's the same model used by the TastyBytes benchmark.
model = rai.Model(name="PyRelTastyBytesBenchmark", config=globals().get("config"))
sf = Snowflake(model)

Record = sf.TASTYBYTES.HARMONIZED.LOYALTY_ORDERS_REGION_CALIFORNIA

# TODO: re-enable when performance improves (i.e. by turning off IVM, etc)
# with model.query() as select:
#     record = Record()
#     num_records = aggregates.count(record)
#     select(num_records)

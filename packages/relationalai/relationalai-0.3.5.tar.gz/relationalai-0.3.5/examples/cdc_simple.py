#pyright: reportUnusedExpression=false
from typing import Tuple
import relationalai as rai
from relationalai.clients.snowflake import Snowflake
from relationalai.std import aggregates


def setup():
    import pandas as pd
    from pathlib import Path
    from snowflake.connector.pandas_tools import write_pandas
    model = rai.Model("cdc_simple", dry_run=False)
    model.resources._exec("create database if not exists sandbox")
    model.resources._exec("create schema if not exists sandbox.public")
    person = pd.read_csv(Path(__file__).parent / "data/people.csv")
    transaction = pd.read_csv(Path(__file__).parent / "data/transactions.csv")
    dfs = [person, transaction]
    names = ["PERSON", "TRANSACTION"]
    for df, name in zip(dfs, names):
        write_pandas(
            model.resources._conn,
            df,
            name,
            database="SANDBOX",
            schema="PUBLIC",
            auto_create_table=True
        )

model = rai.Model("cdc_simple", dry_run=False)
sf = Snowflake(model)
Person = sf.sandbox.public.person

with model.query() as select:
    person = Person()
    z = select(aggregates.count(person))

print(z.results)

@model.export("sandbox.public")
def person_id(name: str) -> Tuple[int]:
    p = Person()
    p.name == name
    return p.age,

if not model._client.dry_run:
    print("\nCalling person_id from Snowflake!\n")
    print(model.resources._exec("call sandbox.public.person_id('Tommy Roman');").fetch_pandas_all()) # pyright: ignore
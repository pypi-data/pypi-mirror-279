#pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.clients import config as cfg

import snowflake.connector

config = cfg.Config()

connection = snowflake.connector.connect(
    user=config.get('user'),
    password=config.get('password'),
    account=config.get('account'),
    warehouse=config.get('warehouse', ""),
    role=config.get('role', ""),
    client_store_temporary_credential=True,
    client_request_mfa_token=True,
)

model = rai.Model("MyCoolDatabase", connection=connection)
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

with model.query() as select:
    a = Adult()
    z = select(a, a.name, a.age)

print("People!\n")
print(z.results)








<!-- markdownlint-disable MD024 -->

# `relationalai.Model`

```python
class relationalai.Model(name: str, *, profile: str|None = None, connection: SnowflakeConnection|None = None)
```
A RelationalAI Model comprises [objects](../Instance/README.md) representing real-world entities,
categorized by [type](../Type/README.md),
and [rules](./rule.md) defining their properties and relationships.
The `Model` class is used to create, manage, and [query](./query.md) models.

## Parameters

| Name | Type | Description |
| :------ | :--- | :------------ |
| `name` | `str` | The name of the model. Must be at least three characters. May only contain letters, numbers, and underscores. |
| `profile` | `str` or `None` | Optional name of the [conifuration profile](../../configuration/README.md#profiles) to use when creating the model. If `None`, the currently active profile is used. |
| `connection` | `Session` or `None` | Optional Snowpark Session object to use when creating the model. If `None`, connection details in the configuration profile set by the `profile` parameter are used. Ignored in Azure-based projects. |

## Attributes

| Name | Type | Description |
| :--- | :--- | :------ |
| `Model.name` | `str` | The name of the model. |

## Methods

The core methods of the `Model` class are used to create [`Type`](../Type/README.md) instances and contexts for defining rules and querying the model.

| Name | Description | Returns |
| :--- | :------ | :--- |
| [`Model.Type()`](./Type.md) | Create a [`Type`](../Type/README.md) instance for classifying objects in the model. | [`Type`](../Type/README.md) |
| [`Model.rule()`](./rule.md) | Context manager for defining a new rule in the model. | [`Context`](../Context/README.md) |
| [`Model.query()`](./query.md) | Context manager for querying the model. | [`Context`](../Context/README.md) |
| [`Model.read()`](./read.md) | Context manager for reading data from an imported [snapsnot](../../cli/imports_snapshot.md). (Azure only.) | [`Context`](../Context/README.md) |

[`.rule()`](./rule.md), [`.query()`](./query.md), and [`.read()`](./read.md) return a [`Context`](../Context/README.md) object,
which is a Python [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers)
and must be used in a [`with` statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement).
The following methods create subcontexts and must be called from inside a `with` block created by `.rule()`, `.query()`, or `.read()`:

| Name | Description | Returns |
| :--- | :------ | :--- |
| [`Model.scope()`](./scope.md) | Create a scoped context for subqueries. | [`Context`](../Context/README.md) |
| [`Model.found()`](./found.md) | Check that a subquery has at least one result. | [`Context`](../Context/README.md) |
| [`Model.not_found()`](./not_found.md) | Check that a subquery has no results. | [`Context`](../Context/README.md) |
| [`Model.ordered_choice()`](./ordered_choice.md) | Execute subcontexts in an "if-else" fashion. | [`Context`](../Context/README.md) |
| [`Model.union()`](./union.md) | Execute subcontexts in an "or" fashion. | [`Context`](../Context/README.md) |

## Example

```python
import relationalai as rai
from relationalai.clients.snowflake import Snowflake

# Create a new model named "people" and connect it to your Snowflake account.
# Snowflake connection details are read from the active configuration profile.
model = rai.Model("people")
sf = Snowflake(model)

# Get the Person table from the 'sandbox.public' schema in Snowflake.
# Note that the table name is not case-sensitive.
Person = sf.sandbox.public.person

# Create an Adult type in the model.
Adult = model.Type("Adult")

# The model.rule() context manager is used to define rules in the model.
# This rule adds all people over 18 to the Adult type.
with model.rule():
    person = Person()
    person.age >= 18
    person.set(Adult)

# The model.query() context manager is used to query the model.
# This query returns the names of all adults in the model.
with model.query() as select:
    adult = Adult()
    response = select(adult.name)

print(response.results)
# Output:
#     name
# 0  Alice
# 1    Bob
```

> [!IMPORTANT]
> Before you can access a Snowflake table in a model,
> such as the `sandbox.public.person` table in the preceding example,
> you must import the table using the [`rai imports:stream`](../../cli/imports_stream.md) CLI command
> or the [RelationalAI SQL Library](../../../../sql/README.md).
> Your Snowflake user must have the correct priveledges to create a stream on the table.
> Contact your Snowflake administrator if you need help importing a Snowflake table.

To use a [configuration profile](../../configuration/README.md#profiles) other than the active profile,
pass the profile name to the `profile` parameter when creating the model:

```python
# Note that the profile name must be passed as a keyword argument.
model = rai.Model("people", profile="my_profile")
```

To use a Snowpark Session other than the one specified in the configuration profile,
pass a `Session` object to the `connection` parameter when creating the model:

```python
from snowflake.snowpark import Session

connection_parameters = {
    "user": <USER>,
    "password": <PASSWORD>,
    "account": <ACCOUNT>,
    "warehouse": <WAREHOUSE>,
    "database": <DATABASE>,
    "schema": <SCHEMA>
)

conn = Session.builder.configs(connection_parameters).create()

# Note that the connection object must be passed as a keyword argument.
model = rai.Model("people", connection=conn)
```

See the [Snowflake](https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session) docs
for more details on creating Snowpark Session objects.

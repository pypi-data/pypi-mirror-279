# `relationalai.clients.Snowflake.SnowflakeTable`

The `SnowflakeTable` class is a subclass of [`Type`](../../../Type/README.md)
that represents objects imported from a Snowflake table.

```python
class relationalai.clients.snowflake.SnowflakeTable(Type)
```

`SnowflakeTable` objects are not created directly.
You create `SnowflakeTable` instances using a [`Snowflake`](../Snowflake.md) object.
See the [Example](#example) section for details.

> [!IMPORTANT]
> Before you can access a Snowflake table in a model,
> you must import the table using the [`rai imports:stream`](../../cli/imports_stream.md) CLI command
> or the [RelationalAI SQL Library](../../../../sql/README.md).
> Your Snowflake user must have the correct priveledges to create a stream on the table.
> Contact your Snowflake administrator if you need help importing a Snowflake table.

## Parameters

None.

## Methods

- [`SnowflakeTable.describe()`](./describe.md)
- [`SnowflakeTable.fqname()`](./fqname.md)
- [`SnowflakeTable.namespace()`](./namespace.md)

## Example

```python
import relationalai as rai
from relationalai.clients.snowflake import Snowflake

model = rai.Model("myModel")

# Get a new Snowflake instance for the model.
sf = Snowflake(model)

# To access a table, use `sf.<db_name>.<schema_name>.<table_name>`.
Person = sf.sandbox.public.people

# `Person` behaves like a read-only `Type`.
# For instance, this query gets the names and ages of all people.
with model.query() as select:
    person = Person()
    response = (person.name, person.age)
```

The `Person` object returned by `sf.sandbox.public.people` is a [`SnowflakeTable`](./SnowflakeTable.md) instance.
Property names, such as `age`, come from the table's column names and are case-insensitive.
For example, if the column in the table is named `AGE` in all caps,
then `person.AGE` and `person.age` both refer to the same column.

You can view all of the known properties of a `SnowflakeTable` object,
including properties derived from the table's columns,
using the [`.known_properties()`](../../../Type/known_properties.md) method:

```python
print(Person.known_properties())
# Output:
# ['id', 'name', 'age']
```

Use the [`SnowflakeTable.describe()`](./SnowflakeTable/describe.md) method to describe table columns,
such as which column serves as the [primary key](./PrimaryKey.md):

```python
import relationalai as rai
from relationalai.clients.snowflake import Snowflake, PrimaryKey

model = rai.Model("myModel")
sf = Snowflake(model)

Person = sf.sandbox.public.people
# Set the `id` column as the primary key.
Person.describe(id=PrimaryKey)
```

Multiple primary key columns are supported.

Primary keys are automatically detected from the table's Schema in Snowflake,
provided the table has a primary key constraint.
If the table does not have a primary key constraint,
then `.describe()` may be used to manually designate a primary key for the model to use.
Calling describe does not alter the table's schema in Snowflake.

You may also define foreign key relationships.
See [`SnowflakeTable.describe()`](./SnowflakeTable/describe.md) for more details.

## See Also

[`PrimaryKey`](./PrimaryKey.md) and [`Snowflake`](../Snowflake.md)

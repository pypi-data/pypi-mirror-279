# `relationalai.Type.known_properties()`

```python
relationalai.Type.known_properties() -> list[str]
```

Returns a list of all known properties of objects of type `Type`.


## Parameters

No parameters.

## Returns

A list of strings of names of all known properties of objects of type `Type`.

## Example

Properties set using [`Type.add()`](./add.md) are known to the type:

```python
import relationalai as rai

# Create a model named "people" with Person and Adult types.
model = rai.Model("people")
Person = model.Type("Person")
Adult = model.Type("Adult")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", age=20)
    Person.add(name="Bob", age=15)

# All people who are 18 or older are adults.
with model.rule():
    person = Person()
    person.age >= 18
    person.set(Adult)

# The 'name' and 'age' properties are known to the Person type.
print(Person.known_properties())
# Output:
# ['name', 'age']

# But the 'name' and 'age' properties are not known to the Adult type.
print(Adult.known_properties())
# Output:
# []
```

If you pass additional types to `Type.add()`,
any properties set in the same call to `Type.add()` are known to all types:

```python
with model.rule():
    Person.add(Adult, name="Charlie", birthday="1990-01-01")

# The 'name' and 'birthday' properties are known to both the Person and Adult types,
# because they were set in the same call to Type.add(). But the 'age' property is
# only known to the Person type.
print(Person.known_properties())
# Output:
# ['name', 'age', 'birthday']

print(Adult.known_properties())
# Output:
# ['name', 'birthday']
```

If you call a type in a [rule](../Model/rule.md) with a second type as an argument,
any properties set on the object in the rule are known to both types:

```python
# Give people who are adults a "coolness" property that decreases with their age.
with model.rule():
    person = Person(Adult)
    person.set(coolness = 118 - person.age)

print(Person.known_properties())
# Output:
# ['name', 'age', 'birthday', 'coolness']

print(Adult.known_properties())
# Output:
# ['name', 'birthday', 'age', 'coolness']
```

In addition to the `coolness` property,
the `age` property is also known by the `Adult` type because it was requested from the `person` object in the rule.

Note, however, that the second type _must_ be passed as an argument when calling the first type in the rule.
For instance, the following rule, while logically equivalent to the previous rule,
does not result in the `coolness` and `age` properties being known to the `Adult` type:

```python
with model.rule():
    person = Person()
    Adult(person)
    person.set(coolness = 118 - person.age)

print(Person.known_properties())
# Output:
# ['name', 'age', 'birthday', 'coolness']

print(Adult.known_properties())
# Output:
# ['name', 'birthday']
```

Properties of objects used as nodes in a [`Graph`](../std/graphs/Graph/README.md) object
are not known to the graph's `Node` type:

```python
from relationalai.std.graphs import Graph

graph = Graph(model)
graph.Node.extend(Person, name=Person.name)

with model.rule():
    node = graph.Node()
    node.set(type="person")

# The Node type knows about the 'name' properties because it was set using extend().
# It also knows about the 'type' property because it was set in the rule.
# But it does not know about the 'age' or 'birthday' properties of the Person type.
print(graph.Node.known_properties())
# Output:
# ['name', 'type']

# Properties set on nodes are not known to the parent types.
# For example, the 'type' property of the graph.Node type is not known to the Person type.
print(Person.known_properties())
# Output:
# ['name', 'age', 'birthday']
```

Properties derived from columns in a Snowflake table are known to the [`SnowflakeTable`](../clients/snowflake/SnowflakeTable/README.md) type:

```python
import relationalai as rai
from relationalai.clients.snowflake import Snowflake

# Create a model named "transactions."
model = rai.Model("transactions")

# Connect the model to your Snowflake account.
sf = Snowflake(model)

# Access objects imported from the 'transaction' table the 'sandbox.public' Snowflake schema.
Transaction = sf.sandbox.public.transaction

print(Transaction.known_properties())
# Output:
# ['transaction_id', 'customer_id', 'amount', 'timestamp']
```

> [!IMPORTANT]
> Before you can access a Snowflake table in a model,
> you must import the table using the [`rai imports:stream`](../../cli/imports_stream.md) CLI command
> or the [RelationalAI SQL Library](../../../../sql/README.md).
> Your Snowflake user must have the correct priveledges to create a stream on the table.
> Contact your Snowflake administrator if you need help importing a Snowflake table.

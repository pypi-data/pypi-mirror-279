# `relationalai.Instance.set()`

```python
Instance.set(*args, **kwargs) -> Instance
```

Set properties and assign [types](../Type/README.md) to an [`Instance`](./README.md) object and return the `Instance`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Type`](../Type/README.md) | Optional types to apply to the object. |
| `*kwargs` | `Any` | Properties to set on the `Instance`, using `<property_name>=<value>`. Accepts [`Producer`](../Producer/README.md) objects, numbers, strings, dates, and `datetime` objects. |


## Returns

Returns the [`Instance`](../Instance/README.md) object on which the property or type is set.

## Example
Use `.set()` to set properties and assign types to an object in your model:

```python
import relationalai as rai

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")
Musician = model.Type("Musician")

with model.rule():
    # Add Person named "Kermit" to the model.
    kermit = Person.add(name="Kermit")
    # Set Kermit as a Musician and set his favorite_color property to "green."
    kermit.set(Musician, favorite_color="green")
```

Both [`Type.add()`](../Type/add.md) and `Instance.set()` set properties on objects.
`Person.add()` initially adds an object with the `name` property set to `"Kermit"` and assigns it to the variable `kermit`.
Subsequently, `kermit.set(Musician, favorite_color="green")` assigns the `Musician` type to the `kermit` object
and sets his `favorite_color` to "green".
Unlike `Instance.set()`, properties set by [`Type.add()`](../Type/add.md) function like primary keys in a SQL database,
uniquely identifying each object.

You can assign multiple types and set several properties simultaneously
by passing multiple [`Type`](../Type/README.md) objects as positional arguments
and multiple property values as keyword arguments to `.set()`.

Properties created by both `Type.add()` and `Instance.set()` are single-valued.
Setting a property a second time overwrites the previous value:

```python
# Get Kermit's favorite color.
with model.query() as select:
    person = Person(name="Kermit")
    response = select(person.favorite_color)

# Currently, it is "green."
print(response.results)
# Output:
#   favorite_color
# 0          green

# Change Kermit's favorite color to "blue."
with model.rule():
    kermit = Person(name="Kermit")
    kermit.set(favorite_color="blue")

# Get Kermit's favorite color again.
with model.query() as select:
    person = Person(name="Kermit")
    response = select(person.favorite_color)

print(response.results)
# Output:
#   favorite_color
# 0           blue
```

Attempting to set a multi-valued property using `.set()` raises an `Exception`:

```python
# Add a friends property to Kermit.
# friends is a multi-valued property because it is created with InstanceProperty.extend().
with model.rule():
    kermit = Person(name="Kermit")
    kermit.friends.extend(["Fozzie", "Miss Piggy", "Rowlf"])

# Attempt to set friends to "Gonzo" using .set().
with model.rule():
    kermit = Person(name="Kermit")
    kermit.set(friends="Gonzo")

# Output:
# Exception: Trying to use a property `friends` as both singular and multi-valued
```

See the [InstanceProperty](../InstanceProperty/README.md) documentation for more information on multi-valued properties.

## See Also

[`Type.add()`](../Type/add.md)

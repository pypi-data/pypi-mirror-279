<!-- markdownlint-disable MD024 -->

# `relationalai.Type`

```python
class relationalai.Type(model: Model, name: str)
```

Types are used to categorize objects in a [model](../Model/README.md).
You create types using the [`Model.Type()`](../Model/Type.md) method,
which returns an instance of the `Type` class.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](../Model/README.md) | The model in which the type is created. |
| `name` | `str` | The name of the type. Type names must begin with a Unicode letter or an underscore followed by one or more Unicode letters, underscores, or numbers. |

## Attributes

| Name | Type | Description |
| :--- | :--- | :------ |
| [`Type.model`](./model.md) | [`Model`](../Model/README.md) | The model to which the type belongs. |
| [`Type.name`](./name.md) | `str` | The name of the type. |

## Methods

| Name | Description | Returns |
| :--- | :------ |
| [`Type.__call__()`](./call__.md) | Query objects of this type. | [`Instance`](../Instance/README.md) |
| [`Type.__or__()`](./or__.md) | Create a union of two types. | `TypeUnion` |
| [`Type.add()`](./add.md) | Add a new object to the model. | [`Instance`](../Instance/README.md) |
| [`Type.extend()`](./extend.md) | Extend the type with all objects from another type. | `None` |
| [`Type.known_properties()`](./known_properties.md) | Get all known properties of objects of type `Type`. | `List[str]` |

## Example

Use [`Model.Type()`](../Model/Type.md) to create a `Type` object rather than constructing one directly:

```python
import relationalai as rai

# Create a new model named "people" with Person and Adult types.
model = rai.Model("people")
Person = model.Type("Person")
Adult = model.Type("Adult")

# Add some people to the model in a rule context using Person.add().
with model.rule():
    Person.add(name="Alice", age=30)
    Person.add(name="Bob", age=20)
    Person.add(name="Carol", age=10)

# All people who are at least 18 years old are adults.
with model.rule():
    person = Person()  # Get all Person objects.
    person.age >= 18  # Filter for people who are at least 18 years old.
    person.set(Adult)  # Set each person as a member of the Adult type.

# Query the model for names of adults.
with model.query() as select:
    adult = Adult()  # Get all Adult objects.
    response = select(adult.name)  # Select the name of each adult.

print(response.results)
# Output:
#     name
# 0  Alice
# 1    Bob
```

## See Also

[`Model.Type()`](../Model/Type.md)
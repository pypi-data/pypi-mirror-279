<!-- markdownlint-disable MD024 -->

# `relationalai.Instance`

```python
class relationalai.Instance()
```

`Instance`, as a subclass of [`Producer`](../Producer/README.md),
produces model objects in [rule](../Rule/README.md) and [query](../Query/README.md) contexts.
They are created by calling a [`Type`](../Type/README.md) or the [`Type.add()`](../Type/add.md) method.

## Methods

In addition to the methods inherited from [`Producer`](../Producer/README.md), `Instance` supports:

| Name | Description | Returns |
| :------ | :---------- | :------ |
| [`.set(*args, **kwargs)`](./set.md) | Set a `Type` or a property on an object. | `Instance` |

## Example

`Instance` objects act as variables representing model objects in [rules](../Rule/README.md) and [queries](../Query/README.md).
Here's how to create and manipulate an `Instance`:

```python
import relationalai as rai

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    # Add a person named "Kermit" to the model.
    # Person.add() returns an Instance.
    kermit = Person.add(name="Kermit")
    # Set Kermit's favorite color to "green" using Instance.set().
    kermit.set(favorite_color="green")

    # Add a person named "Rolf" to the model.
    rolf = Person.add(name="Rowlf")
    # Set Rolf's favorite color to "brown" using Instance.set().
    rolf.set(favorite_color="brown")

with model.query() as select:
    # Get all Person objects.
    # Person() returns an Instance.
    person = Person()
    # Filter objects by name.
    person.name == "Kermit"
    # Select the name and favorite_color properties of the Person objects.
    # Properties are accessed as Instance attributes.
    response = select(person.favorite_color)

print(response.results)
# Output:
#      name favorite_color
# 0  Kermit          green
```

In the above example's rule:

1. `Person.add(name="Kermit")` returns an `Instance` that produces a `Person` object with a `name` property set to the string `"Kermit"`.
2. `kermit.set(favorite_color="green")` sets Kermit's `favorite_color` property to the string `"green"`.
   Property values may also be numbers, dates, `datetime` objects, or `None`.
   `favorite_color` is single-valued, meaning setting it a second time overwrites the previous value.
   See the [`.set()`](./set.md) method docs for more information on single- and multi-valued properties.
   Note that `kermit.set()` returns the `kermit` instance, although it is not used here.

In the query:

3. `Person()` returns an `Instance` that produces `Person` objects.
4. `person.name == "Kermit"` filters the objects produced by `Person()`, letting only those with the name `"Kermit"` pass through.
   Alternatively, you may combine this line with the first as `person = Person(name="Kermit")`.
5. `select(person.favorite_color)` selects the `favorite_color` property of the remaining objects.

`person.name` and `person.favorite_color` return [`InstanceProperty`](../InstanceProperty/README.md) objects,
a type of [producer](../Producer/README.md) that represents object properties.
The [`==` operator](../Producer/eq__.md) returns an [`Expression`](../Expression.md),
yet another type of producer that filters objects based on whether or not the expression evaluates to `True`.

## See Also

[`Expression`](../Expression.md),
[`InstanceProperty`](../InstanceProperty/README.md),
and [`Producer`](../Producer/README.md).

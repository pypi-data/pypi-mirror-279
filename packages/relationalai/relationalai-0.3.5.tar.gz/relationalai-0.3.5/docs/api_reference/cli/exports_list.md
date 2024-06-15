# `exports:list`

```sh
rai exports:list [OPTIONS]
```

List all of the SQL objects, such as stored procedures, exported from RelationalAI to Snowflake.

## Options

| Option | Type | Required | Description |
| :--- | :--- | :--- | :------ |
| `--model` | Text | No | The name of the [model](../python/Model/README.md) from which exports originate. |

## Example

Use the `exports:list` command without any options to interactively select a model and list all exports from that model:

```sh
rai exports:list
```

List all exports from the RelationalAI model named `myModel`:

```sh
rai exports:list --model myModel
```

# `imports:list`

```sh
rai imports:list [OPTIONS]
```

List objects imported into a RelationalAI model.

## Options

| Option | Type | Description |
| :------ | :--- | :------------ |
| `--model` | String | The name of the [model](../python/Model/README.md) for which imports are filtered. |

## Example

Use the `imports:list` command to list all objects imported into a RelationalAI model.
For example, to list all imports for a model named `myModel`, run:

```sh
❯ rai imports:list --model myModel

---------------------------------------------------
 
▰▰▰▰ Imports fetched


  Import                                  Type               Status
 ────────────────────────────────────────────────────────────────────
  SNOWFLAKE_DB.SCHEMA.TABLE1              Snowflake object   SYNCING
  SNOWFLAKE_DB.SCHEMA.TABLE2              Snowflake object   SYNCED


---------------------------------------------------
```

If no model named `myModel` exists, the command returns an error message:

```sh
❯ rai imports:list --model myModel

---------------------------------------------------
 
▰▰▰▰ Imports fetched               

No imports found

---------------------------------------------------
```

If the `--model` option is not provided, you are prompted to interacively select a model from a list of available models:

```sh
❯ rai imports:list

---------------------------------------------------
 
▰▰▰▰ Models fetched   

? Select a model: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   2/2                                                                                   │
│❯ myModel                                                                                 │
│  myModel2                                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Imports fetched


  Import                                  Type               Status
 ────────────────────────────────────────────────────────────────────
  SNOWFLAKE_DB.SCHEMA.TABLE1              Snowflake object   SYNCING
  SNOWFLAKE_DB.SCHEMA.TABLE2              Snowflake object   SYNCED


---------------------------------------------------
```

Use the arrow keys to select a model and press `Enter` to confirm your selection.
You can search for a model by typing part of its name in the prompt.

## See Also

[`imports:snapshot`](./imports_snapshot.md),
[`imports:stream`](./imports_stream.md),
and [`imports:delete`](./imports_delete.md).

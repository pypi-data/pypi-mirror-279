# `imports:delete`

```sh
rai imports:delete [OPTIONS]
```

Delete an import from a RelationalAI model.

> [!NOTE]
> Removing an import from a model does not delete the data in the host platform.
> For instance, if you delete an object imported from a Snowflake table, the table remains in Snowflake.

## Options

| Option | Type | Description |
| :------ | :--- | :------------ |
| `--model` | Text | The name of the [model](../python/Model/README.md) from which to delete the import. |
| `--object` | Text | The name of the object to delete. |

## Example

Use the `imports:delete` command without any options to interactively delete an import from a RelationalAI model:

```sh
$ rai imports:delete

▰▰▰▰ Models fetched   

? Select a model: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   2/2                                                                                   │
│❯ myModel                                                                                 │
│  myModel2                                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Imports fetched

? Select objects (tab for multiple): 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   3/3 (0)                                                                               │
│❯ SNOWFLAKE_DB.SCHEMA.TABLE1                                                              │
│  SNOWFLAKE_DB.SCHEMA.TABLE2                                                              │
│  SNOWFLAKE_DB.SCHEMA.TABLE3                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ SNOWFLAKE_DB.SCHEMA.TABLE1 removed   

---------------------------------------------------
```

Use the up and down arrow keys to navigate the list of models and imports.
You can search for a model or import by typing part of its name in the prompt.
Use the `TAB` key to select multiple imports if you need to delete more than one import from the same model.

To delete an import without interactively selecting the model and object,
pass arguments the `--model` and `--object` options:

```sh
$ rai imports:delete --model myModel --object my_import

---------------------------------------------------
 
▰▰▰▰ Imports fetched
▰▰▰▰ my_import removed

---------------------------------------------------
```

If either of the `--model` or `--object` options is missing,
you are prompted to select them interactively.

## See Also

[`imports:list`](./imports_list.md),
[`imports:snapshot`](./imports_snapshot.md),
and [`imports:stream`](./imports_stream.md).
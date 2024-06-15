# `imports:stream`

```sh
rai imports:stream [OPTIONS]
```

Stream data from a Snowflake table or view into RelationalAI.

> [!IMPORTANT]
> `imports:stream` is only available for Snowflake-based models.

An import stream utilizes [change data capture](https://docs.snowflake.com/en/user-guide/streams)
to synchronize your Snowflake data with your RelationalAI model at an interval of once per minute.

## Options

| Option | Type | Description |
| :------ | :--- | :------------ |
| `--source` | Text | The [fully-qualified name](https://docs.snowflake.com/en/sql-reference/name-resolution) of a Snowflake table or view. |
| `--model` | Text | The name of the [model](../python/Model/README.md) to which the data in the Snowflake table or view is streamed. |

## Example

Use the `imports:stream` command without any options to interactively select a Snowflake table or view to stream into a RelationalAI model:

```sh
❯ rai imports:stream

---------------------------------------------------
 
▰▰▰▰ Models fetched   

? Select a model: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   2/2                                                                                   │
│❯ myModel                                                                                 │
│  myModel2                                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Databases fetched   

? Select a database: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   2/2                                                                                   │
│❯ MY_DATABASE1                                                                            │
│  MY_DATABASE2                                                                            │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Schemas fetched   

? Select a schema: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   2/2                                                                                   │
│❯ MY_SCHEMA1                                                                              │
│  MY_SCHEMA2                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Tables fetched   

? Select tables (tab for multiple): 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   2/2 (0)                                                                               │
│❯ MY_TABLE1                                                                               │
│  MY_TABLE2                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Stream for MY_DATABASE1.MY_SCHEMA1.MY_TABLE1 created   

---------------------------------------------------
```

Use the up and down arrow keys to navigate the interactive prompts and press `Enter` to select an option.
You may select multiple tables to import by pressing the `tab` key.
Each prompt is searchable.
Simply start typing to filter the available options.

You may provide either of the `--model` or `--source` options to skip the interactive prompts.
Provide both to create a stream without any prompts:

```sh
$ rai imports:stream --model myModel --source MY_DATABASE1.MY_SCHEMA1.MY_TABLE1

---------------------------------------------------

▰▰▰▰ Stream for MY_DATABASE1.MY_SCHEMA1.MY_TABLE1 created   

---------------------------------------------------
```


Once the stream is finished setting up,
data from the table may be accessed using the `relationalai` Python package:

```python
import relationalai as rai
from relationalai.clients.snowflake import Snowflake

model = rai.Model("myModel")

# Initialize a Snowflake object with your model.
sf = Snowflake(model)

# Access `my_table` as a Python object.
MyTable = sf.my_database.my_schema.my_table
```

See the [`Snowflake` client](../python/clients/snowflake/README.md) docs for more information on how to interact with your Snowflake data from Python with RelationalAI.

## See Also

[`imports:list`](./imports_list.md),
[`imports:snapshot`](./imports_snapshot.md),
and [`imports:delete`](./imports_delete.md).

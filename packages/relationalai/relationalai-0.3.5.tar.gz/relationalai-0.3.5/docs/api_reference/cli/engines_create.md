# `engines:create`

```sh
rai engines:create [OPTIONS]
```

Create a new RelationalAI engine.

## Options

| Option | Type | Description |
| :------ | :--- | :---------- |
| `--name` | Text | The name of the engine. Must be at least three characters, begin with a letter, and may only contain letters, numbers, and underscores. If missing, you are prompted to enter the name interactively. |
| `--size` | Text | The size of the engine. Must be one of `XS`, `S`, `M`, or `L`. If missing, you are prompted to select the size interactively. |
| `--pool` | Text | The Snowflake compute pool to create the engine in. If missing, you are prompted to select the pool interactively. Not used in Azure-based project. |

## Example

Use the `engines:create` command to create a new RelationalAI engine.
For example, to create a new engine named `my-engine` of size `S`, execute the following command:

```sh
$ rai engines:create --name my_engine --size S

---------------------------------------------------
 
▰▰▰▰ Fetched compute pools   

? Compute pool: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   4/4                                                                                   │
│❯ [REFETCH LIST]                                                                          │
│  SF_POOL_1                                                                               │
│  SF_POOL_2                                                                               │
│  SF_POOL_3                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Engine 'my_engine' created!                                                            

---------------------------------------------------
```

> [!NOTE]
> The `engines:create` command blocks until the engine is ready, which may take several minutes.

In Snowflake-based projects, engines are created in a Snowflake compute pool,
which you must select from the list of available pools.
Use the up and down arrow keys to navigate the list of pools.
You can search for a pool by typing part of its name in the prompt.

Alternatively, you can use the `--pool` option to specify the pool name directly:

```sh
$ rai engines:create --name my_engine --size S --pool my_snowflake_pool

---------------------------------------------------

▰▰▰▰ Engine 'my_engine' created!                                                            

---------------------------------------------------
```

Azure-based projects do not use compute pools, so the `--pool` option is not available.

## See Also

[`engines:list`](./engines_list.md),
[`engines:get`](./engines_get.md),
and [`engines:delete`](./engines_delete.md).

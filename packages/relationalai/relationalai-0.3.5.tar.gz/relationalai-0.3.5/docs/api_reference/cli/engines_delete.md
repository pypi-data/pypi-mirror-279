# `engines:delete`

```sh
rai engines:delete [OPTIONS]
```

Delete an engine.

## Options

| Option | Type | Description |
| :------ | :--- | :---------- |
| `--name` | Text | The name of the engine to delete. If missing, you are prompted to enter the name interactively. |

## Example

Use the `engines:delete` command to delete an existing RelationalAI engine.
For example, to delete an engine named `my_engine`, execute the following command:

```sh
$ rai engines:delete --name my_engine

---------------------------------------------------
 
▰▰▰▰ Engine 'my_engine' deleted!

---------------------------------------------------
```

If no engine named `my_engine` exists, an error message is displayed:

```sh
$ rai engines:delete --name my_engine

---------------------------------------------------
 
Engine 'my_engine' not found

---------------------------------------------------
```

If the `--name` option is missing, you are prompted to select the engine name interactively:

```sh
$ rai engines:delete

---------------------------------------------------
 
▰▰▰▰ Fetched engines   

? Select an engine: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   3/3                                                                                   │
│❯ [REFETCH LIST]                                                                          │
│  my_engine                                                                               │
│  my_other_engine                                                                         │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Engine 'my_engine' deleted!

---------------------------------------------------
```

Use the up and down arrow keys to navigate the list of engines.
You can search for an engine by typing part of its name in the prompt.

## See Also

[`engines:list`](./engines_list.md),
[`engines:get`](./engines_get.md),
and [`engines:create`](./engines_create.md).

# `engines:get`

```sh
rai engines:get [OPTIONS]
```

Get engine details.

## Options

| Option | Type | Description |
| :------ | :--- | :--------- |
| `--name` | Text | The name of the engine to get details for. |

## Example

Use the `engines:get` command to get details for a specific engine.
For example, to get details for an engine named `my_engine`, execute the following command:

```sh
$ rai engines:get --name my_engine

---------------------------------------------------
 

  Name       Size   State
 ─────────────────────────
  my_engine  S      READY


---------------------------------------------------
```

If no engine named `my_engine` exists, an error message is displayed:

```sh
 
$ rai engines:get --name my_engine

---------------------------------------------------
 
Engine not found                     

---------------------------------------------------
```

If the `--name` option is missing, you are prompted to select the engine name interactively:

```sh
❯ rai engines:get

---------------------------------------------------
 
? Engine name: my_engine


  Name       Size   State
 ─────────────────────────
  my_engine  S      READY


---------------------------------------------------
```

## See Also

[`engines:list`](./engines_list.md),
[`engines:create`](./engines_create.md),
and [`engines:delete`](./engines_delete.md).

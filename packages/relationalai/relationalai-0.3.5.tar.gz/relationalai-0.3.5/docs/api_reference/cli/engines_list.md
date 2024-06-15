## `engines:list`

```sh
rai engines:list [OPTIONS]
```

List all RelationalAI engines.

## Options

| Option | Type | Description |
| :------ | :--- | :--------- |
| `--state` | Text | Filter engines by state. Possible values: `ready`, `pending`, and `suspended`. |

## Example

Use the `engines:list` command to list all RelationalAI engines available in your account:

```sh
$ rai engines:list

---------------------------------------------------


  Name                    Size   State    
 ──────────────────────────────────────── 
  my_small_engine         S      READY    
  my_large_engine         L      READY        
  test_engine             S      PENDING  


---------------------------------------------------
```

To filter the list by the state of the engine, use the `--state` option.
For example, to list only the engines that are in the `READY` state, execute the following command:

```sh
$ rai engines:list --state ready

---------------------------------------------------


  Name                    Size   State    
 ──────────────────────────────────────── 
  my_small_engine         S      READY    
  my_large_engine         L      READY        


---------------------------------------------------
```

## See Also

[`engines:get`](./engines_get.md),
[`engines:create`](./engines_create.md),
and [`engines:delete`](./engines_delete.md).

# `transactions:list`

```sh
rai transactions:list [OPTIONS]
```

List transactions.

## Options

| Option | Type | Description |
| :------ | :--- | :------------ |
| `--id` | Text | Filter transactions by ID. |
| `--state` | Text | Filter transactions by state. |
| `--limit` | Integer | Limit the number of transactions to list. |
| `--all-users` | Flag | List transactions for all users. |

## Example

Use the `transactions:list` command without any options to list all of your transactions:

```sh
$ rai transactions:list

---------------------------------------------------
 
▰▰▰▰ Transactions fetched   

                                                                                            
  ID                                  Schema    State       Created               Duration  
 ────────────────────────────────────────────────────────────────────────────────────────── 
  01b439a7-0002-6944-0051-c0070497…   myModel   COMPLETED   2024-05-09 18:15:31       2.4s  
  01b439a7-0002-693d-0051-c0070498…   myModel   COMPLETED   2024-05-09 18:15:06      20.5s  
                                                                                            

---------------------------------------------------
```

To filter transactions by ID, state, or limit, pass the corresponding option:

```sh
$ rai transactions:list --state aborted --limit 1

---------------------------------------------------
 
▰▰▰▰ Transactions fetched   

                                                                                            
  ID                                  Schema    State     Created               Duration  
 ────────────────────────────────────────────────────────────────────────────────────────── 
  01b439a7-0002-692f-0051-c0070497…   myModel   ABORTED   2024-05-09 18:16:28       1.2s  
                                                                                            

---------------------------------------------------
```

To list transactions for all users, not just the current user, use the `--all-users` flag.

## See Also

[`transactions:get`](./transactions_get.md) and [`transactions:cancel`](./transactions_abort.md).

# `transactions:cancel`

```sh
rai transactions:cancel [OPTIONS]
```

Cancel a transaction.

## Options

| Option | Type | Description |
| :------ | :--- | :--------- |
| `--id` | Text | The ID of the transaction to cancel. If missing, you are prompted to enter the ID interactively. |
| `--all-users` | Flag | Show transactions from all users. If missing, only transactions from active config profile's user are shown. |

## Example

Use the `transactions:cancel` command without any options to interactively select a transaction to cancel:

```sh
$ rai transactions:cancel

---------------------------------------------------
 
▰▰▰▰ Transactions fetched   
                                            
  ID   Schema   State   Created   Duration  
 ────────────────────────────────────────── 
                                            
? Select a transaction to cancel: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   1/1                                                                                   │
│❯ 01b439b8-0002-6941-0051-c007049869fa                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Transaction cancelled   

---------------------------------------------------
```

Use the up and down arrow keys to navigate the list of transactions, and press `Enter` to select a transaction to cancel.
You can search for a transaction by typing part of its ID in the prompt.

Use the `--all-users` flag to show transactions from all users in the interactive list.

If you know the ID of the transaction you want to cancel, you can specify it using the `--id` option and skip the interactive propmt:

```sh
$ rai transactions:cancel --id 01b439b8-0002-6941-0051-c007049869fa

---------------------------------------------------

▰▰▰▰ Transaction cancelled

---------------------------------------------------
```

## See Also

[`transactions:list`](./transactions_list.md) and [`transactions:get`](./transactions_get.md).

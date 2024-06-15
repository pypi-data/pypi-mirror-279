# `transactions:get`

```sh
rai transactions:get [OPTIONS]
```

Get transaction details.

## Options

| Option | Type | Description |
| :------ | :--- | :--------- |
| `--id` | Integer | The ID of the transaction to get details for. If missing, you are prompted to enter the ID interactively. |

## Example

Use the `transactions:get` command to get details for a specific transaction.
If you know the ID of the transaction, you can specify it using the `--id` option:

```sh
❯ rai transactions:get --id 01b439b2-0002-6941-0051-c0070498679a

---------------------------------------------------
 
▰▰▰▰ Transaction fetched   

                                                       
  Field          Value                                 
 ───────────────────────────────────────────────────── 
  id             01b439b2-0002-6941-0051-c0070498679a  
  database       myModel                               
  state          COMPLETED                             
  abort_reason   N/A                                   
  read_only      True                                  
  created_by     user@company.com              
  created_on     2024-05-09 19:26:09                   
  finished_at    2024-05-09 19:26:09                   
  duration       0.2s                                  
                                                       

---------------------------------------------------
```

If you do not provide the `--id` option, you are prompted to enter the ID interactively:

```sh
❯ rai transactions:get

---------------------------------------------------
 
? Transaction id: 01b439b2-0002-6941-0051-c0070498679a

▰▰▰▰ Transaction fetched   

                                                       
  Field          Value                                 
 ───────────────────────────────────────────────────── 
  id             01b439b2-0002-6941-0051-c0070498679a  
  database       myModel                               
  state          COMPLETED                             
  abort_reason   N/A                                   
  read_only      True                                  
  created_by     david.amos@relational.ai              
  created_on     2024-05-09 19:26:09                   
  finished_at    2024-05-09 19:26:09                   
  duration       0.2s                                  
                                                       

---------------------------------------------------
```

If you do not know the ID of the transactions, you can list all transactions using the [`transactions:list`](./transactions_list.md) command.
Transaction IDs are also visible in the [debugger](./debugger.md).

## See Also

[`transactions:list`](./transactions_list.md),
[`transactions:cancel`](./transactions_abort.md).


# RelationalAI Engine FAQ

## How are concurrent workloads handled by an engine?

Engines are the primary mechanism for performance isolation.
Load balancing across engines is not automatic, so you retain control over each engine's workload.

As a general rule, all workloads executing concurrently against the same engine affect each other in some way.
Use separate engines whenever you want to avoid different users having to coordinate their usage.

To illustrate, let's say two developers A and B are working on separate [models](../api_reference/python/Model/README.md),
but both are using the same engine.
Now A loads a large amount of test data.
While the load is ongoing, B will see their model changes spinning.
Then say B introduces an error into their model, unintentionally causing a very expensive, unconstrained computation.
As this happens, A will suddenly experience performance degradation.

An engine can queue up to 128 transactions, and this limit is currently not configurable.
Queued transactions follow a first-in/first-out priority.
Engine failure cancels queued transactions by marking their status as `ABORTED` with the reason  `'engine failed'`.
A full queue rejects new transactions, returning [HTTP error 429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429).

Each engine, regardless of size, can concurrently execute up to 8 transactions.
Currently, this limit is non-configurable.
High-resource transactions will be serialized.
For executing large graph algorithms, we recommend sequential execution or using separate engines.

All writes to a RelationalAI database on the _same engine_ are serialized and concurrent writes are queued.
For concurrent writes to the same database _across engines_, only one commits, while others must retry.
Avoid writing to the same database from different engines.

## How can I tell if I need more engines?

Use the[RelationalAI CLI](../api_reference/cli/README.md) to check the status of your transactions:

```sh
rai transactions:list
```

If you see transactions sitting in the queued state for any significant amount of time, then the engine has reached its concurrency limit.
Reduce the number of concurrent transactions or redirect some load to an idle engine to free up the engine's CPU.
If you see transactions sitting in the waiting state, then the engine does not have enough memory or IO capacity available to make progress on them.
Cancel the affected transactions and rerun them against an idle engine.
Finally, if transactions sit in the created state, then no engine has been able to even accept them.
This likely means that all available engines are overloaded.

## What are the best practices for creating and using engines?

For large inputs, graph algorithms generally aim to utilize all resources on an engine.
Run at most one large scale graph algorithm per engine at a time.

Each active Snowflake schema requires memory on an engine.
Avoid interacting with more than two or three schemas through a single engine at a time.
Always prefer working with the same engine on the same schema and avoid mixing, as juggling too many active schemas will degrade engine performance.

Billing is based on engine run-time, not usage.
To minimize costs, shut down your engine when not in use.
However, frequent restarts incur warm-up costs, both financial and in terms of performance.
You may want to keep an engine running if you expect to use it again soon.
In the future, policies for automated cost management will be provided.

Engines responsible for maintaining streams from Snowflake to RelationalAI should be kept running
to ensure that changes to your Snowflake tables are available right away.
If you do shut down a stream's engine, changes to the data are synced when the engine is restarted.

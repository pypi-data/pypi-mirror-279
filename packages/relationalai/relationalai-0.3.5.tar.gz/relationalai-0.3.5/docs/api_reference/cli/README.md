<!-- markdownlint-disable MD024 -->

# RelationalAI CLI Reference

The RelationalAI Command Line Interface (CLI) is used to initialize RelationalAI projects and manage project resources.

## Installation

The CLI is bundled with the RelationalAI Python Package.
See [Install the `relationalai` Python Package](../../getting_started.md#install-the-relationalai-python-package) for details.

## Basic Usage

The CLI is invoked using the `rai` command.
Execute `rai` without any arguments to see a list of all available commands:

```sh
rai
```

> [!IMPORTANT]
> If you encounter the error `command not found: rai`, you may need to activate your project's virtual environment.

To execute a command, type `rai`, followed by the command name and any arguments you want to pass.
For example, the following creates a new RelationalAI engine named `my-engine` of size `S`:

```sh
rai engines:create --name my-engine --size S
```

To view help for a command, use the `--help` flag:

```sh
rai engines:create --help
```

## Commands

- [`init`](./init.md) - Initialize a new project.
- [`version`](./version.md) - Print version info.
- [`debugger`](./debugger.md) - Open the RAI debugger.
  
### Configuration and Profiles

All RelationalAI projects require a [configuration file](../configuration/README.md),
created using [`rai init`](./init.md),
that specifies the project's settings, platform credentials, and other configuration options.

Use the following commands to manage your project's configuration and profiles:

- [`config:explain`](./config_explain.md) - Inspect config status.
- [`config:check`](./config_check.md) - Check whether config is valid.
- [`profile:switch`](./profile_switch.md) - Switch to a different profile.

### Engines

Engines are the compute resources used to run queries and models.
Use the following commands to manage engines:

- [`engines:list`](./engines_list.md) - List all engines.
- [`engines:get`](./engines_get.md) - Get engine details.
- [`engines:create`](./engines_create.md) - Create a new engine.
- [`engines:delete`](./engines_delete.md) - Delete an engine.

### Imports

Imports are objects imported into RAI, such as data from a Snowflake table, for use in models and queries.
Use the following commands to manage imports:

- [`imports:list`](./imports_list.md) - List objects imported into RAI.
- [`imports:snapshot`](./imports_snapshot.md) - Load an object once into RAI (Azure only).
- [`imports:stream`](./imports_stream.md) - Stream an object into RAI (Snowflake only).
- [`imports:delete`](./imports_delete.md) - Delete an import from RAI.

### Exports

Exports are objects that are exported out of RAI for use in other systems,
such as exporting query results into a Snowflake table.
Use the following commands to manage exports:

> [!NOTE]
> This feature is currently disabled but will be available soon!

- [`exports:list`](./exports_list.md) - List objects exported out of RAI (Snowflake only).
- [`exports:delete`](./exports_delete.md) - Delete an export from RAI (Snowflake only).

### Transactions

Transactions are operations that modify the state of a RelationalAI model.
They are created when you import data and when you run queries.
Use the following commands to manage transactions:

- [`transactions:list`](./transactions_list.md) - List all transactions.
- [`transactions:get`](./transactions_get.md) - Get transaction details.
- [`transactions:cancel`](./transactions_cancel.md) - Cancel a transaction.

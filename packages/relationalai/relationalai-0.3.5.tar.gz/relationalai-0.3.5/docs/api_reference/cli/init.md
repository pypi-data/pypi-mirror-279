# `init`

```sh
rai init
```

Initialize a new project and create a `raiconfig.toml` file.

## Example

`rai init` walks you through setting up a RelationalAI project, connecting to a cloud platform,
and saving a `raiconfig.toml` [configuration file](../configuration/README.md):

```sh
$ rai init

---------------------------------------------------

Welcome to RelationalAI!

Press Control-S to skip a prompt

? Host platform: 
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│❯   2/2                                                                                                                                   │
│❯ Snowflake                                                                                                                               │
│  Azure (Beta)                                                                                                                            │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

When you run `rai init`, you are prompted to select a cloud platform and provide connection information,
as well as select or create the RelationalAI engine to use for executing transactions.

> [!NOTE]
> If a `raiconfig.toml` with a [profile](../configuration/README.md#profiles) for the chosen platform
> exists in your project directory, you are given the option to select the existing profile.
> This profile's values are then suggested as defaults in subsequent prompts for editing or reusing in a new profile.

### Initialize a Snowflake Project

Select `Snowflake` from the host platform prompt to connect to a Snowflake account and create a new project.
You are prompted to enter your Snowflake username and password:

```sh
? Host platform: Snowflake
? SnowSQL user: user@example.com
? SnowSQL password: ********************
```

After entering your Snowflake credentials, you are prompted to enter
the [account identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier)
of the Snowflake account your project will use:

```sh
  Note: Account ID should look like: myorg-account123
  Details: https://docs.snowflake.com/en/user-guide/admin-account-identifier

  Alternatively, you can log in to Snowsight, copy the URL, and paste it here.
  Example: https://app.snowflake.com/myorg/account123/worksheets

? Snowflake account: myorg-account123
```

The account identifier has the format `<orgname>-<account_name>`, where:

- `<orgname>` is the name of your Snowflake organization.
- `<account_name>` is the unique name of your Snowflake account.

If you have trouble finding your account identifier,
log in to Snowsight and copy the URL from the address bar into the prompt.
The account identifier will be inferred from the URL.

Next, you are prompted to select the Snowflake role, warehouse, and RelationalAI Native App instance to use with your project:

```sh
▰▰▰▰ Fetched roles   

? Select a role: 
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│❯   3/3                                                                                                                                 │
│  [REFETCH LIST]                                                                                                                          │
│❯ ACCOUNTADMIN                                                                                                                            │
│  USER                                                                                                                                    │
│  PUBLIC                                                                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Fetched warehouses   

? Select a warehouse: 
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│❯   1/1                                                                                                                                   │
│  [REFETCH LIST]                                                                                                                          │
│❯ MY_WAREHOUSE                                                                                                                            |
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

▰▰▰▰ Fetched apps   

? Select RelationalAI app name: 
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│❯   1/1                                                                                                                                   │
│  [REFETCH LIST]                                                                                                                          │
│❯ MY_RAI_NATIVE_APP                                                                                                                       │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Use the up and down arrow keys to navigate the list of roles, warehouses, and apps.
Press `Enter` to make a selection.
You may filter the list by typing the name of the role, warehouse, or app you want to select.
Select `[REFETCH LIST]` to refresh the list.

Finally, you are prompted to select the RelationalAI engine to use with your project:

```sh
▰▰▰▰ Fetched engines   

? Select an engine: 
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│❯   7/7                                                                                                                                   │
│  [REFETCH LIST]                                                                                                                          │
│  [CREATE A NEW ENGINE]                                                                                                                   │
│❯ my_engine                                                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Select `[CREATE A NEW ENGINE]` to create a new engine if the engine you want to use is not listed.
The flow for creating an engine is the same as the flow for the [`rai engines:create`](./engines_create.md) command.

After selecting an engine, the configuration settings are saved in a `raiconfig.toml` file in the current directory.
If a `raiconfig.toml` file already exists in the current directory,
you are prompted to overwrite any existing profiles or save the new settings as a new named profile
and asked if you want to activate the new profile:

```sh
? Overwrite existing profile No

? Profile name: my_profile

? Activate this profile? Yes

✓ raiconfig.toml saved!
```

You can verify that your connection settings are valid by running the [`rai config:check`](./config_check.md) command:

```sh
$ rai config:check

---------------------------------------------------
 
▰▰▰▰ Connection successful!              

---------------------------------------------------
```

### Initialize an Azure Project

Select `Azure (Beta)` from the host platform prompt to connect to an Azure account and create a new project.
You are prompted to enter your RelationalAI OAuth client ID and client secret:

```sh
? Host platform: Azure (Beta)
? Client ID: <RELATIONALAI_CLIENT_ID>
? Client Secret: ****************************************************************
```

Next, you are prompted to select or create a RelationalAI engine to use with your project:

```sh
▰▰▰▰ Fetched engines   

? Select an engine: 
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│❯   7/7                                                                                                                                   │
│  [REFETCH LIST]                                                                                                                          │
│  [CREATE A NEW ENGINE]                                                                                                                   │
│❯ my_engine                                                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Select `[CREATE A NEW ENGINE]` to create a new engine if the engine you want to use is not listed.
The flow for creating an engine is the same as the flow for the [`rai engines:create`](./engines_create.md) command.

After selecting an engine, the configuration settings are saved in a `raiconfig.toml` file in the current directory.
If a `raiconfig.toml` file already exists in the current directory,
you are prompted to overwrite any existing profiles or save the new settings as a new named profile
and asked if you want to activate the new profile:

```sh
? Overwrite existing profile No

? Profile name: my_profile

? Activate this profile? Yes

✓ raiconfig.toml saved!
```

You can verify that your connection settings are valid by running the [`rai config:check`](./config_check.md) command:

```sh
$ rai config:check

---------------------------------------------------
 
▰▰▰▰ Connection successful!              

---------------------------------------------------
```

## See Also

[`config:check`](./config_check.md) and [`config:explain`](./config_explain.md).

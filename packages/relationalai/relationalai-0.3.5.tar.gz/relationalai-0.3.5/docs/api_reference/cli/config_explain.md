# `config:explain`

```sh
rai config:explain [OPTIONS]
```

Inspect configuration status.

## Options

| Option | Type | Description |
| :------ | :--- | :--------- |
| `--profile` | Text | The profile to inspect. If missing, the active profile is used. |
| `--all-profiles` | | Inspect all profiles. If missing, only the profile specified by the `--profile` option is inspected. |

## Example

Use the `config:explain` command to inspect the configuration status of the active profile:

```sh
$ rai config:explain

---------------------------------------------------
 
/path/to/raiconfig.toml

[default]
platform = snowflake
user = user@company.com
password = ************
account = <SNOWFLAKE_ACCOUNT_NAME>
role = <SNOWFLAKE_ROLE_NAME>
warehouse = <SNOWLAKE_WAREHOUSE_NAME>
rai_app_name = <RAI_NATIVE_APP_NAME>
engine = <ENGINE_NAME>

---------------------------------------------------
```

Sensitive information, such as your password, is redacted in the output.

If your [configuration file](../configuration/README.md) has multiple profiles,
you can use the `--profile` option to inspect a specific profile:

```sh
rai config:explain --profile my-profile
```

To inspect all profiles in the configuration file, use the `--all-profiles` option:

```sh
rai config:explain --all-profiles
```

Missing information is indicated by a question mark (`?`).
The following output indicates that the `password` and `engine` fields are missing:

```sh
$ rai config:explain

---------------------------------------------------
 
/path/to/raiconfig.toml

[default]
platform = snowflake
user = user@company.com
account = <SNOWFLAKE_ACCOUNT_NAME>
role = <SNOWFLAKE_ROLE_NAME>
warehouse = <SNOWLAKE_WAREHOUSE_NAME>
rai_app_name = <RAI_NATIVE_APP_NAME>
password = ?
engine = ?

---------------------------------------------------
```

## See Also

[`config:check`](./config_check.md) and [`profile:switch`](./profile_switch.md).

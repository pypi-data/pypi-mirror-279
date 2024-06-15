# `config:check`

```sh
rai config:check
```

Check whether the configuration is valid.

## Example

Use the `config:check` command to check whether the currently activated configuration profile is valid.
If the configuration is missing required fields, the command will return an error message:

```sh
$ rai config:check

---------------------------------------------------
 
▰▱▱▱ Connecting to platform...

Error: Missing config value for 'password'

---------------------------------------------------
```

If all required fields are present, the command attempts to connect to the platform using the provided credentials.
If the connection succeeds, the command returns a success message:

```sh
$ rai config:check

---------------------------------------------------
 
▰▰▰▰ Connection successful!              

---------------------------------------------------
```

If the connection is unsuccessful, the command displays an error message with details about the failure:

```sh
$ rai config:check

---------------------------------------------------
 
▱▱▰▰ Connecting to platform...

Error: 250001 (08001): Failed to connect to DB: 
my-swnoflake-account.snowflakecomputing.com:443. Incorrect username
or password was specified.

---------------------------------------------------
```

## See Also

[`config:explain`](./config_explain.md) and [`profile:switch`](./profile_switch.md).
# `profile:switch`

```sh
rai profile:switch [OPTIONS]
```

Switch to a different profile.

## Options

| Option | Type | Description |
| :------ | :--- | :--------- |
| `--profile` | Text | The profile to switch to. If missing, you are prompted to select the profile interactively. |

## Example

Use the `profile:switch` command to switch the active profile to a different profile.
For example, to switch to the profile named `my-profile`, execute the following command:

```sh
$ rai profile:switch --profile my-profile

---------------------------------------------------
 
✓ Switched to profile 'my-profile'

---------------------------------------------------
```

If no profile named `my-profile` exists in the configuration file, an error message is displayed:

```sh
$ rai profile:switch --profile my-profile

---------------------------------------------------
 
Profile 'my-profile' not found

---------------------------------------------------
```

If the `--profile` option is missing, you are prompted to select the profile interactively.
In the following example, there are three profiles in the configuration file named `dev`, `prod`, and `test`,
and the user selects the `test` profile:

```sh
$ rai profile:switch

---------------------------------------------------
 
? Select a profile: 
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│❯   3/3                                                                                   │
│  dev                                                                                     │
│  prod                                                                                    │
│❯ test                                                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────┘

---------------------------------------------------
 
✓ Switched to profile 'test'

---------------------------------------------------
```

Use the up and down arrow keys to navigate the list of profiles.
You may search for a profile by typing the profile name in the prompt.

## See Also

[`config:explain`](./config_explain.md) and [`config:check`](./config_check.md).

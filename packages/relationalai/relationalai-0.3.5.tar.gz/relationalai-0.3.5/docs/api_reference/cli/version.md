# `version`

```sh
rai version
```

Print version info.

## Example

Use the `version` command to display the version info for your project's dependencies:

```sh
$ rai version

---------------------------------------------------
 
                                          
  RelationalAI   0.2.5 → 0.2.7      
  Rai-sdk        0.7.5              
  Python         3.12.1             
  App            2024.5.8-a1b26cea  
                                    

---------------------------------------------------
```

Outdated dependencies are highlighted in red and marked with an arrow pointing to the latest version.
If your current Python version is supported, it will be displayed in green, even if it is not the latest version.

> [!NOTE]
> The App version is the version of the RelationalAI Snowflake Native App that is installed on your Snowflake account.
> Azure-based projects will not display an App version.
> If your Snowflake Native App is outdated, contact your Snowflake administrator to update it.

To update the `relationalai` and `rai-sdk` Python packages to the latest versions,
active your project's virtual environment and run the following command:

```sh
python -m pip install --upgrade relationalai rai-sdk
```

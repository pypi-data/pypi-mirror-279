# HongXiongMao Refuel

Toolbox for importing data from various financial sources; 
for a personal project so if you are here by accident I highly advise you look elsewhere.

## Usage
There are no plans to go into any material depth here, so these are just notes to job my own memory. 

### Snowflake
Snowflake objects here specifically related to the snowflake-connector so connecting to a database. 
There are three main functions.
`rsa_token_stuff` which returns pkb given a password string and private_key_file.p8
`snowflake_connect` which returns a snowflake-python-connector connection, 
`snowflake_sql_engine` returns an SQL Alchemy engine object. 
Not being a database pro, both seem to work but I favour the engine. 

Both functions require the same inputs:
```
def snowflake_sql_engine(
    user_details: dict,                     # dictionary of required inputs
    method='rsa',                           # can be 'rsa' or 'user' 
    password: None | str = None,            # password if using rsa
    private_key_file: None | str = None     # file location of .p8 file if using RSA
    ):
```

To help there are also templates for the user_details:

```
SNOWFLAKE_RSA_USER_DETAILS_TEMPLATE = dict(
    user="USERNAME",
    password="",
    account="xx123455",
    region="eu-west-1",
    warehouse="LAB_SOMETHING_WH",
    database="LAB_SOMETHING",
    # schema="",)
```

As well as some helper functions
`check_compatibility` tests a df vs. a snowflake table for compatability (could be a bit buggy)
`sql_append_with_drop_duplicates` does as it says on the tin

## Installation 

### Bloomberg API
To make Bloomberg calls, the `blpapi` package must be installed; we then extend the excellent `xbbg` package. 
Unfortunately, installing of `blpapi` can be a pain in the backside.
I can't get `pyproject.toml` to correctly install `blpapi` as a dependency.

Using pip instruction from [the Bloomberg website](https://www.bloomberg.com/professional/support/api-library/)

```
python -m pip install --index-url=https://bcms.bloomberg.com/pip/simple blpapi
```

Poetry [requires 2 steps](https://github.com/python-poetry/poetry/issues/7587)
1. Set up Bloomberg as a source,
2. installing `blpapi`

```
poetry source add --priority=supplemental bloomberg https://bcms.bloomberg.com/pip/simple/
poetry add --source bloomberg blpapi
```

### Snowflake SQL
In order to get snowflake connectors working we've had to install several additional packages. 
Snowflake is very picky about which versions of pyarrow etc... are installed and requires old versions.
```
snowflake-connector-python = "^3.2.0"
snowflake-sqlalchemy = "^1.5.0"
pyarrow = ">=10.0.1, <10.1.0"
cryptography = "^41.0.5"
```

## Publishing to PyPi
I'm no pro at deploying packages to PyPi, so these are my notes for deployment of a poetry package. 
For reference, I followed 
[this tutorial](https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04)

Key points:
* (PyPi account is required)[https://pypi.org/manage/account/#account-emails]
* (Configure Poetry)[https://python-poetry.org/docs/repositories/#configuring-credentials]
* poetry build
* poetry publish

```
# configure API key
poetry config pypi-token.pypi <pypi-reallyREALLYllongKEY...>

# The build bit
(base) (hxm-refuel-py3.10) PS C:\Users\XXX\Documents\GitHub\hxm-refuel> poetry build

Building hxm-refuel (0.1.0)
  - Building sdist
  - Built hxm_refuel-0.1.0.tar.gz
  - Building wheel
  - Built hxm_refuel-0.1.0-py3-none-any.whl

# publishing bit
(base) (hxm-refuel-py3.10) PS C:\Users\T333208\Documents\GitHub\hxm-refuel> poetry publish

Publishing hxm-refuel (0.1.0) to PyPI
 - Uploading hxm_refuel-0.1.0-py3-none-any.whl 0%
 - Uploading hxm_refuel-0.1.0-py3-none-any.whl 85%
 - Uploading hxm_refuel-0.1.0-py3-none-any.whl 100%
 - Uploading hxm_refuel-0.1.0.tar.gz 0%
 - Uploading hxm_refuel-0.1.0.tar.gz 100%
```

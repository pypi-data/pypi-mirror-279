""" Snowflake Connection Stuff """
import warnings

# Snowflake connection stuff
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import snowflake.connector as connector

# for RSA token initialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


SNOWFLAKE_RSA_USER_DETAILS_TEMPLATE = dict(
    user="USERNAME",
    password="",
    account="xx123455",
    region="eu-west-1",
    warehouse="LAB_SOMETHING_WH",
    database="LAB_SOMETHING",
    # schema="",
)

SNOWFLAKE_BROWSER_LOGIN_TEMPLATE = dict(
    user="first.last@domain.org",
    password="",
    authenticator = "externalbrowser",
    account="xx123455",
    region="eu-west-1",
    warehouse="LAB_SOMETHING_WH",
    database="LAB_SOMETHING",
    # schema="",
)


def rsa_token_stuff(password: str, private_key_file="rsa_key.p8"):
    """ Create RSA Tokens

    For RSA we require 2 things:
        1. a password, which is a string and should be private saved in os.env or whatever
        2. a private key, which is a .p8 file and wil have a form like below

            -----BEGIN ENCRYPTED PRIVATE KEY-----
            MIIFHzBJBgkqhkiG9w0BBQ0wPDAbBgkqhkiG9w0BBQwwDgQIxIoCnzcfizcCAggA
            BUTthisLINEwillGOonFOR20or30linesOFnonsense!Basdgers&WeaselsROCK
            -----END ENCRYPTED PRIVATE KEY-----

    INPUTS:
        password: str: something of the form "pleasechangemepassphraseZXCs1234"
        private_key_file: str: file path to "rsa_key.p8" file
    """

    assert isinstance(private_key_file, str), f"private key file needs to be a string: {type(private_key_file)}"

    with open(private_key_file, "rb") as key:
        p_key = serialization.load_pem_private_key(
            key.read(),
            password=password.encode('utf-8'),
            backend=default_backend(),
        )

        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    return pkb


def snowflake_asserts(user_details, method, password, private_key_file, raw):
    """ Assertions for Snowflake Connect & SQL Engine """

    assert method in ['rsa', 'user'], "supplied method must either be rsa or user"
    assert isinstance(user_details, dict), f"user details must be supplied as dictionary: {type(user_details)} provided"
    assert isinstance(raw, bool), f"raw must be boolean: {type(raw)}"

    # check all the keys from the RSA template are in the user_details
    for k in SNOWFLAKE_RSA_USER_DETAILS_TEMPLATE.keys():
        assert k in user_details.keys(), f"user_details dict is missing: {k} as a required field"

    if method == 'user':
        assert "authenticator" in user_details.keys(), \
            f"""user_details dict is missing: authenticator as a required field. 
            Possible you used the RSA template rather than the browser login template."""

    if method == "rsa":
        assert isinstance(password, str), "using an RSA key a password str must be provided"
        assert isinstance(private_key_file, str), "using an RSA key, private_key_file path must be provided as str"


def snowflake_connect(
        user_details: dict,
        method='rsa',
        password: None | str = None,
        private_key_file: None | str = None,
        raw: bool = False):
    """ Connection to Snowflake via Snowflake-Connector-Python"""
    snowflake_asserts(**locals())
    if method == 'rsa':
        pkb = rsa_token_stuff(password, private_key_file)
        return connector.connect(
            private_key=pkb, **user_details, client_session_keep_alive=True)
    else:
        return connector.connect(**user_details, client_session_keep_alive=True)


def snowflake_sql_engine(
        user_details: dict,
        method='rsa',
        password: None | str = None,
        private_key_file: None | str = None,
        raw: bool = False):
    """
    Connection via the SQL Alchemy Engine Method

    Parameters:
        raw: bool == False: outputs engine.raw_connection() object

    """
    snowflake_asserts(**locals())
    if method == 'rsa':
        pkb = rsa_token_stuff(password, private_key_file)
        engine = create_engine(URL(**user_details), connect_args={'private_key': pkb})
    else:
        engine = create_engine(URL(**user_details))

    # there was a change in SQL Alchemy
    if raw:
        return engine.raw_connection()
    else:
        warnings.warn(f"""
        hxm-refuel warning: there is a change to SQL Alchemy meaning we need to specify a connect() or raw_connection()
        lots of packages have been refactored to convert a engine already; 
        in the future we will set the raw default == True 
        """)
        return engine


# quick run
if __name__ == '__main__':

    #
    import os
    HOME = os.path.expanduser('~')
    print(HOME)

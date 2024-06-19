import os

import dotenv
from dotenv import load_dotenv
from qcaas_common.logger import get_logger

log = get_logger(__name__)


def pytesting() -> bool:
    "Is the system being tested by pytest?"
    return "PYTEST_CURRENT_TEST" in os.environ


def load_env_file_if_exists(env_file: str = ".env", secrets_envfile=".env.secrets"):
    # Load env file if it exists, env_file name/path relational from the qcaas package
    # root folder.
    abs_secrets_envfile = dotenv.find_dotenv(secrets_envfile, usecwd=True)
    if not pytesting():
        loaded_secrets = dotenv.load_dotenv(abs_secrets_envfile, override=True)
        if loaded_secrets:
            keys = dotenv.dotenv_values(abs_secrets_envfile).keys()
            print(f"ENV.SECRETS: {abs_secrets_envfile} loaded with keys:")
            print(", ".join(keys))
        else:
            print(f"no {abs_secrets_envfile} file/values found")

    if os.path.isabs(env_file):
        env_path = env_file
    else:
        env_path = os.path.join(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
            ),
            env_file,
        )
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path)
        log.info(f"Loaded env file from '{env_path}'.")
    else:
        log.info(f"Couldn't find env file at '{env_path}'. Not loading")

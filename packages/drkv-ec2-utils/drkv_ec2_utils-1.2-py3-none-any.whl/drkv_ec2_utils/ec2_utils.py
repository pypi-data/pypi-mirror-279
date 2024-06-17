"""Module providing utility functions."""

import logging
import sys
import functools
from typing import Dict, Tuple
import boto3
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Common constants
PROCESS_ID = "process_id"
INTENDED_STATE = "intended_state"
COMMAND_ID = "CommandId"

# Cryptographic constants
ENCRYPTION_KEY = "encryption_key"
ENCRYPTION_IV = "encryption_iv"
ENCODING_SCHEME = "utf-8"

# AWS constants
SECRETS_MANAGER = "secretsmanager"
SSM = "ssm"

# System config constants
SYSTEM_CONFIGS = [PROCESS_ID, ENCRYPTION_IV, ENCRYPTION_KEY, INTENDED_STATE, COMMAND_ID]


class Ec2Utils:

    def __init__(self, profile_name=False, region_name="eu-central-1"):
        self.profile_name = profile_name
        self.region_name = region_name
        self.logger = self.initiate_logging(__name__)

    def initiate_logging(self, name, level=None):
        """
        Create an object for logging

        :param name: class name from where logging object invoked
        :param level: logging levels ex: WARNING, DEBUG, INFO etc

         For more log level refer to the below link
         https://docs.python.org/3/library/logging.html#levels

        :return: logger object
        """
        logger = logging.getLogger(name)
        if hasattr(logger, "logger_handler_initiated"):
            return logger
        level = level or "DEBUG"
        logger.setLevel(level)
        return self.prepare_logger(logger, level)

    def prepare_logger(self, logger, level):
        """Handler to get an output of function and default to sys.stderr"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        logger.propagate = False

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.logger_handler_initiated = True
        return logger

    def exception_handler(self, logger=None):
        """Decorator to handle exception"""

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                except Exception as ex:
                    message = (
                        f"Exception : {type(ex).__name__} was raised: {ex} during "
                        f"calling {func.__name__}"
                    )
                    logger.exception(message)
            return wrapper

        return decorator

    def get_aws_client(self, service_name):
        """Function to create AWS services clients"""
        profile_name = self.profile_name
        session = boto3.Session(profile_name=profile_name) if profile_name else boto3.Session()
        client = session.client(
            service_name=service_name,
            region_name=self.region_name,
        )
        return client

    def get_config(self, secret_id, key) -> Dict[str, str]:
        """Function to get parameter from parameter store"""
        try:
            ssm_client = self.get_aws_client(SSM)
            response = ssm_client.get_parameter(Name=f"/{secret_id}/{key}")
            return response["Parameter"]["Value"]
        except Exception as exception:
            self.logger.exception("Exception in get config : %s", str(exception))
            return None

    def set_config(self, secret_id, key, val):
        """Function to set parameter in parameter store"""
        try:
            ssm_client = self.get_aws_client(SSM)
            if not val:
                val = " "
            name = f"/{secret_id}/{key}"
            ssm_client.put_parameter(Name=name, Value=val, Type="String", Overwrite=True)
            return True
        except Exception as exception:
            self.logger.exception("Exception in set config : %s", str(exception))
            return False

    def get_configs(self, secret_id):
        """Function to get parameters from parameter store"""
        try:
            client = self.get_aws_client(SSM)
            parameter_list = {}
            paginator = client.get_paginator("get_parameters_by_path")
            iterator = paginator.paginate(
                Path=f"/{secret_id}/", WithDecryption=True, Recursive=True
            )

            for page in iterator:
                for param in page.get("Parameters", []):
                    parameter_list[param.get("Name")] = param.get("Value")

            parameter_list = self.filter_system_config(parameter_list)
            return parameter_list
        except Exception as exception:
            self.logger.exception("Exception in get configs : %s", str(exception))
            return None

    def get_trader_credential(self, secret_id) -> Tuple[int | None, str | None]:
        """Function to get secrets from secret manager"""
        try:
            sm_client = self.get_aws_client(service_name=SECRETS_MANAGER)

            response = sm_client.get_secret_value(SecretId=secret_id)
            self.logger.info(response["SecretString"])
            secrets = response["SecretString"]
            secrets = json.loads(secrets.replace("'", '"'))
            password = self.get_decrypted_password(secret_id, secrets["password"])
            return int(secrets["username"]), password
        except Exception as exception:
            self.logger.exception("Exception in get trader credential : %s", str(exception))
            return None, None

    def get_decrypted_password(self, secret_id, password):
        """Function to get decryption data from parameter store and decode password"""
        encryption_key = self.get_config(secret_id, ENCRYPTION_KEY)
        encryption_iv = self.get_config(secret_id, ENCRYPTION_IV)
        encryption_iv = encryption_iv.encode(ENCODING_SCHEME)
        password = base64.b64decode(password)
        cipher = AES.new(
            encryption_key.encode(ENCODING_SCHEME), AES.MODE_CBC, encryption_iv
        )
        password = unpad(cipher.decrypt(password), 16)
        return password.decode(ENCODING_SCHEME, "ignore")

    def filter_system_config(self, parameter_list):
        """Function to filter all system config from user defined config"""
        return {
            key.split("/")[-1]: val
            for key, val in parameter_list.items()
            if key.split("/")[-1] not in SYSTEM_CONFIGS
        }

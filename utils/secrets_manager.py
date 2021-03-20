"""
Secrets Manager's keys handler
"""
import base64
import json
import os

import boto3  # pylint: disable=import-error
from botocore.exceptions import ClientError


class SecretsManager(dict):
    """The main secrets manager handler implementation"""

    def __init__(self, region="eu-central-1"):
        session = boto3.session.Session()
        self.client = session.client(
            service_name="secretsmanager", region_name=region
        )

    def __getitem__(self, attr):
        """Retrieve key value from the dictionary or from Secrets Manager

        Arguments:
            attr {str} -- Key name

        Raises:
            e: Botocore Client exception

        Returns:
            [dict] -- Key/Value dictionary
        """
        if attr in self.__dict__:
            return self.__dict__[attr]

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=os.environ[attr]
            )
        except ClientError as e:
            raise e

        if "SecretString" in get_secret_value_response:
            response = json.loads(get_secret_value_response["SecretString"])
        else:
            response = base64.b64decode(
                get_secret_value_response["SecretBinary"]
            )

        response_item = response

        self.__setitem__(attr, response_item)

        return response_item

    def __setitem__(self, attr, value):
        self.__dict__[attr] = value

    def update_secret_keys(self, attr, obj):
        """Updates secret values on Secrets Manager
        - If the secret name is a binary string,
            the old value will be overwritten;
        - If the secret name is a collection of keys and values,
            the two values are merged,
            new keys will take precedence over old keys;
        - Otherwise, TypeError is raised.

        Arguments:
            attr {str} -- Environment variable name which contains secrets manager key name
            obj {dict} -- New values

        Raises:
            TypeError

        Returns:
            dict - Boto execution result
        """

        if type(obj) == dict:
            self.__dict__[attr].update(obj)

            return self.client.update_secret(
                SecretId=os.environ[attr],
                SecretString=json.dumps(self.__dict__[attr]),
            )
        else:
            raise TypeError("Only dict is supported.")

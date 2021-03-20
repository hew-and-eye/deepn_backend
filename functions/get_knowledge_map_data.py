import boto3
import uuid
from json import loads

from functions.get_user import handler as get_user

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_USERS"


def handler(event, context):
    name = event["body"]["name"]
    return {name : "hello {}".format(name)}


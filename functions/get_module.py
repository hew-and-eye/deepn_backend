import boto3
import uuid
from json import loads
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client("dynamodb")
TASK_TABLE_NAME = "DEEPN_MODULES"
ACCESS_TABLE_NAME = "DEEPN_ACCESS_RIGHTS"


def handler(event, context):
    
    
    return {name : "hello"}


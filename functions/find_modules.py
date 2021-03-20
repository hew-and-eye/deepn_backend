import boto3
import uuid
from json import loads
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client("dynamodb")
MODULES_TABLE_NAME = "DEEPN_MODULES"

def handler(event, context, include_password=False):
    try:
        response = dynamodb.scan(
            TableName=MODULES_TABLE_NAME,
            Select='ALL_ATTRIBUTES'
            )
        result = _get_formatted_modules(response["Items"])
    except Exception as e:
        print("Error while getting find_modules", e, event)
        result = {
            "error": str(e)
        }
    return result

def _format(value, type="S"):
    return {type: value}

def _get_formatted_modules(modules):
    print("some modules", modules)
    return [
        {
            "id": x["id"]["S"] if x.get("id") else "",
            "name": x["name"]["S"] if x.get("name") else "",
            "dependencies": x["dependencies"]["M"] if x.get("dependencies") else "",
            "templates": x["templates"]["S"] if x.get("templates") else "",
            "owner": x["owner"]["S"] if x.get("owner") else "",
            "reactions": x["reactions"]["S"] if x.get("reactions") else "",
        }
        for x in modules
    ]


import boto3
import uuid
import json

from functions.share_task import handler as share_task

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_MODULES"


def handler(event, context):
    try:
        body = event.get("body")
        id = str(uuid.uuid4())
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
            "id": _format(id),
            "name": _format(body['name']),
            "dependencies": dict_to_item(body['dependencies']),
            "templates": _format(body['templates']),
            "owner": _format(body['owner']),
            "reactions": _format(body['reactions'])
            },
        )
        result = {
            "success": True,
            "result": {
                "id": id,
                "name": _format(body['name']),
            },
        }
    except Exception as e:
        print("Error while creating module:", e, event)
        result = {"error": str(e), "event": event}
    return result


def _format(value, type="S"):
    if isinstance(value, dict):
        return {type: json.dumps(value)}
    elif isinstance(value, str):
        return {type: value}

def dict_to_item(raw):
    if isinstance(raw, dict):
        return {
            'M': {
                k: dict_to_item(v)
                for k, v in raw.items()
            }
        }
    elif isinstance(raw, list):
        return {
            'L': [dict_to_item(v) for v in raw]
        }
    elif isinstance(raw, str):
        return {'S': str(raw)}
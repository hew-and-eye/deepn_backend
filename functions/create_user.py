import boto3
import uuid
from json import loads

from functions.get_user import handler as get_user

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_USERS"


def handler(event, context):
    try:
        event["body"]["username"] = event["body"]["username"].lower()
        existing_user = get_user(event, context)
        if existing_user.get("results"):
            raise Exception("User already exists")
        elif existing_user.get("error"):
            raise Exception(
                "Unable to create user - could not check for existing users",
                existing_user["error"],
            )
        body = event.get("body")
        id = str(uuid.uuid4())
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "id": _format(id),
                "org_id": _format("test_deepn_org"),
                "username": _format(body["username"]),
                "password": _format(
                    body["password"]
                ),  # All data in DDB is encryted at rest, so I'm not bothering with an additional encryption layer for now
            },
        )
        result = {
            "success": True,
            "result": {
                "id": id,
                "username": body["username"],
                "password": body["password"],
            },
        }
    except Exception as e:
        print("Error while creating user:", e, event)
        result = {"error": str(e), "event": event}
    return result


def _format(value, type="S"):
    return {type: value}

import boto3
import uuid

from functions.share_task import handler as share_task

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "MBL_TASKS"


def handler(event, context):
    try:
        body = event.get("body")
        id = str(uuid.uuid4())
        user_id = event["enhancedAuthContext"]["user_id"]
        shared_users = body.get("shared_users", [])
        print("before append", shared_users)
        shared_users.append({"id": user_id, "access_type": "edit"})
        print("after append", shared_users)
        shared_users = [
            {
                "M": {
                    "id": _format(x["id"]),
                    "access_type": _format(x["access_type"]),
                }
            }
            for x in shared_users
        ]
        print("ABOUT TO PUT ITEM", _format(shared_users, "L"))
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "id": _format(id),
                "user_id": _format(user_id),
                "description": _format(body.get("description", "")),
                "title": _format(body.get("title", "")),
                "shared_users": _format(shared_users, "L"),
            },
        )
        result = {
            "success": True,
            "result": {
                "id": id,
                "user_id": user_id,
                "title": body.get("title"),
                "description": body.get("description"),
                "shared_users": body.get("shared_users", []),
            },
        }
        if shared_users:
            print("GOING TO SHARE SOME USERS")
            share_task_event = {
                **event,
                "body": {
                    "users": _format(shared_users, "L"),
                    "task_id": _format(id),
                },
            }
            print("SHARED", share_task_event)
            share_result = share_task(share_task_event, context)
            result["share_result"] = share_result
    except Exception as e:
        print("Error while creating task:", e, event)
        result = {"error": str(e), "event": event}
    return result


def _format(value, type="S"):
    return {type: value}

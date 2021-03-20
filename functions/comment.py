import boto3
import uuid

from functions.share_task import handler as share_task

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_TASKS"


def handler(event, context):
    try:
        body = event.get("body")
        task_id = body["task_id"]
        comment = body["comment"]
        user_id = event["enhancedAuthContext"]["user_id"]
        full_task = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="id = :task_id",
            ExpressionAttributeValues={":task_id": _format(task_id)},
        )
        full_task = full_task.get("Items")[0]
        if not full_task.get("comments"):
            full_task["comments"] = _format([], "L")
        full_task["comments"]["L"].append(
            {"M": {"user_id": _format(user_id), "comment": _format(comment)}}
        )
        result = {"commented_task": full_task}
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item=full_task,
        )
        result = {"success": True}
    except Exception as e:
        print("Error while creating task:", e, event)
        result = {"error": str(e), "event": event}
    return result


def _format(value, type="S"):
    return {type: value}

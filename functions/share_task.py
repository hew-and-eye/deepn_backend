import boto3
import uuid
from json import loads

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "TEAMO_ACCESS_RIGHTS"


def handler(event, context):
    try:
        print("going to try to do share a task", event)
        print([x for x in event["body"]["users"]["L"]])
        request_items = [
            {
                "PutRequest": {
                    "Item": {
                        "user_id": x["M"]["id"],
                        "shared_by": _format(
                            event["enhancedAuthContext"]["user_id"]
                        ),
                        "access_type": x["M"]["access_type"],
                        "task_id": event["body"]["task_id"],
                    }
                }
            }
            for x in event["body"]["users"]["L"]
        ]

        for chunk in list(_chunks(request_items, 25)):
            print("going to batch write", chunk)
            dynamodb.batch_write_item(RequestItems={TABLE_NAME: chunk})
        result = {"success": True}
    except Exception as e:
        print("Error while sharing task:", e, event)
        result = {"error": "Error while sharing task"}
    return result


def _format(value, type="S"):
    return {type: value}


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst.

    Args:
        lst: list to get chunks from
        n: ???

    Yields:
        slice: slice of list
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

import boto3
import uuid
from json import loads
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client("dynamodb")
TASK_TABLE_NAME = "MBL_TASKS"
ACCESS_TABLE_NAME = "TEAMO_ACCESS_RIGHTS"


def handler(event, context, include_password=False):
    try:
        params = event.get("body")
        username = params.get("username")
        user_id = event["enhancedAuthContext"]["user_id"]
        if user_id:
            task_ids = dynamodb.query(
                TableName=ACCESS_TABLE_NAME,
                KeyConditionExpression="user_id = :user_id",
                ExpressionAttributeValues={":user_id": _format(user_id)},
                IndexName="UserId",
            )
        print("task find results", task_ids)
        task_ids = _get_formatted_task_ids(task_ids)
        print("going to query", _format(task_ids, "L"))
        expression_attribute_values = {}
        filter_expression = "#tid IN ("
        for index, tid in enumerate(task_ids):
            name = ":t" + str(index)
            expression_attribute_values[name] = _format(tid)
            if index:
                filter_expression += ", " + name
            else:
                filter_expression += name
        filter_expression += ")"
        additional_scan_args = {}
        exclusive_start_key = (
            {"id": _format(params["page_id"])}
            if params.get("page_id")
            else None
        )
        if exclusive_start_key:
            additional_scan_args["ExclusiveStartKey"] = exclusive_start_key
        tasks = dynamodb.scan(
            TableName=TASK_TABLE_NAME,
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames={"#tid": "id"},
            **additional_scan_args,
        )
        tasks["Items"] = _get_formatted_tasks(tasks["Items"])
        next_page_id = tasks["Items"][-1]["id"] if tasks["Items"] else None
        result = {
            "task_ids": task_ids,
            "results": tasks,
            "user_id": user_id,
            "next_page_id": next_page_id,
        }
    except Exception as e:
        print("Error while getting tasks", e, event)
        result = {
            "error": str(e),
            "fe": filter_expression,
            "eav": expression_attribute_values,
        }
    return result


def _format(value, type="S"):
    return {type: value}


def _get_formatted_task_ids(task_ids):
    return [x["task_id"]["S"] for x in task_ids["Items"]]


def _get_formatted_tasks(tasks):
    print("some tasks", tasks)
    return [
        {
            "id": x["id"]["S"],
            "title": x["title"]["S"] if x.get("title") else "",
            "comments": [
                {
                    "user_id": y["M"]["user_id"]["S"],
                    "comment": y["M"]["comment"]["S"],
                }
                for y in x["comments"]["L"]
            ]
            if x.get("comments")
            else [],
            "description": x["description"]["S"]
            if x.get("description")
            else "",
        }
        for x in tasks
    ]

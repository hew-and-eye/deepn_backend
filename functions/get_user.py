import boto3
import uuid
from json import loads

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "MBL_USERS"


def handler(event, context, include_password=False):
    try:
        params = event.get("query")
        if not params:
            params = event.get("body")
        attribute_values = {}
        if params.get("username"):
            attribute_values[":u"] = _format(params["username"])
            expression = "username = :u"
            index_name = "Username"
            users = dynamodb.query(
                IndexName=index_name,
                TableName=TABLE_NAME,
                KeyConditionExpression=expression,
                ExpressionAttributeValues=attribute_values,
            )
        elif params.get("id"):
            attribute_values[":id"] = _format(params["id"])
            expression = "id = :id"
            users = dynamodb.query(
                TableName=TABLE_NAME,
                KeyConditionExpression=expression,
                ExpressionAttributeValues=attribute_values,
            )
        print("got some users", users)
        result = {"results": _get_formatted_result(users, include_password)}
    except Exception as e:
        print("Error while getting user", e, event)
        result = {"error": str(e), "event": event}
    return result


def _format(value, type="S"):
    return {type: value}


def _get_formatted_result(result, include_password=False):
    if include_password:
        return [
            {
                "id": x["id"]["S"],
                "username": x["username"]["S"],
                "password": x["password"]["S"],
            }
            for x in result["Items"]
        ]
    else:
        return [
            {"id": x["id"]["S"], "username": x["username"]["S"]}
            for x in result["Items"]
        ]

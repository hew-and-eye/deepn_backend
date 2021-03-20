import boto3
import uuid
from json import loads

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_USERS"


def handler(event, context, include_password=False):
    try:
        params = event.get("query")
        if not params:
            params = event.get("body")
        username = params.get("username")
        if username:
            attribute_values = {
                ":lower_bound": _format(username + "aaaaaaaa"),
                ":upper_bound": _format(username + "zzzzzzzzz"),
                ":org_id": _format("test_deepn_org"),
            }
            expression = "org_id=:org_id AND #username BETWEEN :lower_bound AND :upper_bound"
            index_name = "NameOrgSearch"
            users = dynamodb.query(
                IndexName=index_name,
                TableName=TABLE_NAME,
                KeyConditionExpression=expression,
                ExpressionAttributeValues=attribute_values,
                ExpressionAttributeNames={"#username": "username"},
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

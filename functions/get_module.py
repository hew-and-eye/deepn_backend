import boto3
import uuid
from json import loads

from functions.get_user import handler as get_user

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_MODULES"


def handler(event, context):
    try:
        params = event.get("body")
        attribute_values = {}
        if "name" in params.keys():
            attribute_values[":u"] = _format(params["name"])
            expression = "#name = :u"
            index_name = "Name"
            module = dynamodb.query(
                TableName=TABLE_NAME,
                IndexName=index_name,
                KeyConditionExpression=expression,
                ExpressionAttributeValues=attribute_values,
                ExpressionAttributeNames={"#name": "name"}
            )
            print("got module: ", module)
            result = {"results": _get_formatted_result(module['Items'][0])}
        else:
            attribute_values[":u"] = _format(params["id"])
            expression = "#id = :u"
            module = dynamodb.query(
                TableName=TABLE_NAME,
                KeyConditionExpression=expression,
                ExpressionAttributeValues=attribute_values,
                ExpressionAttributeNames={"#id": "id"}
            )
            print("got module: ", module)
            result = {"results": _get_formatted_result(module['Items'][0])}
    except Exception as e:
        print("Error while getting module", e, event)
        result = {"error": str(e), "event": event}
    return result

def _format(value, type="S"):
    return {type: value}

def _get_formatted_result(result, include_password=False):
    return {
        "id": result["id"]["S"], 
        "name": result["name"]["S"],
        "dependencies": result["dependencies"]["M"],
        "templates": result['templates']["S"],
        "owner": result['owner']["S"],
        "reactions": result['reactions']["S"]
        }


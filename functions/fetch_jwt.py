import boto3

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_ACCESS_TOKENS"

# This function could be better named. It purpose isn't to fetch the JWT, but to validate that the JWT exists.
def handler(event, context):
    access_token = event["headers"]["Authorization"].replace("Bearer ", "")
    if access_token:
        items = dynamodb.query(
            IndexName="AccessToken",
            TableName=TABLE_NAME,
            KeyConditionExpression="access_token = :access_token",
            ExpressionAttributeValues={":access_token": _format(access_token)},
        )
        print(items)
        if items:
            result = {"success": True, "access_token": access_token}
    else:
        result = {"error": "Missing authentication header"}
    return result


def _format(value, type="S"):
    return {type: value}

import boto3

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "MBL_ACCESS_TOKENS"


def handler(event):
    session = event["body"]["session"]
    dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            "user_id": _format(session["user_id"]),
            "access_token": _format(session["access_token"]),
            "expires_at": _format(session["expires_at"]),
        },
    )


def _format(value, type="S"):
    return {type: value}

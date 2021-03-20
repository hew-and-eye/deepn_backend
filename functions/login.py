import boto3
import jwt
import uuid
import datetime
from json import loads
from utils.secrets_manager import SecretsManager
from functions.store_jwt import handler as store_jwt

from functions.get_user import handler as get_user

dynamodb = boto3.client("dynamodb")
USER_TABLE = "MBL_USERS"


def handler(event, context):
    existing_user = get_user(event, context, include_password=True)
    if existing_user.get("results"):
        body = event.get("body")
        if body["password"] == existing_user["results"][0]["password"]:
            user = existing_user["results"][0]
            jwt = _generate_jwt(user)
            user.pop("password", None)
            result = {
                "session": {
                    "access_token": jwt,
                    "user_id": user["id"],
                    "expires_at": str(
                        datetime.datetime.utcnow() + datetime.timedelta(hours=6)
                    ),
                },
                "user": user,
            }
            try:
                store_jwt({"body": result})
            except Exception as e:
                result = {"error": "Failed to store token: " + str(e)}
        else:
            result = {"error": "Username or password is incorrect"}
    elif existing_user.get("error"):
        result = {"error": "Internal error while checking users"}
    return result


def _format(value, type="S"):
    return {type: value}


def _generate_jwt(user):
    sm = SecretsManager()
    jwt_key = sm["TEAMO"]["JWT_PRIVATE_KEY"]
    access_token = jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6),
            "user": {"id": user["id"], "username": user["username"]}
            # I might put a list of permissions here in the future
        },
        jwt_key,
        algorithm="HS256",
    )
    print("Generated JWT!", access_token)
    return access_token

from utils.secrets_manager import SecretsManager
import jwt
from functions.fetch_jwt import handler as fetch_jwt
from json import loads


def handler(event, context):
    access_token = fetch_jwt(event, context)["access_token"]
    print(access_token)
    if access_token:
        sm = SecretsManager()
        jwt_key = sm["DEEPN"]["JWT_PRIVATE_KEY"]
        decoded_jwt = jwt.decode(access_token, jwt_key, algorithms=["HS256"])
        # Create IAM policy document
        return {
            "principalId": event["requestContext"]["accountId"],
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow" if access_token else "Deny",
                        "Resource": "*",
                    },
                    {
                        "Action": "lambda:InvokeFunction",
                        "Effect": "Allow" if access_token else "Deny",
                        "Resource": "*",
                    },
                ],
            },
            "context": {
                "access_token": access_token,
                "user_id": decoded_jwt["user"]["id"],
                "username": decoded_jwt["user"]["username"],
            },
        }

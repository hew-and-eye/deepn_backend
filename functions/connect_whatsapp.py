import os
import requests
import boto3
import uuid
from json import loads
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client("dynamodb")
QR_ENDPOINT = os.getenv("qrEndpoint")
TASK_TABLE_NAME = "DEEPN_TASKS"
ACCESS_TABLE_NAME = "DEEPN_ACCESS_RIGHTS"


def handler(event, context):
    params = {"user_id": event["enhancedAuthContext"]["user_id"]}
    response = requests.get(QR_ENDPOINT, params=params)
    response.raise_for_status()
    print("GOT A RESPONSE", response.json())
    return response.json()

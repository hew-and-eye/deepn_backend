import boto3
import uuid
from json import loads

from functions.get_user import handler as get_user

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "DEEPN_USERS"


def handler(event, context):
    name = event["body"]["name"]

    mock_find_modules = [{
        "id": "abc123",
        "name": "Team members",
        "dependencies": {},
        "templates": {
            "0": "Ruben",
            "1": "Ruben and Matthew",
            "2": "Ruben, Matthew, Julia, and Maitre de Feu"
        },
        "owner": "Matthew",
        "reactions": { "thumbs_up": 2, "eggplant": 100 }
        },
        {
        "id": "abc123",
        "name": "Hello Team",
        "dependencies": {},
        "templates": {
            "0": "Ruben",
            "1": "Ruben and Matthew",
            "2": "Ruben, Matthew, Julia, and Maitre de Feu"
        },
        "owner": "Matthew",
        "reactions": { "thumbs_up": 2, "eggplant": 100 }
        },
        {
        "id": "abc123",
        "name": "Amazing (team) members",
        "dependencies": {},
        "templates": {
            "0": "Ruben",
            "1": "Ruben and Matthew",
            "2": "Ruben, Matthew, Julia, and Maitre de Feu"
        },
        "owner": "Matthew",
        "reactions": { "thumbs_up": 2, "eggplant": 100 }
        }]

    return mock_find_modules


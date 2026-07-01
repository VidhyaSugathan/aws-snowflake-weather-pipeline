import json
import os
import boto3
import requests
from datetime import datetime
from decimal import Decimal

# Environment Variable
API_KEY = os.environ["OPEN_WEATHER_API"]

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("weatherData")


def lambda_handler(event, context):

    city = "Kochi"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response = requests.get(url)

    weather = response.json()

    table.put_item(
        Item={
            "city": weather["name"],
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": Decimal(str(weather["main"]["temp"])),
            "humidity": Decimal(str(weather["main"]["humidity"])),
            "pressure": Decimal(str(weather["main"]["pressure"])),
            "description": weather["weather"][0]["description"]
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Weather data stored successfully!")
    }
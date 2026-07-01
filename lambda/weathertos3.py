import json
import boto3
import os
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer

s3 = boto3.client("s3")
deserializer = TypeDeserializer()

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]


def lambda_handler(event, context):

    print("===== Lambda Started =====")
    print("Received Event:")
    print(json.dumps(event))

    records = event.get("Records", [])
    print(f"Number of Records: {len(records)}")

    for record in records:
        print("Event Name:", record.get("eventName"))

        if record["eventName"] in ("INSERT", "MODIFY"):

            new_image = record["dynamodb"].get("NewImage")
            print("NewImage:", new_image)

            if not new_image:
                print("No NewImage found")
                continue

            item = {k: deserializer.deserialize(v) for k, v in new_image.items()}
            print("Deserialized Item:", item)

            timestamp = datetime.utcnow().strftime("%Y-%m-%d/%H-%M-%S-%f")
            key = f"weather-data/{timestamp}.json"

            print(f"Uploading to bucket: {BUCKET_NAME}")
            print(f"S3 Key: {key}")

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=json.dumps(item, default=str),
                ContentType="application/json",
            )

            print("✅ Upload Successful")

    print("===== Lambda Finished =====")

    return {"statusCode": 200, "body": json.dumps("Success")}

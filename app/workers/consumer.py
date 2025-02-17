import boto3
import os
import asyncio
import json
from dotenv import load_dotenv
from services.image_processor import dog_process_image, cat_process_image
import requests
from PIL import Image
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

# Create client consumer
sqs = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Create a FIFO SQS queue
response = sqs.create_queue(
    QueueName="pets-fifo.fifo",
    Attributes={
        "DelaySeconds": "0",
        "MessageRetentionPeriod": "86400",
        "FifoQueue": "true",
        "ContentBasedDeduplication": "true",
    },
)

queue_url = response["QueueUrl"]


async def fetch_image_from_url(url: str):
    """Fetch an image from a URL asynchronously"""
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)), True
    except Exception as e:
        return f"Error fetching image: {url} | {e}", False


async def process_message(message):
    """Process received message"""
    body = json.loads(message["Body"])
    image_url = body.get("image_url")
    analysis_type = body.get("analysis_type")
    pet_id = body.get("pet_id")

    temp_image_path, result = await fetch_image_from_url(image_url)

    if result:
        if analysis_type == "DOG-EMOTIONAL":
            result = await dog_process_image(temp_image_path)
        elif analysis_type == "CAT-EMOTIONAL":
            result = await cat_process_image(temp_image_path)

        logging.info(f"📥 Image received for analysis: {image_url} | Type: {analysis_type}")

        if result["status"] == "200":
            logging.info(f"✅ Analysis successful: ID:{pet_id}  Result:{result['result']}")
        else:
            logging.error(f"🚫 {result['result']}")

    else:
        logging.error(f"🚫 {temp_image_path}")


async def poll_queue():
    """Listen and process messages from SQS asynchronously"""
    logging.info("🔊 Listening for messages...")
    while True:
        try:
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
            )
            if "Messages" in messages:
                for message in messages["Messages"]:
                    logging.info("🔊 Message received")
                    await process_message(message)

                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message["ReceiptHandle"],
                    )
                    logging.info("✅ Message processed and removed from queue")

        except Exception as e:
            logging.error(f"🚫 Error processing messages: {e}")
        
        await asyncio.sleep(2)
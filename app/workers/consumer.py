import boto3
import os
import asyncio
import json
import logging
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import requests
from services.image_processor import (
    dog_breed_process_image,
    cat_breed_process_image,
    dog_process_image,
    cat_process_image,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize SQS client
sqs = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Function to create SQS queues
def create_queue(queue_name):
    return sqs.create_queue(
        QueueName=queue_name,
        Attributes={
            "DelaySeconds": "0",
            "MessageRetentionPeriod": "86400",
            "FifoQueue": "true",
            "ContentBasedDeduplication": "true",
        },
    )["QueueUrl"]

# Initialize queue URLs
queue_url = create_queue("pets-analysis-fifo.fifo")
response_queue_url = create_queue("pets-responses-fifo.fifo")

# Mapping of analysis types to processing functions
ANALYSIS_FUNCTIONS = {
    "DOG_EMOTIONAL": dog_process_image,
    "CAT_EMOTIONAL": cat_process_image,
    "DOG_BREED": dog_breed_process_image,
    "CAT_BREED": cat_breed_process_image,
}

async def fetch_image_from_url(url: str):
    """Fetch image from a URL and return a PIL Image object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        logging.error(f"🚫 Error fetching image: {url} | {e}")
        return None

async def send_response(analysis_id, result, status, type=None, accuracy=None):
    """Send a response message to the SQS response queue."""
    sqs.send_message(
        QueueUrl=response_queue_url,
        MessageGroupId="pets",
        MessageBody=json.dumps({
            "analysisId": analysis_id,
            "result": result,
            "status": status,
            "analysisType": type,
            "accuracy": accuracy,
        }),
    )

async def process_message(message):
    """Process an incoming SQS message."""
    body = json.loads(message["Body"])
    image_url, analysis_type, analysis_id = body.get("imageUrl"), body.get("analysisType"), body.get("analysisId")
    logging.info(f"📥 Processing image: {image_url} | Type: {analysis_type}")
    
    image = await fetch_image_from_url(image_url)
    if not image:
        return await send_response(analysis_id, "Failed to fetch image", "500")
    
    process_function = ANALYSIS_FUNCTIONS.get(analysis_type)
    if not process_function:
        return await send_response(analysis_id, "Invalid analysis type", "400")
    
    result = await process_function(image)
    status = "200" if result.get("status") == "200" else "500"
    await send_response(analysis_id, result.get("result", "Unknown error"), status, analysis_type, result.get("score"))
    logging.info(f"✅ Analysis complete: ID:{analysis_id} | Result:{result.get('result')}")

async def poll_queue():
    """Continuously poll the SQS queue for new messages."""
    logging.info("🔊 Listening for messages...")
    while True:
        try:
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
            ).get("Messages", [])
            
            for message in messages:
                logging.info("🔊 Message received")
                await process_message(message)
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
                logging.info("✅ Message processed and removed from queue")

        except Exception as e:
            logging.error(f"🚫 Error processing messages: {e}")
        
        await asyncio.sleep(2)
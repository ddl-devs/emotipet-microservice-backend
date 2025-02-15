import boto3
import os
import time
import json
from dotenv import load_dotenv
from app.services.image_processor import dog_process_image

load_dotenv()

#Create client consumer
sqs = boto3.client(
    "sqs", 
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

#Create a SQS FIFO queue
response = sqs.create_queue(
    QueueName="pets-fifo.fifo",  
    Attributes={
        "DelaySeconds": "0",  
        "MessageRetentionPeriod": "86400",  
        "FifoQueue": "true",  
        "ContentBasedDeduplication": "true", 
    }
)

queue_url = response["QueueUrl"]

def process_message(message):
    """Process received message"""
    body = json.loads(message["Body"])
    image_url = body.get("image_url")
    image_type = body.get("analysis_type")
    pet_id = body.get("pet_id")

    print(f"📥 Recebida imagem para análise: {image_url} | Tipo: {image_type}")

def poll_queue():
    """Listen and process messages from SQS"""
    while True:
        messages = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        if "Messages" in messages:
            for message in messages["Messages"]:
                process_message(message)

                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message["ReceiptHandle"]
                )
                print("✅ Mensagem processada e removida da fila")

        time.sleep(2)  

if __name__ == "__main__":
    print("🎯 Escutando a fila SQS...")
    poll_queue()

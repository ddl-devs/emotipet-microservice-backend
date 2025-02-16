import boto3
import os
import time
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
    region_name=os.getenv("AWS_REGION")
)

# Create a SQS FIFO queue
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


def fetch_image_from_url(url: str) -> str:
    """
    Fetch an image from a URL, save it as a temporary file, and return the file path.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return Image.open(BytesIO(response.content)), True
    except:
        return f"Erro ao buscar a imagem: {url}", False


def send_success_message(message):
    sqs.send_message(
        MessageGroupId="pets",
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )

def process_message(message):
    """Process received message"""
    body = json.loads(message["Body"])
    image_url = body.get("image_url")
    analysis_type = body.get("analysis_type")
    pet_id = body.get("pet_id")
    
    temp_image_path, result = fetch_image_from_url(image_url)

    if result:
        if analysis_type == "DOG-EMOTIONAL":
                result = dog_process_image(temp_image_path)
        
        elif analysis_type == "CAT-EMOTIONAL":
            result = cat_process_image(temp_image_path)

        logging.info(f"📥 Recebida imagem para análise: {image_url} | Tipo: {analysis_type}")

        if result["status"] == "200":
            logging.info(f"✅ Analise realizada com sucesso: ID:{pet_id}  Resultado:{result['result']}")

        else:
            logging.error(f"🚫{result["result"]}")

    else:
        logging.error(f"🚫{temp_image_path}")


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


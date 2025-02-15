import boto3
import os
import json


queue_url = "https://sqs.us-east-2.amazonaws.com/209479262001/pets-fifo.fifo"

#Create client consumer
sqs = boto3.client(
    "sqs", 
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# Simulação de URLs de imagens
image_requests = [
    {"image_url": "https://meusite.com/imagens/dog1.jpg", "image_type": "dog"},
    {"image_url": "https://meusite.com/imagens/cat1.jpg", "image_type": "cat"},
    {"image_url": "https://meusite.com/imagens/dog2.jpg", "image_type": "dog"},
]

# Enviar mensagens para a fila
for request in image_requests:
    response = sqs.send_message(
        MessageGroupId="pets",
        QueueUrl=queue_url,
        MessageBody=json.dumps(request)
    )
    print(f"Mensagem enviada: {request} | MessageId: {response['MessageId']}")
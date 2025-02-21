import boto3
import os
import json


queue_url = "https://sqs.us-east-2.amazonaws.com/209479262001/pets-analysis-fifo.fifo"

# Create client consumer
sqs = boto3.client(
    "sqs", 
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# Message data for testing AWS SQS and AI Models
image_requests = [
    # {
    #     "image_url": "https://media.istockphoto.com/id/1503385646/pt/foto/portrait-funny-and-happy-shiba-inu-puppy-dog-peeking-out-from-behind-a-blue-banner-isolated-on.jpg?s=2048x2048&w=is&k=20&c=V7rwk63TEO_FYZHGVwTOi1FZflI03jITp_B1HWKjHvE=",
    #     "analysis_type": "DOG-EMOTIONAL",
    #     "pet_id": 1
    # },
    # {
    #     "image_url": "https://delavanlakesvet.com/wp-content/uploads/sites/195/2022/03/smiling-cat-for-web.jpg",
    #     "analysis_type": "CAT-EMOTIONAL",
    #     "pet_id": 1
    # },
    # {
    #     "image_url": "https://assets.elanco.com/8e0bf1c2-1ae4-001f-9257-f2be3c683fb1/fca42f04-2474-4302-a238-990c8aebfe8c/Siamese_cat_1110x740.jpg?w=3840&q=75&auto=format",
    #     "analysis_type": "CAT-BREED",
    #     "pet_id": 1
    # },
    # {
    #     "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Jewelkatz_Romeo_Of_Stalker-Bars.jpg",
    #     "analysis_type": "CAT-BREED",
    #     "pet_id": 1
    # },
    {
        "imageUrl": "https://animalcarecentersmyrna.com/wp-content/uploads/2021/08/Untitled-design-2021-08-19T162152.857.png",
        "analysisType": "DOG-BREED",
        "analysisId": 1
    },
]

# Simulates main backend sending messages
for request in image_requests:
    response = sqs.send_message(
        MessageGroupId="pets",
        QueueUrl=queue_url,
        MessageBody=json.dumps(request)
    )
    print(f"Message sended: {request} | MessageId: {response['MessageId']}")
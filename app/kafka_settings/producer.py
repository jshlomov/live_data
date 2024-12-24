import json
import os

from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv(verbose=True)

def produce_message(topic_name: str, message: str, key: str):
    producer = KafkaProducer(
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        value_serializer= lambda value: json.dumps(value).encode('utf-8')
    )
    producer.send(
        topic_name,
        value=message,
        key=key.encode('utf-8')
    )
    producer.flush()

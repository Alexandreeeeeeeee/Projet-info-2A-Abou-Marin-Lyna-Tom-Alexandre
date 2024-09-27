from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    'listen-events',
     bootstrap_servers=['ec2-54-154-64-115.eu-west-1.compute.amazonaws.com:9092'],
     auto_offset_reset='earliest',
     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    message = message.value
    print(message)
    # DO SOMETHING

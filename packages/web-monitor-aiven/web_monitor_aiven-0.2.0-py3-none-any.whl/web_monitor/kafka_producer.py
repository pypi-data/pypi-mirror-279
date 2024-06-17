from kafka import KafkaProducer
import json
import logging


class KafkaProducerWrapper:
    def __init__(self, kafka_server, credentials_source, kafka_topic):
        folderName = credentials_source
        logging.info(f"Initializing Kafka producer for topic {kafka_topic} on server {kafka_server}")
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_server,
			security_protocol="SSL",
			ssl_cafile=folderName+"ca.pem",
			ssl_certfile=folderName+"service.cert",
			ssl_keyfile=folderName+"service.key",
			value_serializer=lambda v: json.dumps(v).encode('ascii'),
			key_serializer=lambda v: v.encode('ascii')
        )
        self.kafka_topic = kafka_topic

    def send(self, message):
        try:
            key = message['url']
            logging.info(f"Sending message to Kafka topic {self.kafka_topic}: {message}")
            self.producer.send(self.kafka_topic, key=key, value=message)
            self.producer.flush()
            logging.info(f"Message sent to Kafka topic {self.kafka_topic}")
        except Exception as e:
            logging.error(f"Failed to send message to Kafka Topic: {e}")

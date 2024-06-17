from kafka import KafkaProducer
import json
import logging


class KafkaProducerWrapper:
    def __init__(self, kafka_server, credentials_source_dir, kafka_topic):
        # Initialize Kafka producer
        folderName = credentials_source_dir # Path to the folder containing the Kafka credentials
        logging.info(f"Initializing Kafka producer for topic {kafka_topic} on server {kafka_server}")
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_server,
			security_protocol="SSL", # Use SSL for secure communication
			ssl_cafile=folderName+"ca.pem", # Path to the CA certificate
			ssl_certfile=folderName+"service.cert", # Path to the service certificate
			ssl_keyfile=folderName+"service.key", # Path to the service key
			value_serializer=lambda v: json.dumps(v).encode('ascii'), # Serialize the value to JSON and encode to ASCII
			key_serializer=lambda v: v.encode('ascii') # Serialize the key to ASCII
        )
        self.kafka_topic = kafka_topic

    def send(self, message):
        # Send a message to the Kafka topic
        try:
            key = message['url'] if 'url' in message else None # Use the URL as the key
            logging.info(f"Sending message to Kafka topic {self.kafka_topic}: {message}")
            self.producer.send(self.kafka_topic, key=key, value=message) # Send the message to the Kafka topic with the key
            self.producer.flush()
            logging.info(f"Message sent to Kafka topic {self.kafka_topic}")
        except Exception as e:
            logging.error(f"Failed to send message to Kafka Topic: {e}")

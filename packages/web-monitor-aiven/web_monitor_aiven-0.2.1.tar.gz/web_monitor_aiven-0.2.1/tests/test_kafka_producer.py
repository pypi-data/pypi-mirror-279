# tests/test_kafka_producer.py
import unittest
from unittest.mock import patch, MagicMock
import logging
from web_monitor.kafka_producer import KafkaProducerWrapper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestKafkaProducerWrapper(unittest.TestCase):

    @patch('web_monitor.kafka_producer.KafkaProducer')
    def test_send_message(self, MockKafkaProducer):
        mock_producer_instance = MagicMock()
        MockKafkaProducer.return_value = mock_producer_instance

        kafka_server = 'localhost:9092'
        credentials_source_dir = '/path/to/credentials/'
        kafka_topic = 'website_monitor'
        
        producer = KafkaProducerWrapper(
            kafka_server, credentials_source_dir, kafka_topic)
        message = {'url': 'https://example.com', 'status_code': 200}

        producer.send(message)

        mock_producer_instance.send.assert_called_once_with(
            kafka_topic,
            key=b'https://example.com',
            value=message
        )
        mock_producer_instance.flush.assert_called_once()

if __name__ == '__main__':
    unittest.main()

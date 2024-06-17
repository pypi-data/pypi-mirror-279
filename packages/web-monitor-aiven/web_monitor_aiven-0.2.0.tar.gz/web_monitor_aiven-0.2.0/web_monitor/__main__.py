import argparse
import time
import yaml
import logging
from web_monitor.checker import WebsiteChecker
from web_monitor.kafka_producer import KafkaProducerWrapper

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Website Monitor')
    parser.add_argument('--config', type=str, required=True, help='Path to configuration file')
    args = parser.parse_args()

    config = load_config(args.config)
    kafka_server = config['kafka']['server']
    credentials_source = config['kafka']['credentials_source']
    kafka_topic = config['kafka']['topic']
    websites = config['websites']
    interval = config['interval']

    producer = KafkaProducerWrapper(kafka_server, credentials_source, kafka_topic)

    while True:
        for site in websites:
            checker = WebsiteChecker(site['url'], site.get('regex'))
            result = checker.check()
            producer.send(result)
        time.sleep(interval)

if __name__ == '__main__':
    logging.info("Starting website monitor")
    main()
    

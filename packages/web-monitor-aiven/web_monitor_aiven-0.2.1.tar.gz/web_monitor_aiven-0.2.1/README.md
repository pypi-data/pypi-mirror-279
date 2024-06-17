# Web Monitor

A scalable web monitor application that feeds information about website availability to an Aiven Kafka instance.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup for Distribution on PyPI](#setup-for-distribution-on-pypi)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Program](#running-the-program)
- [Design Decisions](#design-decisions)
- [TODO List](#todo-list)
- [Scalability and Real-World Scenarios](#scalability-and-real-world-scenarios)
- [Open Source Considerations](#open-source-considerations)

## Overview

This application periodically checks the availability of specified websites and sends the results to a Kafka topic. The metrics collected include total response time, HTTP status code, and optional regex match results.

## Project Structure

```bash
web_monitor/
├── web_monitor/
│ ├── init.py
│ ├── main.py
│ ├── checker.py
│ └── kafka_producer.py
├── tests/
│ ├── init.py
│ └── test_checker.py
│ └── test_kafka_producer.py
├── README.md
├── setup.py
└── requirements.txt
```

## Setup for Distribution on PyPI

To distribute this package on PyPI, follow these steps:

1. **Install `wheel` and `twine`**:

    ```sh
    pip install wheel twine
    ```

2. **Create Distribution Packages**:

    ```sh
    python setup.py sdist bdist_wheel
    ```

3. **Upload to PyPI**:

    ```sh
    twine upload dist/*
    ```

## Configuration

Create a configuration file `config.yaml` with the following structure:

```yaml
kafka:
  server: 'localhost:9092'
  credentials_source_dir: '/path/to/credentials/'
  topic: 'website_monitor'

websites:
  - url: 'https://example.com'
    regex: '<title>Example Domain</title>'
  - url: 'https://anotherexample.com'

interval: 60
```

- kafka.server: The address of your Kafka server.
- kafka.credentials_source_dir: The path to your SSL certificates for Kafka. Sensitivity should be considered when storing these credentials. The path should contain the following files:
    -- ca.pem
    -- service.cert
    -- service.key
- kafka.topic: The Kafka topic where messages will be sent.
- websites: A list of websites to monitor, each with an optional regex for content validation.
- interval: The interval in seconds between checks.

## Installation

To install the `web_monitor` package, use the following command:

```sh
pip install web_monitor
```

## Running the Program

To run the program, execute the following command:

```sh
web_monitor --config config.yaml
```

## Design Decisions

- Modular Structure: The application is divided into modular components (checker.py and
kafka_producer.py) to separate concerns and improve maintainability.
- SSL for Kafka: The Kafka producer uses SSL for secure communication, with paths to certificate files specified in the configuration.
- Configurable: The program reads from a YAML configuration file, making it easy to adjust settings without changing the code.
- Message Key: Using the website address as the key for Kafka messages ensures messages related to the same website are sent to the same partition.

## TODO List

- Enhanced Error Handling: Improve error handling and retries for network issues and Kafka communication failures.
- Logging: Implement a more robust logging system with different log levels and output formats.
Asynchronous Requests: Use asynchronous HTTP requests to handle a larger number of websites more efficiently.
- CI/CD Integration: Add Continuous Integration and Continuous Deployment pipelines for automated testing and deployment.
- Testing: Increase test coverage, especially for edge cases and failure scenarios.

## Scalability and Real-World Scenarios

### Scalability 

- The program can scale to monitor a larger number of websites by running multiple instances in parallel, each monitoring a subset of websites.
- Asynchronous Processing: Use libraries like `aiohttp` and `asyncio` to perform non-blocking HTTP requests.
- Batch Processing: Batch website checks and Kafka messages to reduce load and improve efficiency.

### Real-World Scenarios

- Fault Tolerance: Implement retry mechanisms for failed requests and Kafka messages to ensure data integrity.
- Monitoring: Add monitoring and alerting capabilities to detect issues and ensure the application is running smoothly.
- Performance Optimization: Profile the application to identify bottlenecks and optimize performance for large-scale deployments.
- Security: Implement secure coding practices and regular security audits to protect against vulnerabilities.

## Open Source Considerations

- License: Choose an open-source license (e.g., MIT, Apache) to allow others to use and modify the code.
- Documentation: Provide clear documentation, including installation instructions, configuration options, and usage examples.
- Code Quality: Follow PEP 8 guidelines, use meaningful variable names, and include comments to make the code easy to understand.
- Community Engagement: Encourage contributions from the community through issues, pull requests, and discussions.
- Versioning: Use semantic versioning to indicate changes and updates to the codebase.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so.

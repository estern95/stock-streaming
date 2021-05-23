# stock-streaming

This is an end-to-end app utilizing kafka, spark on the Databricks runtime, and Docker + docker-compose. The stream is then processed with the Spark Structured Streaming Module to generate stock predictions based on options buying behavior.

## Helpful Resources

### Docker and Compose:
[Running Compose on Google Cloud](https://cloud.google.com/community/tutorials/docker-compose-on-container-optimized-os)

### Kafka Troubleshooting
[Connectivity FAQ](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity)
[Kafka Networking](https://rmoff.net/2018/08/02/kafka-listeners-explained/)
[Kafka Docker Tutorial](http://wurstmeister.github.io/kafka-docker/)

### Spark Streaming
[Connecting to Kafka](https://sparkbyexamples.com/spark/spark-streaming-with-kafka/)


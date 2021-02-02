1. get kafka install on machine (Done)
2. get kafka-python quick start running (Done)
3. get medium article python code working (Done)
4. Added Docker Container (Done)
   1. Not done: setting up zookeeper + Kafka Server
5. Set up kafkaProducer in scappers (done)
6. set up databricks to consume from kafka broker
7. Cloud Work
   1. I think we need a couple of instances:
      1. Kafka Server
      2. Zookeeper Server
      3. Scrapper App 
      4. Spark instance for analytics
      5. Serverless function for generating backend
      6. React.js or FastAPI or Flask for frontend 
   2. After more research, we can do this with docker compose with one EC2 instance https://medium.com/big-data-engineering/hello-kafka-world-the-complete-guide-to-kafka-with-docker-and-python-f788e2588cfc
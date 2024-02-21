<div align="center">
    
# BATCH
(*for Linux*)
<hr />

[xxx](#docker-general-info) •


</div>

<hr />
<br>

## INTRODUCTION 

We will be covering: 
1. What is Stream Processing
2. What is Kafka
3. What is Kafka's role in this space
4. Message prcperties of Str
5. Configuration and Paramaters specific to Kafka
6. Time Spanning
7. Karka Producers and Consumers
8. Stream Processing data partitionings
9. Working with Karka streams (in Java)
10. Role of Schema
11. Kafka Connect
12. KSQL DB

## WHAT IS STREAMING 

Data is exchanged in real time rather than in batches. In batch processing we may consume data every minute or every hour, and in streaming the comes in much faster. 

## WHAT IS KAFKA STREAMING 
Producers produces info to a topic and consumer retrieves info from a topic. 

Topic - a continuous stream of events. 

Events across time are a single data point at a certain tiem stamp. 

Logs are how events are stored in a database. 

Each event contains a message containing a key, value, timestamp. Key is used for mining and partitioning. 

Why is Karka popular: 
- Replication - robust and reliable
- Flexible - can have small or large topics, with any number of consumers
- Lots of integration - Kafka connect, KSQL DB
- Can store data in tier storage - cheap and available.
- Scalable.

Why do we need Stream Processing: 
- In the past data was housed in Monolith Service. 
- The trend now is towards working with microservices - many small applications. 
- The microservices need to communicate with each other... genearlly via APIs, message bus, or another central DB. 
- This architecture works alright when your microservices are not growing that much and your api size is not that big.
- With more and more data, you need a consistant message service or streaming service to pass info.
- One of the microservice writes to a kafka topic, and then any of the other microservices with access can read that.
- Sometimes you need to have multiple data sources, Kafka provides Change Data Capture (CDC) to deal with that.
- The DBs can also write to the Kafka topics, and anybody interested with access can read.
- Kafka acts as a bridge between microservices and DBs.

# CONFLUENT CLOUD SET UP 
There will also be a docker file provided, if you would prefer to set up Kafka locally. 


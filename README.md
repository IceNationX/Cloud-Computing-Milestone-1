# SOFE4630U - Milestone 1: Data Ingestion System (Cloud Pub/Sub)

**Student Name:** Mohammad Al-Lozy  
**Student ID:** 100829387  
**Course:** SOFE4630U - Distributed Systems  

---

## 📖 Project Overview
In the first part of Milestone 1, the objective was to familiarize ourselves with the Google Cloud Platform (GCP) and create the project and the Pub/Sub topics.

After successfully forking the repository, we utilized the `v1` and `v2` folders. By changing the name of the Project ID, we were able to successfully send messages from a smart meter simulation to a consumer script.

---

## 📂 Repository Structure

### 1. Smart Meter Simulation (V2)
This section simulates a smart device sending data to the cloud.
* **Producer (`smartMeter.py`):** Generates and sends random sensor data.
* **Consumer (`consumer.py`):** Receives and displays the data.

### 2. Design Part
For the design task, I set up a new folder and added the `Auth.json` file. I created two Python scripts—one for publishing and one for consuming—and created a new topic named `designTopic`.

* **`design_producer.py`**: Reads records from `Labels.csv` and publishes them to the topic.
* **`design_consumer.py`**: Subscribes to the topic and consumes the records.

---

## 🎥 Video Deliverables

* **Smart Meter Application Demo:** [PASTE YOUR LINK HERE]
* **Design Part Demo:** [PASTE YOUR LINK HERE]

---

## 📝 Discussion

### 1. What is EDA? What are its advantages and disadvantages?

**EDA (Event-Driven Architecture)** is a software design pattern where decoupled services communicate by generating and consuming "events" (notifications of a state change) rather than direct request-response calls. In this architecture, a producer publishes an event (e.g., "Order Placed") to a broker (like Pub/Sub), and consumers subscribe to react to that event asynchronously.

**Advantages:**
* **Loose Coupling:** Producers and consumers do not know about each other.
* **Scalability:** Since components are decoupled, they can be scaled independently. If the consumer service is overwhelmed, you can add more instances to distribute the load.
* **Fault Tolerance:** If a consumer fails, the event broker buffers the messages until the consumer comes back online. The failure is isolated and does not crash the producer.
* **Responsiveness:** EDA allows for real-time processing, enabling systems to react immediately as events occur rather than waiting for scheduled jobs.

**Disadvantages:**
* **Complexity:** EDA is inherently more complex to design and build than monolithic architectures.
* **Debugging Difficulty:** Tracing a transaction that hops through multiple asynchronous services is difficult. If an error occurs, it is harder to pinpoint exactly where the data flow broke compared to a linear request-response chain.
* **Eventual Consistency:** Since data updates happen asynchronously, different parts of the system might see different data states for a short time (eventual consistency) rather than immediate consistency.

### 2. Cloud Pub/Sub has two types of subscriptions: push and pull. Describe them.

**Pull Subscription:**
In a pull subscription, the subscriber makes the request to the Pub/Sub server to fetch messages. The subscriber enters a loop and asks, "Do you have any new data for me?"
* **Advantages:** It provides better flow control. If the subscriber is flooded, it can just stop pulling messages until it is caught up. It is best suited for high-throughput batch processing or large workloads where the subscriber needs to handle its own resources.
* **Disadvantages:** It requires more complex code (looping, error handling) and can cause higher latency because the subscriber may wait before polling again.

**Push Subscription:**
In a push subscription, Pub/Sub makes the first call by sending an HTTP POST request to a webhook (URL) provided by the subscriber. The subscriber is passive and waits to be called by the server.
* **Advantages:** It is easier to implement (no polling loops needed) and provides near real-time latency. It is great for serverless apps (such as Google Cloud Functions) or webhooks where the app simply responds to incoming traffic.
* **Disadvantages:** The subscriber has no control over the flow; if a million messages come at once, the subscriber could be flooded (DDoS attack style). It also requires a publicly accessible HTTPS endpoint.

### 3. When publishing a message into a topic, an ordering key can be specified. Describe its role and benefits.

**Role:**
By default, Pub/Sub does not guarantee order. But if an **"Ordering Key"** is attached to a message, Pub/Sub guarantees that all messages with that ordering key will be delivered to the subscriber in the exact order that they were published.

**Benefits:**
This allows the developer to ensure that certain logical sequences are maintained for specific items without requiring the whole system to be synchronous, which would be slow.

**Examples:**
* **Database Updates:** In order to sync a database, "Create Record" must be done before "Update Record." By using the `Record_ID` as the ordering key, we ensure that these changes happen in the proper sequence for that specific record.
* **User Activity Tracking:** In order to track user activity for a game, we must know that "picked up key" happens before "opened door." By using `User_ID` as the ordering key, we ensure that specific user's activities happen in the proper sequence, even if thousands of other users' activities are happening in parallel.

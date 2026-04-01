# Real-Time Fraud Detection Pipeline (MLOps)

An end-to-end Machine Learning operations (MLOps) pipeline built to detect fraudulent credit card transactions in real-time. 

## Architecture
This project simulates a live streaming environment where transactions are processed and evaluated by an AI model in milliseconds.

1. **Data Ingestion:** A Python Producer script simulates live transactions and publishes them to **Redpanda (Kafka)**.
2. **Stream Processing:** A Python Consumer subscribes to the topic, performs feature formatting, and passes data to the ML model.
3. **Inference:** An **XGBoost** model evaluates the 30-feature vector to predict `Fraud` or `Legit`.
4. **Storage:** Results and financial metrics are pushed to a **PostgreSQL** database.
5. **Monitoring:** A live **Grafana** dashboard queries the database to visualize fraud volume and financial impact in real-time.

## Tech Stack
* **Machine Learning:** Python, Pandas, Scikit-Learn, XGBoost
* **Streaming:** Redpanda / Apache Kafka
* **Infrastructure:** Docker, Docker Compose
* **Database & Viz:** PostgreSQL, Grafana

## How to Run (Locally or in Codespaces)

**Start the Infrastructure:**
   ```bash
   docker-compose up -d

   pip install -r requirements.txt

   python3 consumer.py

   python3 producer.py


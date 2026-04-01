import json
import time
import random
from kafka import KafkaProducer

# Setup Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# --- 1. Create FULL templates with all 30 columns ---
legit_template = {"Time": 0.0, "Amount": 20.0}
fraud_template = {"Time": 9999.0, "Amount": 5000.0}

# Automatically fill V1 through V28 with dummy data
for i in range(1, 29):
    legit_template[f"V{i}"] = 0.1   # Normal looking data
    fraud_template[f"V{i}"] = -5.0  # Suspicious looking data

print("🚀 Starting Continuous Stress Test (200 Transactions)...")

# --- 2. Send the Stream ---
for i in range(200):
    if random.random() > 0.15: # 85% chance it's legit
        data = legit_template.copy()
        data['Amount'] = random.uniform(10, 100) 
        label = "LEGIT"
    else: # 15% chance it's fraud
        data = fraud_template.copy()
        data['Amount'] = random.uniform(1000, 5000) 
        label = "FRAUD"

    producer.send('transactions', value=data)
    print(f"Sent {i}/200 | Type: {label}")
    time.sleep(0.1) # Send fast!

print("Stress Test Complete!")
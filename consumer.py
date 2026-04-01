import joblib
import json
import pandas as pd
import psycopg2
from kafka import KafkaConsumer

# --- 1. Database Setup ---
def init_db():
    conn = psycopg2.connect(
        host="localhost",
        database="fraud_db",
        user="user",
        password="password"
    )
    cur = conn.cursor()
    # Create a table to store our results
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            transaction_id INT,
            prediction INT,
            amount FLOAT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn, cur

conn, cur = init_db()

# --- 2. Load Model ---
model = joblib.load('fraud_model.pkl')
print("Model and Database ready!")

# --- 3. Setup Kafka Consumer ---
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Waiting for transactions...")

# --- 4. The Real-Time Loop ---
# Define the EXACT order the model expects
feature_order = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']

for message in consumer:
    transaction_data = message.value
    
    # 1. Create DataFrame
    df_temp = pd.DataFrame([transaction_data])
    
    # 2. Re-order columns to match the model's training exactly
    # This fixes the "feature_names mismatch" error
    try:
        df_temp = df_temp[feature_order]
    except KeyError as e:
        print(f"Skipping record: Missing column {e}")
        continue
    
    # 3. Predict
    prediction = int(model.predict(df_temp)[0])
    
    # 4. Save to Database
    amt = float(transaction_data.get('Amount', 0))
    cur.execute(
        "INSERT INTO predictions (transaction_id, prediction, amount) VALUES (%s, %s, %s)",
        (message.offset, prediction, amt)
    )
    conn.commit()
    
    status = "FRAUD!" if prediction == 1 else "Legit"
    print(f"ID: {message.offset} | Result: {status} | Saved to DB")
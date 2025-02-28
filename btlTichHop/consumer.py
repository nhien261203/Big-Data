from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# 1️⃣ Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tiktok_db"]  # Tạo database "tiktok_db"
collection = db["tiktok_data"]  # Tạo collection "tiktok_data"

# 2️⃣ Kết nối Kafka Consumer
consumer = KafkaConsumer(
    "tiktok-trends",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("📥 Listening and saving to MongoDB...")

# 3️⃣ Nhận dữ liệu từ Kafka và lưu vào MongoDB
for message in consumer:
    collection.insert_one(message.value)  # Lưu dữ liệu vào MongoDB
    print(f"✅ Saved to MongoDB: {message.value}")

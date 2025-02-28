import csv
import json
import time
from kafka import KafkaProducer

# Kết nối tới Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "tiktok-trends"

# Đọc file CSV
with open("tiktok_dataset.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        producer.send(topic, row)
        print(f"Sent: {row}")
        time.sleep(1)  # Giả lập gửi dữ liệu theo thời gian thực

producer.flush()
print("✅ Done sending data!")

from kafka import KafkaProducer
import pandas as pd
import os, json, time
import random

# CONFIG
brker1 = "my-release-kafka-controller-0.my-release-kafka-controller-headless.default.svc.cluster.local:9092"
brker2 = "my-release-kafka-controller-1.my-release-kafka-controller-headless.default.svc.cluster.local:9092"
brker3 = "my-release-kafka-controller-2.my-release-kafka-controller-headless.default.svc.cluster.local:9092"

bootstrap_servers= [brker1, brker2, brker3] # địa chỉ của broker để gửi nhận message | localhost:9092 là địa chỉ brokder mặc định (check trong file config/server.properties)
topic = 'prjBigdata'
csv_file = r"C:\Users\ADMIN\OneDrive\Desktop\Traffic-accident-analysis\sample_data_to_send\sample10.csv"

# đọc file csv
df = pd.read_csv(csv_file)
records = df.to_dict("records")

# Khởi tạo 1 Producer
producer = KafkaProducer(bootstrap_servers= bootstrap_servers)

# Gửi message tới 1 topic (ví dụ gửi 20 message LIÊN TỤC)
for record in records:
    message = json.dumps(record).encode('utf-8') # encode về dạng bytes để gửi | chỉ gửi được thông điệp dạng bytes
    producer.send(topic, message)
    time.sleep(random.randint(1,5))

# Close the producer
producer.flush()
producer.close()

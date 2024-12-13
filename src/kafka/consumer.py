from kafka import KafkaConsumer
import json

# CONFIG
topic_name = 'prjBigdata'
bootstrap_servers = ['localhost:9092', 'localhost:9093'] # địa chỉ của brokder để gửi nhận message | localhost:9092 là địa chỉ brokder mặc định (check trong file config/server.properties)
auto_offset_reset='earliest' # Start reading at the beginning | tự động đọc bắt đầu từ đầu
group_id='my_group'


# Khởi tạo 1 Consumer
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers= bootstrap_servers,
    auto_offset_reset= auto_offset_reset,  
    group_id= group_id
)

# Đọc các message consumer nhận được
for message in consumer:
    value = message.value.decode('utf-8') # bytes.decode() -> để ra string
    data = json.loads(value)
    print(type(data))

Chạy kafka 
- bước 1: Chạy zookeeper và các brokers (cluster) trước bằng docker: 
        sudo docker-compose up -d
- bước 2: Test lại cluster (các brokers): nếu ra cái WARN là lỗi, phải không ra cái gì mới là ok
        sudo docker exec -it broker1 kafka-topics --bootstrap-server broker1:29092 --list 
        note: xem boostrap-server là broker1:2902 ở trong file .yaml, dòng: CONFLUENT_METRICS_REPORTER_BOOTSTRAP_SERVERS: broker1:29092
- bước 3: Tạo topic cũng trên terminal (không phải trong code)
        sudo docker exec -it broker1 kafka-topics --bootstrap-server broker1:29092 --create --topic prjBigdata --replication-factor 2 --partitions 3
- bước 4: verify lại topic (bằng cách miêu tả topic)
        sudo docker exec -it broker1 kafka-topics --bootstrap-server broker1:29092 --describe --topic prjBigdata
- bước 5: Chạy file producer.py
        để bootstrap_servers = các localhost:909x | xem ở file .yaml, cái PLAINTEXT_HOST ở dòng: KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker1:29092,PLAINTEXT_HOST://localhost:9092
- bước 6: chạy file consumer.py
        để bootstrap_servers y hệt như trên
- Kết thúc tất cả:
        sudo docker-compose down
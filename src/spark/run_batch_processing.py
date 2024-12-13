from pyspark.sql import SparkSession
from transformations import *
# from cassandra.cluster import Cluster

### CONFIG
appName = "Batch Processing"
install_tool = "spark.jars.packages" # cái hỗ trợ tải các java package
install_packages = "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0" # các package cần tải

file_data_hdfs = "hdfs://namenode:9000/input/data.csv" # file path của master dataset trên HDFS

keyspace = "bigdata"

# Tạo SparkSession
spark = SparkSession.builder \
    .appName(appName) \
    .config(install_tool, install_packages) \
    .getOrCreate()

# Đọc dữ liệu từ HDFS
df = spark.read.csv(file_data_hdfs, header=True, inferSchema=True)
print("Dữ liệu từ HDFS:")
df.show()

### Transform dữ liệu
list_transform_func: list[function] = list()
list_table_name: list[str] = list()

for transform_func, table_name in zip(list_transform_func, list_table_name):
    # Transform dữ liệu
    df_transformed = transform_func(df)

    print("Dữ liệu đã xử lý:")
    df_transformed.show()

    # Ghi vào Cassandra | NOTE: phải cấu hình đúng - Spark sẽ tự động kết nối với Service của Cassandra nếu có cấu hình đúng. 
    # NOTE: có thể cấu hình bằng tay được - truyền vào khi tạo SparkSession
    
    df_transformed.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table=table_name, keyspace= keyspace) \
        .save()

    print("Đã ghi vào Cassandra!")

# Dừng Spark
spark.stop()

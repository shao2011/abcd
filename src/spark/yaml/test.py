# from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName("Spark Cluster Test").getOrCreate()
#    # .master("spark://my-release-spark-master-0.my-release-spark-headless.default.svc.cluster.local:7077") \
# # Tạo DataFrame mẫu
# data = [("Alice", 29), ("Bob", 31), ("Cathy", 25)]
# columns = ["Name", "Age"]
# df = spark.createDataFrame(data, columns)

# df.show()

# spark.stop()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
from pyspark.sql import SparkSession
# from cassandra.cluster import Cluster

### CONFIG
appName = "Batch Processing"
install_tool = "spark.jars.packages" # cái hỗ trợ tải các java package
install_packages = "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0" # các package cần tải


keyspace = "bigdata"

# Tạo SparkSession
spark = SparkSession.builder \
    .appName(appName) \
    .config(install_tool, install_packages) \
    .getOrCreate()

# Tạo DataFrame mẫu
data = [("Alice", 29), ("Bob", 31), ("Cathy", 25)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

df.write.format("org.apache.spark.sql.cassandra").mode("append").options(table = table_name, keyspace = keyspace).save()

print("\n\n\nĐã ghi vào Cassandra!\n\n\n")

# Dừng Spark
spark.stop()

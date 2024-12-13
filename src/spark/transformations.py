from pyspark.sql.functions import col, to_timestamp, year, month, dayofweek, hour, when
from pyspark.sql.functions import unix_timestamp, round, count

### Các transform dùng để clean data
def preprocess_missing_value(df):
    # Loại bỏ các hàng có nhiều giá trị null
    df = df.dropna(subset=["Start_Time", "End_Time", "Start_Lat", "Start_Lng"])

    # Điền giá trị mặc định cho các cột quan trọng
    df = df.fillna({
        "Temperature(F)": 60.0, 
        "Visibility(mi)": 10.0, 
        "Wind_Speed(mph)": 5.0
    })

    return df


### Các transform biến đổi ra bảng mới/cột mới -> phục vụ đầu vào cho dashboard
def convert_tO_timestamp(df):
    df = df.withColumn("Start_Time", to_timestamp("Start_Time"))

    # Trích xuất phần tử thời gian
    df = df.withColumn("Year", year(col("Start_Time"))) \
        .withColumn("Month", month(col("Start_Time"))) \
        .withColumn("DayOfWeek", dayofweek(col("Start_Time"))) \
        .withColumn("Hour", hour(col("Start_Time")))
    
    return df

def count_by_severity(df):
    return df.groupBy("Severity").count().orderBy("count", ascending=False)

def get_accident_duration(df):
    return df.withColumn("Duration_Minutes", 
                   round((unix_timestamp("End_Time") - unix_timestamp("Start_Time")) / 60, 2))

def get_avg_distance_by_sevirity(df):
    return  df.groupBy("Severity") \
                .agg({"Distance(mi)": "avg"}) \
                .withColumnRenamed("avg(Distance(mi))", "Avg_Distance") \
                .orderBy("Avg_Distance", ascending=False)

def get_proportion_weatherConditions(df):
    # Đếm sự cố theo thời tiết
    df_weather = df.groupBy("Weather_Condition").agg(count("*").alias("Count"))

    # Tính tỷ lệ phần trăm
    total_accidents = df.count()
    df_weather = df_weather.withColumn("Percentage", (col("Count") / total_accidents) * 100) \
                        .orderBy("Percentage", ascending=False)
    
    return df_weather

def get_num_accidents_by_lat_lng(df):
    # Làm tròn tọa độ để nhóm vào các ô lưới
    df_geo = df.withColumn("Grid_Lat", round(col("Start_Lat"), 2)) \
            .withColumn("Grid_Lng", round(col("Start_Lng"), 2))

    # Đếm số sự cố trong mỗi ô lưới
    df_geo_count = df_geo.groupBy("Grid_Lat", "Grid_Lng").count().orderBy("count", ascending=False)

    return df_geo_count

def get_num_accidents_by_dow_severity(df):
    return df.groupBy("DayOfWeek", "Severity").agg(count("*").alias("Count")) \
                            .orderBy("DayOfWeek", "Severity")

def get_num_accidents_by_streetCondition(df):
    return df.groupBy("Traffic_Signal", "Junction", "Stop") \
               .count().orderBy("count", ascending=False)

def classify_weatherCondition(df):

    return df.withColumn(
        "Weather_Group", 
        when(col("Weather_Condition").like("%Rain%"), "Rain") \
        .when(col("Weather_Condition").like("%Snow%"), "Snow") \
        .when(col("Weather_Condition").like("%Clear%"), "Clear") \
        .when(col("Weather_Condition").like("%Fog%"), "Fog") \
        .otherwise("Other")
    )


def transformation(df):

    return
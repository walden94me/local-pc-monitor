import pika
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# 1. 初始化 InfluxDB 客户端 (请替换为你在网页里生成的实际值)
token = "CtDXZ4X1LrgXLDEgtWBg9TelWyyeg39g4ADgS22I71Kho9-dTWrITEyTyi2-hiWlvPjLa7UhXn4CZ6PqaotmNw=="
org = "my-home"
bucket = "computer_monitor"
influx_client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# 2. 连接 RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='computer_metrics')

def callback(ch, method, properties, body):
    metrics = json.loads(body)
    print(f" [o] 收到数据: CPU {metrics['cpu_usage']}%")
    
    # 3. 构建时序数据点 (Point) 并写入 InfluxDB
    point = Point("system_metrics") \
        .tag("host", "local_computer") \
        .field("cpu", float(metrics['cpu_usage'])) \
        .field("memory", float(metrics['memory_usage']))
    
    write_api.write(bucket=bucket, org=org, record=point)

channel.basic_consume(queue='computer_metrics', on_message_callback=callback, auto_ack=True)
print(' [*] 消费者已启动，正在将 DMQ 数据转存至 InfluxDB...')
channel.start_consuming()

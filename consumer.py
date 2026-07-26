import pika
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

token = "CtDXZ4X1LrgXLDEgtWBg9TelWyyeg39g4ADgS22I71Kho9-dTWrITEyTyi2-hiWlvPjLa7UhXn4CZ6PqaotmNw=="
org = "my-home"
bucket = "computer_monitor"
influx_client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 队列也要声明持久化，两边保持一致
channel.queue_declare(queue='pc_system_metrics', durable=True)

def callback(ch, method, properties, body):
    try:
        metrics = json.loads(body)
        print(f" [o] 收到数据: CPU {metrics['cpu_usage']}%")

        point = Point("system_metrics") \
            .tag("host", "local_computer") \
            .field("cpu", float(metrics['cpu_usage'])) \
            .field("memory", float(metrics['memory_usage']))

        write_api.write(bucket=bucket, org=org, record=point)
        # ========== 写入Influx成功后，手动ACK告诉MQ删除消息 ==========
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # 写入失败，消息重回队列，下次继续消费
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        print("写入异常，消息重回队列：", e)

# ========== auto_ack=False 关闭自动确认 ==========
channel.basic_consume(queue='pc_system_metrics', on_message_callback=callback, auto_ack=False)

# 限制单次拉取数量，避免瞬间大量消息压垮InfluxDB
channel.basic_qos(prefetch_count=10)

print(' [*] 消费者已启动，持久化模式，堆积消息可断点续消费')
channel.start_consuming()

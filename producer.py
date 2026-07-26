import pika
import json
import psutil
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# ========== 改动1：声明持久化队列 durable=True ==========
channel.queue_declare(queue='pc_system_metrics', durable=True)

print("开始采集并发送监控数据...")
try:
    while True:
        metrics = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "timestamp": time.time()
        }
        # ========== 改动2：消息标记为持久化 delivery_mode=2 ==========
        props = pika.BasicProperties(delivery_mode=2)
        channel.basic_publish(
            exchange='',
            routing_key='pc_system_metrics',
            body=json.dumps(metrics),
            properties=props
        )
        print(f" [x] 已发送: {metrics}")
        time.sleep(2)
except KeyboardInterrupt:
    connection.close()

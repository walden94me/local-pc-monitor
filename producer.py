import pika
import json
import psutil
import time

# 1. 连接到本地 RabbitMQ 服务
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. 声明一个名为 'computer_metrics' 的队列
channel.queue_declare(queue='computer_metrics')

print("开始采集并发送监控数据...")
try:
    while True:
        # 采集数据
        metrics = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "timestamp": time.time()
        }
        
        # 3. 将数据转换为 JSON 并推送到队列
        channel.basic_publish(
            exchange='',
            routing_key='computer_metrics',
            body=json.dumps(metrics)
        )
        print(f" [x] 已发送: {metrics}")
        time.sleep(2)  # 每2秒采集一次
except KeyboardInterrupt:
    connection.close()

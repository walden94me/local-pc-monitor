# 方案一：psutil获取性能指标

1. 生产者：psutil 采集 CPU / 内存 → 发给 RabbitMQ 队列

2. 消费者：监听 RabbitMQ 队列，拿到监控数据，写入 InfluxDB 时序数据库



启动rabitmq

`docker start rabbitmq`



```bash
# 用docker 启动 rabbitmq 和 InfluxDB
docker start rabbitmq
docker ps | grep rabbitmq
# 后台：http://localhost:15672

docker start influxdb
docker ps | grep influxdb
# 后台：http://localhost:8086

# systemd系统服务托管
sudo systemctl start grafana-server


# dmqEnv 虚拟环境，执行生产脚本
/home/liang/pyenv/dmqEnv/bin/python /home/liang/local-monitor/producer.py



```



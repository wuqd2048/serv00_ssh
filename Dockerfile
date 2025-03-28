# 使用官方Python基础镜像
FROM python:3.9-slim

# 安装依赖和cron服务
RUN apt-get update && apt-get install -y cron && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制脚本和配置文件
COPY ssh_client.py .
COPY ssh_accounts.yaml .

# 安装Python依赖
RUN pip install paramiko pyyaml socket

# 创建定时任务文件
# 修改Cron任务（添加@reboot触发）
# 修改定时任务输出到标准输出
RUN echo "@reboot root /usr/local/bin/python /app/ssh_client.py >/proc/1/fd/1 2>&1\n\
* * * * 5 root /usr/local/bin/python /app/ssh_client.py >/proc/1/fd/1 2>&1" > /etc/cron.d/ssh-cron

# 修改启动命令
CMD cron && tail -f /dev/null
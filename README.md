1、根据Dockerfile生成镜像。

docker build -t ssh-client .

2、执行容器，生成容器时会自动执行登录一次。
sudo docker run -d -v /volume1/ActiveBackupforBusiness/serv00:/app --name ssh-scheduler ssh-client

3、文件ssh_accounts.yaml、ssh_client.py需要在同一个目录。

4、ssh_accounts.yaml账号地址
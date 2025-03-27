docker build -t ssh-client .

sudo docker run -d -v /volume1/ActiveBackupforBusiness/serv00:/app --name ssh-scheduler ssh-client
import os  # 新增模块导入
import paramiko
import yaml
from datetime import datetime  # 新增导入

def load_ssh_accounts(yaml_path):
    try:  # 添加异常处理
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"配置文件 {yaml_path} 不存在")
        exit(1)
    except yaml.YAMLError as e:
        print(f"YAML解析错误: {str(e)}")
        exit(1)

def ssh_login(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在连接 {username}@{hostname}:{port}...")
        client.connect(hostname, port=port, username=username, password=password)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {username}@{hostname} 登录成功！")
        
        # 示例：执行简单命令
        cmd = 'lsb_release -a || uname -a'
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在执行命令: {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # 新增命令输出日志
        output = stdout.read().decode()
        errors = stderr.read().decode()
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 命令输出:")
        print(f"[stdout]\n{output}")
        if errors:
            print(f"[stderr]\n{errors}")
            
    except paramiko.AuthenticationException:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {username}@{hostname} 认证失败")
    except paramiko.SSHException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {username}@{hostname} 连接失败: {str(e)}")
    finally:
        client.close()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 连接已关闭")

# 在文件顶部添加datetime导入
import os
import paramiko
import yaml
from datetime import datetime  # 新增导入

if __name__ == "__main__":
    # 自动生成跨平台路径
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),  # 获取当前脚本绝对路径
        "ssh_accounts.yaml"
    )
    
    accounts = load_ssh_accounts(config_path)
    
    # 轮流尝试所有账号
    for account in accounts:
        ssh_login(
            hostname=account['hostname'],
            port=account.get('port', 22),  # 默认使用22端口
            username=account['username'],
            password=account['password']
        )
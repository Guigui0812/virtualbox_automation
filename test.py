import paramiko

try:
    paramiko.util.log_to_file('paramiko.log')
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # SSH to VM
    client.connect(hostname="192.168.146.57", port=22, username="guillaume", password="Kolonel0812!", timeout=10)
    (stdin, stdout, stderr) = client.exec_command("uname")

    print(stdout.readlines())

except Exception as e:

    print(f"SSH connection failed: {e}")
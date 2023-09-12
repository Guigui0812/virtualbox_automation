import subprocess
import paramiko
import re

def get_vm_network_type(vm_name):
    try:
        result = subprocess.run(["VBoxManage", "showvminfo", vm_name], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

        if result.returncode == 0:
            lines = result.stdout.split("\n")
            for line in lines:
                if re.match(r"NIC \d:", line):
                    if "Bridged" in line:
                        return "Bridged"
                    elif "NAT" in line:
                        return "NAT"
                    elif "Host-only" in line:
                        return "Host-only"
                    else:
                        return "Unknown"

    except Exception as e:
        print(f"Error: {e}")
        return "Unknown"

def get_vm_ip(vm_name):
    try:
        result = subprocess.run(["VBoxManage", "guestproperty", "get", vm_name, "/VirtualBox/GuestInfo/Net/0/V4/IP"],stdout=subprocess.PIPE,text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split("\n")
            for line in lines:
                if line.startswith("Value: "):
                    ip_address = line[len("Value: "):]
                    return ip_address.strip()
                
    except Exception as e:
        print(f"Error: {e}")
    return None

def ssh_to_vm(vm_ip, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip, username=username, password=password)

        # You can perform SSH operations here

        ssh_client.close()
        return True
    except Exception as e:
        print(f"SSH connection failed: {e}")
        return False

# Replace "VM_NAME" with your VM's name
vm_name = "Your_VM_Name"

# Get the VM network type
network_type = get_vm_network_type(vm_name)
print(f"VM Network Type: {network_type}")

# Check if it's a Bridged network
if network_type == "Bridged":
    vm_ip = get_vm_ip(vm_name)
    if vm_ip:
        print(f"VM IP address: {vm_ip}")
        # Replace with your VM's SSH credentials
        username = "Your_SSH_Username"
        password = "Your_SSH_Password"
        if ssh_to_vm(vm_ip, username, password):
            print("SSH connection successful")
        else:
            print("SSH connection failed")
    else:
        print("Unable to retrieve VM IP address")
elif network_type == "NAT":
    print("VM is in NAT mode. SSH may require port forwarding.")
else:
    print("Unknown network type or VM not found.")
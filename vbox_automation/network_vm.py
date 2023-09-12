import subprocess
import paramiko
import re

# Faire une boucle pour envoyé les commandes à la VM à la suite comme dans le terminal
# Si "Exit" alors on sort de la boucle, on ferme la connexion et on retourne au menu principal

# Obtenir le type de réseau de la VM
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

# Obtenir l'IP de la VM
def get_vm_ip(vm_name):
    try:
        result = subprocess.run(["VBoxManage", "guestproperty", "get", vm_name, "/VirtualBox/GuestInfo/Net/0/V4/IP"],stdout=subprocess.PIPE,text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split("\n")
            for line in lines:
                if line.startswith("Value: "):
                    ip_address = line[len("Value: "):]
                    print(f"IP de la VM : {ip_address}")
                    return ip_address.strip()
                
    except Exception as e:
        print(f"Error: {e}")
    return None

# SSH to VM
def ssh_to_vm(vm_ip, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.connect(vm_ip, port=22, username=username, password=password)

        # You can perform SSH operations here

        ssh_client.close()
        return True
    
    except Exception as e:
        print(f"SSH connection failed: {e}")
        return False

def connect_to_vm(vm_name):

    # Get the VM network type
    network_type = get_vm_network_type(vm_name)
    print(f"Type de réseau de la VM : {network_type}")

    # Check if it's a Bridged network
    if network_type == "Bridged":
        vm_ip = get_vm_ip(vm_name)
        print(f"IP de la VM : ")

        if vm_ip:
            username = "guillaume"
            password = "Kolonel0812!"
            if ssh_to_vm("192.168.146.57", username, password):
                print("Vous êtes connecté à la VM.")
            else:
                print("La connexion SSH a échoué")
        else:
            print("Impossible de se connecter à la VM.")
    elif network_type == "NAT":
        print("VM is in NAT mode. SSH may require port forwarding.")

        # Ajouter la connexion avec le port à spécifier + préciser que l'IP est celle de la machine hôte

    else:
        print("Unknown network type or VM not found.")
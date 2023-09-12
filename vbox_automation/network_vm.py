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

# Prompt SSH pour la connexion à la VM et exécution de commandes
def ssh_to_vm(vm_ip, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(vm_ip, port=22, username=username, password=password)

        connection_open = True

        while connection_open:
            command = input("Entrez une commande : ")
            if command == "Exit":
                connection_open = False
            else:
                stdin, stdout, stderr = ssh_client.exec_command(command)
                print(stdout.read().decode())
                print(stderr.read().decode())

        ssh_client.close()
        return True
    
    except Exception as e:
        print(f"SSH connection failed: {e}")

def connect_to_vm(vm_name):

    try:
        host = ""
        username = ""
        password = ""

        print("Entrez les informations de connexion à la VM :")

        while host == "" :
            host = input("Adresse IP de la VM : ")
        
        while username == "" :
            username = input("Nom d'utilisateur : ")
        
        while password == "" :
            password = input("Mot de passe : ")
        
        ssh_to_vm(host, username, password)
    
    except Exception as e:
        print(f"Error: {e}")
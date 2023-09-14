import subprocess
import paramiko
import re

# Faire une boucle pour envoyé les commandes à la VM à la suite comme dans le terminal
# Si "Exit" alors on sort de la boucle, on ferme la connexion et on retourne au menu principal

### Fonctions permettant de récupérer les informations réseau d'une VM ###

# Obtenir le type de réseau de la VM
def get_vm_network_type(vm_name):

    try:
        result = subprocess.run(["VBoxManage", "showvminfo", vm_name], stdout=subprocess.PIPE, text=True)

        if result.returncode == 0:
            lines = result.stdout.split("\n")
            for line in lines:
                if "NIC" in line:
                    NIC_line= line.split(",")[1].strip()
                    network_type = NIC_line.split(":")[1]
                    print(f"Type de réseau de la VM : {network_type.strip()}")
                    return network_type.strip()


    except Exception as e:
        print("Impossible de récupérer le type de réseau de la VM :", str(e))
    
    return None

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
        print("Impossible de récupérer l'adresse IP de la VM :", str(e))
    
    return None

### Fonctions permettant de configurer une VM en réseau interne ###

def configure_internal_network(vm_name, interface_nb):

    try:
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{interface_nb}", "intnet"])
    
    except Exception as e:
        print("La configuration du réseau interne a échoué :", str(e))

### Fonctions permettant de configurer une VM en Host-Only ###

def create_hostonly_network():

    try:
        subprocess.run(["VBoxManage", "hostonlyif", "create"])

    except Exception as e:
        print("La création du réseau Host-Only a échoué :", str(e))

def get_hostonly_networks():

    try:
        result = subprocess.run(["VBoxManage", "list", "hostonlyifs"], text=True, stdout=subprocess.PIPE)

        hostonly_networks = []
        lines = result.stdout.split("\n")

        for line in lines:
            if "Name:" in line:
                network = line.split(":")[1].strip()
                hostonly_networks.append(network)
        return hostonly_networks
    
    except Exception as e:
        print("La récupération des réseaux Host-Only a échoué :", str(e))

def configure_hostonly_network(vm_name, interface_hostonly, interface_nb):

    try:
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{interface_nb}", "hostonly", "--hostonlyadapter1", interface_hostonly])
    except Exception as e:
        print("La configuration du réseau Host-Only a échoué :", str(e))

### Fonctions permettant de configurer une VM en NAT ###

def configure_nat_port_forwarding(vm_name, guest_port, host_port, rule_name, number_of_rules):

    try:
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--natpf{number_of_rules}", f"{rule_name},tcp,,{host_port},,{guest_port}"])
    except Exception as e:
        print("La configuration du port forwarding a échoué :", str(e))

def configure_nat_network(vm_name, interface_nb, network_name):

    try:
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{interface_nb}", "natnetwork", "--nat-network1", network_name])
    except Exception as e:
        print("La configuration du NAT a échoué :", str(e))

# Fonctions permettant de configurer une VM en Bridge

def configure_bridge_network(vm_name, host_interface, interface_nb):

    print(f"Interface numéro {interface_nb} : {host_interface}")

    try:
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{interface_nb}", "bridged", "--bridgeadapter1", host_interface])
    except Exception as e:
        print("La configuration du Bridge a échoué :", str(e))

def configure_intnet_network(vm_name, interface_nb, network_name):

    try:
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{interface_nb}", "intnet", "--intnet1", network_name])
    except Exception as e:
        print("La configuration du réseau interne a échoué :", str(e))

def configure_simple_nat(vm_name, interface_nb):

    try:
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{interface_nb}", "nat"])

    except Exception as e:
        print("La configuration du NAT a échoué :", str(e))

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
        print(f"Impossible de se connecter à la VM avec SSH :", str(e))
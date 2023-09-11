import subprocess
import re
import os
import psutil

# Chemin ou stocker à ajouter
# Chemin où stoker la machine virtuelle
# Faire les conversions de Mo en Go
# utiliser unattered pour les options de la VM
# Fixer les {vm_name} dans les commandes
# Cas où nom est déjà pris
# check si le fichier est bien un iso

# Fonction pour récupérer les OS supportés
def get_supported_os_types():
    try:
        # Execute la commande VBoxManage pour lister les types de systèmes d'exploitation supportés
        result = subprocess.run(["VBoxManage", "list", "ostypes"], text=True)

        # Récupérer les systèmes d'exploitation supportés ligne par ligne
        lines = result.stdout.splitlines()
        os_types = []

        # Stockage du nom des systèmes d'exploitation dans une liste
        for line in lines:
            if "ID:" in line:
                os = line.split(":")[1].strip()
                os_types.append(os)
        return os_types
    
    except Exception as e:
        print("An error occurred:", str(e))

# Fonction permettant de définir le nom et l'OS
def set_name_and_os_type():

    vm_name = input("Nom de la machine virtuelle : ")

    while vm_name == "" or re.match("^[a-zA-Z0-9_]*$", vm_name) == False:
        print("Le nom de la machine virtuelle ne peut pas être vide ou contenir des caractères spéciaux.")
        vm_name = input("Nom de la machine virtuelle : ")

    #os_types = get_supported_os_types()
    '''
    os_type = input("Type de système d'exploitation (exécutez la commande 'VBoxManage list ostypes' pour voir la liste des systèmes d'exploitation supportés) : ")

    while os_type not in os_types:
        print("Type de système d'exploitation invalide.")
        os_type = input("Nom de l'OS : ")
    '''
    subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--register"])

    return vm_name

# Fonction pour configurer la machine virtuelle selon les paramètres définis par l'utilisateur
def set_vm_config(vm_name):

        path_to_iso = input("Chemin vers le fichier ISO : ")

        # Vérifier les conditions d'entrée pour le chemin vers le fichier ISO
        while path_to_iso == "" or os.path.isfile(path_to_iso.encode('unicode_escape')) == False or path_to_iso.endswith(".iso") == False:
            print("Le chemin vers le fichier ISO est invalide.")
            path_to_iso = input("Chemin vers le fichier ISO : ")

        nb_cpu = input("Nombre de processeurs : ")

        # Vérifier les conditions d'entrée pour le nombre de processeurs
        while nb_cpu == "" or nb_cpu.isdigit() == False or nb_cpu == "0" or int(nb_cpu) > psutil.cpu_count():
            print("Le nombre de processeurs doit être un nombre entier.")
            nb_cpu = input("Nombre de processeurs : ")

        memory_mb = input("Quantité de mémoire vive (en Mo) : ")

        # Vérifier les conditions d'entrée pour la quantité de mémoire vive
        while memory_mb == "" or memory_mb.isdigit() == False or memory_mb == "0":
            print("La quantité de mémoire vive doit être un nombre entier.")
            memory_mb = input("Quantité de mémoire vive (en Mo) : ")

        disk_size_mb = input("Taille du disque dur (en Mo) : ")

        # Vérifier les conditions d'entrée pour la taille du disque dur
        while disk_size_mb == "" or disk_size_mb.isdigit() == False or disk_size_mb == "0":
            print("La taille du disque dur doit être un nombre entier.")
            disk_size_mb = input("Taille du disque dur (en Mo) : ")

        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--memory", memory_mb, "--cpus", nb_cpu])
        subprocess.run(["VBoxManage", "createhd", "--filename", "{vm_name}/{vm_name}.vdi", "--size", str(disk_size_mb)])


        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--bootable", "on"])
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", "{vm_name}/{vm_name}.vdi"])  
        # Attacher l'ISO pour l'installation du système d'exploitation

        #VBoxManage storagectl "$vm_name" --name "IDE Controller" --add ide
        #VBoxManage storageattach "$vm_name" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium "$iso_path"

        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"])
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", path_to_iso])

def set_vm_network(vm_name):

    config_network = True

    while config_network == True:

        print("Sélectionnez un type de réseau:")
        print("1 - NAT")
        print("2 - Bridged")
        print("3 - Host-only")
        print("4 - Internal")
        print("5 - NAT Network")

        option = input("Entrez votre choix: ")

        while option not in ["1", "2", "3", "4", "5"]:
            print("Option invalide.")
            option = input("Entrez votre choix: ")

        match option:
            case "1":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "nat"])
            case "2":

                interface = input("Entrez le nom de l'interface réseau à utiliser pour le mode bridged : ")
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "bridged", "--bridgeadapter1", "enp0s3"])
            case "3":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "hostonly"])
            case "4":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "intnet"])
            case "5":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "natnetwork"])
        
        network_bool = input("Voulez-vous configurer une autre interface réseau ? 1 - Oui, 2 - Non : ")

        while network_bool not in ["1", "2"]:
            network_bool = input("Voulez-vous configurer une autre interface réseau ? 1 - Oui, 2 - Non : ")

        if network_bool == "2":
            config_network = False

        return option
        

# Fonction pour créer une machine virtuelle selon les paramètres définis par l'utilisateur
def create_vm():

    try:
        print("#############################################")
        print("##                                         ##")
        print("##  Bienvenue dans le configurateur de VM  ##")
        print("##                                         ##")
        print("#############################################")

        vm_name = set_name_and_os_type()
        set_vm_config(vm_name)

        network_type = set_vm_network(vm_name)

        # Execute les commandes VBoxManage pour créer la machine virtuelle selon les paramètres définis par l'utilisateur

        # VBoxManage createvm --name OracleLinux6Test --ostype Oracle_64 --register
        # VBoxManage modifyvm OracleLinux6Test --cpus 2 --memory 2048 --vram 12

        if network_type == "bridged":
            interface = input("Entrez le nom de l'interface réseau à utiliser pour le mode bridged : ")
            subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", network_type, "--bridgeadapter1", interface])

        else:
            subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", network_type])
        
        # Lancement de la machine virtuelle en mode headless (sans interface graphique)
        subprocess.run(["VBoxManage", "startvm", vm_name, "--type", "headless"])

        print(f"Virtual machine '{vm_name}' configured successfully.")

    except Exception as e:
        print("An error occurred:", str(e))
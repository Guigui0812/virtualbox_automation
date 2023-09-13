import os
import psutil
import re
import vbox_automation
import subprocess

# Vérifier que les valeurs sont des entiers

# Pour le NAT network : VBoxManage natnetwork add --netname natnet1 --network "192.168.22.0/24" --enable

# Obtenir une liste des machines virtuelles sans les guillemets
def get_vm_list_clean():

    vm_list = vbox_automation.get_vm()
    vm_list_clean = []

    # Supprimer les guillemets
    for vm in vm_list:
        vm = vm.replace('"', '')
        vm_list_clean.append(vm)

    return vm_list_clean

# Afficher la liste des machines virtuelles
def display_vm_list():

    print("Liste des machines virtuelles :")

    vm_list = vbox_automation.get_vm_list_clean()

    for vm in vm_list:
        vm = vm.replace('"', '')
        print(" - " + vm)

# Menu pour cloner une machine virtuelle
def clone_vm_menu():

    display_vm_list()

    vm_name = input("Nom de la machine virtuelle à cloner : ")

    vm_list_clean = get_vm_list_clean()

    # Vérifier que la machine virtuelle existe
    while vm_name == "" or vm_name not in vm_list_clean:
        print("La machine virtuelle n'existe pas.")
        vm_name = input("Nom de la machine virtuelle à cloner : ")

    clone_name = input("Nom du clone : ")

    # Vérifier les conditions d'entrée pour le nom du clone
    while clone_name == "" or clone_name in vbox_automation.get_vm():
        print("Le nom du clone ne peut pas être vide ou déjà utilisé.")
        clone_name = input("Nom du clone : ")

    # Cloner la machine virtuelle
    return_code = vbox_automation.clone_vm(vm_name, clone_name)

    if return_code == 0:
        print("La machine virtuelle a été clonée avec succès.")

# Obtenir les interfaces réseau de la machine hôte pour configurer le bridge
def get_host_network_interfaces():

    result = subprocess.run(["ipconfig", "/all"], stdout=subprocess.PIPE, text=True)

    interfaces = []

    print(result.stdout)

    for line in result.stdout.split("\n"):
        if "Description" in line:
            interfaces.append(line.split(":")[1].strip())

    return interfaces

# Fonction pour configurer le port forwarding
def port_forwarding_menu(vm_name):

    print("##### Configuration du port forwarding #####")

    continue_conf = True
    count_rule = 1

    while continue_conf == True:

        rule_name = input("Nom de la règle : ")

        # Le nom ne peut pas être vide ou contenir des caractères spéciaux
        while rule_name == "" or re.match("^[a-zA-Z0-9_]*$", rule_name) == False:
            print("Le nom de la règle ne peut pas être vide ou contenir des caractères spéciaux.")
            rule_name = input("Nom de la règle : ")

        # Création de la règle de port forwarding
        guest_port = input("Port de la machine virtuelle : ")

        while guest_port == "" or guest_port.isdigit() == False or int(guest_port) > 65535 or int(guest_port) <= 0:
            print("Le port est invalide.")
            guest_port = input("Port de la machine virtuelle : ")
        
        host_port = input("Port de l'hôte : ")

        while host_port == "" or host_port.isdigit() == False or int(host_port) > 65535 or int(host_port) <= 0:
            print("Le port est invalide.")
            host_port = input("Port de l'hôte : ")

        vbox_automation.configure_nat_port_forwarding(vm_name, guest_port, host_port, rule_name, count_rule)

        choice = input("Voulez-vous configurer une autre règle de port forwarding ? 1 - Oui, 2 - Non : ")

        while choice not in ["1", "2"]:
            print("Option invalide.")
            choice = input("Voulez-vous configurer une autre règle de port forwarding ? 1 - Oui, 2 - Non : ")

        if choice == "2":
            continue_conf = False

        count_rule += 1

# Menu de configuration du mode host-only
def vm_hostonly_menu(vm_name, interface_count):

    print("##### Configuration du mode host-only #####")

    print("Créer un nouveau réseau host-only ? 1 - Oui, 2 - Non : ")

    option = input("Entrez votre choix : ")

    while option not in ["1", "2"]:
        print("Option invalide.")
        option = input("Entrez votre choix : ")

    if option == "1":
        # Création du réseau host-only
        vbox_automation.create_hostonly_network()
    
    # Obtenir les interfaces réseau host-only
    hostonly_networks = vbox_automation.get_hostonly_networks()

    # Afficher les interfaces réseau host-only
    for network in hostonly_networks:
        print(network)

    # Demander à l'utilisateur de choisir l'interface réseau host-only à utiliser
    interface_hostonly = input("Entrez le nom de l'interface réseau host-only à utiliser : ")

    # Vérifier les conditions d'entrée pour le nom de l'interface réseau host-only
    while interface_hostonly == "" or interface_hostonly not in hostonly_networks:
        print("Le nom de l'interface réseau host-only est invalide.")
        interface_hostonly = input("Entrez le nom de l'interface réseau host-only à utiliser : ")

    # Configuration de l'interface réseau host-only
    vbox_automation.configure_hostonly_network(vm_name, interface_hostonly, interface_count)

def vm_bridge_menu(vm_name, interface_count):

    print("##### Configuration du mode bridged #####")

    interfaces = get_host_network_interfaces()
    interface_count = 1

    for interface in interfaces:
        print(f"{interface_count} - {interface}")
        interface_count += 1
    
    interface = input("Entrez le numéro de l'interface réseau à utiliser pour le mode bridged : ")

    # Vérifier les conditions d'entrée pour le numéro de l'interface réseau
    while interface == "" or interface.isdigit() == False or int(interface) > len(interfaces) or int(interface) <= 0:
        print("Le numéro de l'interface réseau est invalide.")
        interface = input("Entrez le numéro de l'interface réseau à utiliser pour le mode bridged : ")

    vbox_automation.configure_bridge_network(vm_name, interfaces[int(interface) - 1], interface_count)

# Menu pour configurer le réseau de la machine virtuelle
def vm_network_menu(vm_name):

    config_network = True
    interface_count = 1

    while config_network == True and interface_count <= 4:

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

        # Appel des fonctions pour configurer le réseau selon l'option choisie

        match option:
            case "1":

                # Création de l'inteface NAT
                vbox_automation.configure_simple_nat(vm_name, interface_count)

                # Configuration du port forwarding
                port_forwarding_menu(vm_name)
                
            case "2":
                vm_bridge_menu(vm_name, interface_count)

            case "3":
                vm_hostonly_menu(vm_name, interface_count)


                # A FAIRE

               
    
        network_bool = input("Voulez-vous configurer une autre interface réseau ? 1 - Oui, 2 - Non : ")

        while network_bool not in ["1", "2"]:
            network_bool = input("Voulez-vous configurer une autre interface réseau ? 1 - Oui, 2 - Non : ")

        if network_bool == "2":
            config_network = False

        interface_count += 1

# Menu pour configurer les propriétés de la machine virtuelle
def vm_properties_menu():

    vm_list_clean = get_vm_list_clean()

    vm_name = input("Nom de la machine virtuelle : ")

    # Vérifier les conditions d'entrée pour le nom de la machine virtuelle
    while vm_name == "" or re.match("^[a-zA-Z0-9_]*$", vm_name) == False or vm_name in vm_list_clean:
        print("Le nom de la machine virtuelle ne peut pas être vide, contenir des caractères spéciaux ou être déjà utilisé.")
        vm_name = input("Nom de la machine virtuelle : ")

    path_to_iso = input("Chemin vers le fichier ISO : ")

    # Vérifier les conditions d'entrée pour le chemin vers le fichier ISO
    while path_to_iso == "" or os.path.isfile(path_to_iso.encode('unicode_escape')) == False or path_to_iso.endswith(".iso") == False:
        print("Le chemin vers le fichier ISO est invalide.")
        path_to_iso = input("Chemin vers le fichier ISO : ")

    nb_cpu = input("Nombre de processeurs : ")

    # Vérifier les conditions d'entrée pour le nombre de processeurs
    while nb_cpu == "" or nb_cpu.isdigit() == False or int(nb_cpu) >= psutil.cpu_count() or int(nb_cpu) <= 0:
        print("Le nombre de processeurs doit être un nombre entier.")
        nb_cpu = input("Nombre de processeurs : ")

    memory_mb = input("Quantité de mémoire vive (en Mo) : ")

    # Vérifier les conditions d'entrée pour la quantité de mémoire vive
    while memory_mb == "" or memory_mb.isdigit() == False or memory_mb < "512":
        print("La quantité de mémoire vive doit être un nombre entier.")
        memory_mb = input("Quantité de mémoire vive (en Go) : ")

    disk_size_gb = input("Taille du disque dur (en Go) : ")

    # Vérifier les conditions d'entrée pour la taille du disque dur
    while disk_size_gb == "" or disk_size_gb.isdigit() == False or disk_size_gb < "8":
        print("La taille du disque dur doit être un nombre entier.")
        disk_size_gb = input("Taille du disque dur (en Go) : ")

    # Création de la machine virtuelle
    vbox_automation.set_vm_config(vm_name, path_to_iso, nb_cpu, memory_mb, disk_size_gb)
    
    # Configuration du réseau de la machine virtuelle
    vm_network_menu(vm_name)

    # Démarrage de la machine virtuelle
    return_code = vbox_automation.run_vm(vm_name)

    if return_code == 0:
        print("La machine virtuelle a été créée avec succès.")

# Menu principal
def main_menu():
   
    loop_menu = True

    while loop_menu == True:
    
        print("#############################################")
        print("##                                         ##")
        print("##  Bienvenue sur Virtual Machine Manager  ##")
        print("##                                         ##")
        print("#############################################")

        print("Sélectionnez une option:")
        print("1 - Créer une nouvelle machine")
        print("2 - Lister les machines")
        print("3 - Cloner une machine")
        print("4 - Se connecter à une machine")
        print("5 - Démarrer une machine")
        print("6. Quitter")

        option = input("Entrez votre choix: ")

        while option not in ["1", "2", "3", "4", "5", "6"]:
            print("Ceci n'est pas une option.")
            option = input("Entrez votre choix: ")

        if option == "1":
            vm_properties_menu()
        elif option == "2":
            display_vm_list()
        elif option == "3":
            clone_vm_menu()
        elif option == "4":
            vm_name = input("Nom de la machine virtuelle : ")
            vbox_automation.connect_to_vm(vm_name)
        elif option == "5":
            vm_name = input("Nom de la machine virtuelle : ")
            display_vm_list()
            vbox_automation.run_vm(vm_name)
        elif option == "6":
            loop_menu = False
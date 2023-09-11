import os
import psutil
import re
import vbox_automation

def get_vm_list_clean():

    vm_list = vbox_automation.get_vm()
    vm_list_clean = []

    for vm in vm_list:
        vm = vm.replace('"', '')
        vm_list_clean.append(vm)

    return vm_list_clean


def display_vm_list():

    print("Liste des machines virtuelles :")

    vm_list = vbox_automation.get_vm()

    for vm in vm_list:
        vm = vm.replace('"', '')
        print(" - " + vm)

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

def vm_network_menu(vm_name):

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
                vbox_automation.set_vm_network(vm_name, option)
            case "2":
                interface = input("Entrez le nom de l'interface réseau à utiliser pour le mode bridged : ")

                # Vérifier les conditions d'entrée pour le nom de l'interface réseau
                while interface == "" or interface not in psutil.net_if_addrs().keys():
                    print("Le nom de l'interface réseau est invalide.")
                    interface = input("Entrez le nom de l'interface réseau à utiliser pour le mode bridged : ")

                vbox_automation.set_vm_network(vm_name, option, interface)
            case "3":
                vbox_automation.set_vm_network(vm_name, option)
            case "4":
                vbox_automation.set_vm_network(vm_name, option)
            case "5":
                vbox_automation.set_vm_network(vm_name, option)
    
        network_bool = input("Voulez-vous configurer une autre interface réseau ? 1 - Oui, 2 - Non : ")

        while network_bool not in ["1", "2"]:
            network_bool = input("Voulez-vous configurer une autre interface réseau ? 1 - Oui, 2 - Non : ")

        if network_bool == "2":
            config_network = False

def vm_properties_menu():

    vm_list_clean = get_vm_list_clean()

    vm_name = input("Nom de la machine virtuelle : ")

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

    # Création de la machine virtuelle
    vbox_automation.set_vm_config(vm_name, path_to_iso, nb_cpu, memory_mb, disk_size_mb)
    
    # Configuration du réseau de la machine virtuelle
    vm_network_menu(vm_name)

    # Démarrage de la machine virtuelle
    return_code = vbox_automation.run_vm(vm_name)

    if return_code == 0:
        print("La machine virtuelle a été créée avec succès.")

def main_menu():
    print("#############################################")
    print("##                                         ##")
    print("##  Welcome to the Virtual Machine Manager ##")
    print("##                                         ##")
    print("#############################################")

    print("Sélectionnez une option:")
    print("1 - Créer une nouvelle machine")
    print("2 - Lister les machines")
    print("3 - Cloner une machine")
    print("4. Quitter")

    option = input("Entrez votre choix: ")

    while option not in ["1", "2", "3"]:
        print("Ceci n'est pas une option.")
        option = input("Entrez votre choix: ")

    if option == "1":
        vm_properties_menu()
    elif option == "2":
        display_vm_list()
    elif option == "3":
        clone_vm_menu()
    elif option == "4":
        exit()
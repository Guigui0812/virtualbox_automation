import subprocess

def select_network_type():

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

    if option == "1":
        return "nat"
    elif option == "2":
        return "bridged"
    elif option == "3":
        return "hostonly"
    elif option == "4":
        return "internal"
    elif option == "5":
        return "natnetwork"
    
def create_virtual_machine():

    try:
        # Demander les informations de la machine virtuelle 
        print("Entrez les informations de la machine virtuelle à créer :")
        vm_name = input("Nom de la machine virtuelle : ")
        os_type = input("Type de système d'exploitation : ")
        path_to_vdi = input("Chemin vers le fichier VDI : ")
        nb_cpu = input("Nombre de processeurs : ")
        memory_mb = input("Quantité de mémoire vive (en Mo) : ")
        disk_size_mb = input("Taille du disque dur (en Mo) : ")
        network_type = select_network_type()

        # Execute les commandes VBoxManage pour créer la machine virtuelle selon les paramètres définis par l'utilisateur

        # VBoxManage createvm --name OracleLinux6Test --ostype Oracle_64 --register
        # VBoxManage modifyvm OracleLinux6Test --cpus 2 --memory 2048 --vram 12
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--ostype", os_type, "--register"])
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--memory", memory_mb, "--cpus", nb_cpu])
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", network_type])


        subprocess.run(["VBoxManage", "createhd", "--filename", f"{vm_name}/{vm_name}.vdi", "--size", str(disk_size_mb)])
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--bootable", "on"])
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", path_to_vdi])     

        print(f"Virtual machine '{vm_name}' configured successfully.")

    except Exception as e:
        print("An error occurred:", str(e))


def list_virtual_machines():
    try:
        # Execute la commande VBoxManage pour lister les machines virtuelles
        result = subprocess.run(["VBoxManage", "list", "vms"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Split the output into lines and print each VM name
        vm_list = result.stdout.splitlines()
        for vm in vm_list:
            print(vm)
        else:
            print("Error:", result.stderr)

    except Exception as e:
        print("An error occurred:", str(e))


def main_menu():
    print("#############################################")
    print("##                                         ##")
    print("##  Welcome to the Virtual Machine Manager ##")
    print("##                                         ##")
    print("#############################################")

    print("Sélectionnez une option:")
    print("1 - Créer une nouvelle machine")
    print("2 - Lister les machines")
    print("3. Quitter")

    option = input("Entrez votre choix: ")

    while option not in ["1", "2", "3"]:
        print("Ceci n'est pas une option.")
        option = input("Entrez votre choix: ")

    if option == "1":
        create_virtual_machine()
    elif option == "2":
        list_virtual_machines()


if __name__ == "__main__":

    main_menu()
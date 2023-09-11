import subprocess
from vbox_automation import create_vm

def list_virtual_machines():
    try:
        # Execute la commande VBoxManage pour lister les machines virtuelles
        result = subprocess.run(["VBoxManage", "list", "vms"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Affiche les VM existantes ligne par ligne
        vm_list = result.stdout.splitlines()
        for vm in vm_list:
            print(vm)

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
        create_vm()
    elif option == "2":
        list_virtual_machines()


if __name__ == "__main__":

    main_menu()
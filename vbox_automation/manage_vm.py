import subprocess

# Code de la partie 4 pour utiliser la fonction d'importation de VM de VirtualBox
def import_vm(vm_path, vm_name):

    try:
        subprocess.run(["VBoxManage", "import", vm_path, "--vsys", "0", "--vmname", vm_name])

    except Exception as e:
        print("Une erreur est survenue lors de l'importation de la VM :", str(e))

# Code de la partie 4 pour utiliser la fonction de clonage de VM de VirtualBox
def clone_vm(vm_name, clone_name):

    try:
        # Cloner la machine virtuelle
        result = subprocess.run(["VBoxManage", "clonevm", vm_name, "--name", clone_name, "--register"])

        if result.returncode == 0:
            return run_vm(clone_name)
             
        return result.returncode

    except Exception as e:
        print("Une erreur est survenue lors du clonage de la VM :", str(e))

# Fonction pour lancer la machine virtuelle
def run_vm(vm_name):

    try:
        result = subprocess.run(["VBoxManage", "startvm", vm_name], text=True)
        return result.returncode
    except Exception as e:
        print("Un problème est survenu lors du démarrage de la VM :", str(e))

# Fonction pour lister les machines virtuelles
def get_vm():

    try:
        result = subprocess.run(["VBoxManage", "list", "vms"], text=True, stdout=subprocess.PIPE)
        lines = result.stdout.splitlines()

        vm_list = []

        for line in lines:
            if "{" in line:
                vm = line.split("{")[0].strip()
                vm_list.append(vm)
        return vm_list
    
    except Exception as e:
        print("Une erreur est survenue lors de la récupération de la liste des VM :", str(e))
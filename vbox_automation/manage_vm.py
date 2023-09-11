import subprocess

def clone_vm(vm_name, clone_name):

    try:
        # Cloner la machine virtuelle
        result = subprocess.run(["VBoxManage", "clonevm", vm_name, "--name", clone_name, "--register"])

        if result.returncode == 0:
            return run_vm(clone_name)
             
        return result.returncode

    except Exception as e:
        print("An error occurred:", str(e))

# Fonction pour lancer la machine virtuelle
def run_vm(vm_name):

    try:
        result = subprocess.run(["VBoxManage", "startvm", vm_name, "--type", "headless"])
        return result.returncode
    except Exception as e:
        print("An error occurred:", str(e))

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
        print("An error occurred:", str(e))
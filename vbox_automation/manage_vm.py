import subprocess

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
        result = subprocess.run(["VBoxManage", "list", "vms"], text=True)
        lines = result.stdout.splitlines()
        vm_list = []

        for line in lines:
            if "{" in line:
                vm = line.split("{")[0].strip()
                vm_list.append(vm)
        return vm_list
    
    except Exception as e:
        print("An error occurred:", str(e))
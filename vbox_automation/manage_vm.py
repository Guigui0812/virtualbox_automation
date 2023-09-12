import subprocess

def get_vm_network(vm_name):

    try:
        # Exécute la commande VBoxManage pour obtenir l'adresse IP
        result = subprocess.run(["VBoxManage", "guestproperty", "get", vm_name, "/VirtualBox/GuestInfo/Net/0/V4/IP"],stdout=subprocess.PIPE,text=True)

        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                if line.startswith("Value: "):
                    ip_address = line[len("Value: "):]
                    print(f"IP address: {ip_address}")
        else:
            print("Error while retrieving VM IP:")
            print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")

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
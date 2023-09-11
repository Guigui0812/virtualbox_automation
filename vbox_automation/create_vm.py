import subprocess

# Faire les conversions de Mo en Go
# utiliser unattered pour les options de la VM
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

# Fonction pour configurer le réseau de la machine virtuelle
def set_vm_network(vm_name, network_type, interface = ""):

    try:

        match network_type:
            case "1":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "nat"])
            case "2":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "bridged", "--bridgeadapter1", interface])
            case "3":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "hostonly"])
            case "4":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "intnet"])
            case "5":
                subprocess.run(["VBoxManage", "modifyvm", vm_name, "--nic1", "natnetwork"])

    except Exception as e:
        print("An error occurred:", str(e))

# Fonction pour configurer la machine virtuelle selon les paramètres définis par l'utilisateur
def set_vm_config(vm_name, path_to_iso, nb_cpu, memory_mb, disk_size_mb):

    try:

        # Création de la machine virtuelle
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--register"])

        # Configuration de la mémoire vive, du nombre de processeurs et de la taille du disque dur
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--memory", memory_mb, "--cpus", nb_cpu])
        subprocess.run(["VBoxManage", "createhd", "--filename", "{vm_name}/{vm_name}.vdi", "--size", str(disk_size_mb)])

        # Création du disque dur virtuel
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--bootable", "on"])
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", "{vm_name}/{vm_name}.vdi"])  

        # Attachement de l'ISO pour l'installation du système d'exploitation
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"])
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", path_to_iso])

    except Exception as e:
        print("An error occurred:", str(e))


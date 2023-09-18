import subprocess

# iso path: 
# C:\Users\Guillaume\Downloads\ubuntu-22.04.3-desktop-amd64.iso
# C:\Users\Guillaume\Downloads\ubuntu-22.04.3-live-server-amd64.iso

# Fonction pour configurer la machine virtuelle selon les paramètres définis par l'utilisateur
def set_vm_config(vm_name, path_to_iso, nb_cpu, memory_mb, disk_size_gb, username, login, password, vm_directory):

    try:

        # Détecter le type de système d'exploitation
        result = subprocess.run(["VBoxManage", "unattended", "detect", "--iso", path_to_iso, "--machine-readable"], stdout=subprocess.PIPE, text=True)

        # Récupère le OS type dans : ['OSTypeId="Ubuntu_64"', 'OSVersion="22.04.3 LTS \\"Jammy Jellyfish\\""', 'OSFlavor="Ubuntu "', 'OSLanguages="en-US"', 'OSHints=""', 'IsInstallSupported="on"', '']
        detected_os = result.stdout.splitlines()[0].split('"')[1]

        print(f"OS détecté : {detected_os}")

        # Création de la machine virtuelle
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name,"--ostype", detected_os, "--register"])

        # Convertir les GO reçus en MO
        disk_size_mb = int(disk_size_gb) * 1024

        # Configuration de la mémoire vive, du nombre de processeurs et de la taille du disque dur
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--memory", memory_mb, "--cpus", nb_cpu])
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--vram", "128"])
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--graphicscontroller", "vmsvga"])
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--ioapic", "on"])
        subprocess.run(["VBoxManage", "createhd", "--filename", (vm_directory + f"\\{vm_name}\\{vm_name}.vdi"), "--size", str(disk_size_mb)])

        # Création du disque dur virtuel
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--bootable", "on"])
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", (vm_directory + f"\\{vm_name}\\{vm_name}.vdi")])  

        # Attachement de l'ISO pour l'installation du système d'exploitation
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"])
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", path_to_iso])

        # Fonctionne pour l'installation de l'OS Ubuntu Desktop en mode "unattended"
        subprocess.run(["VboxManage", "unattended", "install", vm_name, "--iso", path_to_iso, "--locale", "fr_FR", "--country", "FR", "--hostname", (vm_name + ".infra"), "--time-zone", "UTC", "--user", login, "--password", password, "--full-user-name", username, "--install-additions", "--script-template", "preseed.cfg"])

        #--post-install-command", "apt-get update && apt-get install openssh-server"])
                        
    except Exception as e:
        print("Une erreur est survenue lors de la configuration de la VM :", str(e))
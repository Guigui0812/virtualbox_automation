import tkinter
from tkinter import filedialog

def open_file_explorer():
    iso_path = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("ISO files", "*.iso*"), ("all files", "*.*")))

def main_gui():

    window = tkinter.Tk()
    window.title("Virtual Machine Manager")
    window.resizable(True, True)
    window.geometry("500x500")

    # Titre de la fenêtre
    title_label = tkinter.Label(window, text="Virtual Machine Manager", font=("Arial", 20))
    title_label.pack()
    
    # Menu pour configurer le nom de la machine virtuelle
    name_label = tkinter.Label(window, text="VM Name:")
    name_label.pack()
    name_entry = tkinter.Entry(window)
    name_entry.pack()

    # Menu pour configurer la mémoire vive de la machine virtuelle
    memory_label = tkinter.Label(window, text="Memory (MB):")
    memory_label.pack()
    memory_entry = tkinter.Entry(window)
    memory_entry.pack()

    # Menu pour configurer le nombre de processeurs de la machine virtuelle
    cpu_label = tkinter.Label(window, text="CPU:")
    cpu_label.pack()
    cpu_entry = tkinter.Entry(window)
    cpu_entry.pack()

    # Menu pour configurer la taille du disque dur de la machine virtuelle
    disk_label = tkinter.Label(window, text="Disk (MB):")
    disk_label.pack()
    disk_entry = tkinter.Entry(window)
    disk_entry.pack()

    # Menu pour configurer le chemin vers le fichier ISO
    button_explore = tkinter.Button(window,text = "Browse Files",command = open_file_explorer)
    button_explore.pack()

    window.mainloop()
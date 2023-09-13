from vbox_cmd import main_menu

if __name__ == "__main__":

    print("#############################################")
    print("##                                         ##")
    print("##  Bienvenue dans le configurateur de VM  ##")
    print("##                                         ##")
    print("#############################################")
    print("Sélectionnez une version:")
    print("1 - CLI")
    print("2 - GUI")

    version = input("Votre choix: ")

    while version not in ["1", "2"]:
        print("Ceci n'est pas une option.")
        version = input("Votre choix: ")

    if version == "1":
        main_menu()

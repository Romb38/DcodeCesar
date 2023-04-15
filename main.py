import cesar as c
import os
import shutil

def infos(chx):
    if chx == 1:
        message = input("Message à encoder : ")
    else :
        message = input("Message à décoder : ")
    decal = int(input("Décalage : "))

    return message,decal

def infos_brute():
    message = input("Message à décoder : ")
    print("Langues disponible : " + str(c.output_langues()))
    print("(Ne mettez rien si vous voulez tester toutes les langues)")
    langue = input("Langue testée : ")
    return message,langue

def ajouter_langue():
    my_path = input("PATH : ")
    filename = input("Nom du fichier : ")
    my_path += "\\"
    my_path += filename
    if my_path[-4:] != ".txt":
        print("Mauvaise extension de fichier !")
        return
    elif not(os.path.exists(my_path)):
        print("Le chemin spécifié n'existe pas !")
        return
    else:
        cdpath = os.getcwd()
        langue = input("Acronyme de la langue : ")
        verif = input("Etes vous sur ? [O/n]")
        if verif.lower() == "o":
            shutil.copy2(my_path, cdpath+"\langues\\"+filename)
            new_filename = "mots_" + langue + ".txt"
            os.rename("./langues/"+filename, "./langues/"+new_filename)
        return



def main():
    titre = "Code Cesar (par Romb38)"
    string = "1 - Coder un message\n"
    string += "2 - Décoder un message\n"
    string += "3 - Bruteforce le décodage\n"
    string += "4 - Ajouter une langue\n"
    string += "0 - Quitter\n"
    string += "Choix (1/2/3/4/0) : "
    print(titre)
    choix = int(input(string))
    while choix != 0:
        if choix == 1:
            message,decal = infos(choix)
            message_encode = c.encrypt_cesar(message,decal)
            print("==============")
            print(message_encode)
        elif choix == 2:
            message,decal = infos(choix)
            message_decode = c.decrypt_cesar(message,decal)
            print("==============")
            print(message_decode)
        elif choix == 3:
            message,langue = infos_brute()
            message_decode = c.brutforce_decrypt_caesar(message,langue)
            print("message decodé, decalage, pourcentage de vérité")
            print("==============")
            print(message_decode)
        elif choix == 4:
            ajouter_langue()
        print("==============")
        choix = int(input(string))
    return 0

if __name__ == "__main__":
    main()
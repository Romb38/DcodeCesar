import cesar as c
import os
import shutil

def infos(chx):
    """
    Récupère les information du message et du nombre de décalage a effectuer
    """
    if chx == 1:
        message = input("Message à encoder : ")
    else :
        message = input("Message à décoder : ")
    decal = int(input("Décalage : "))

    return message,decal

def infos_brute():
    """
    Récupère le message a décoder ainsi que la potentielle langue a tester
    """
    message = input("Message à décoder : ")

    print("Langues disponible : " + str(c.output_langues()))

    print("(Ne mettez rien si vous voulez tester toutes les langues)")
    langue = input("Langue testée : ")

    return message,langue

def ajouter_langue():
    """
    Ajoute une langue aux répertoire
    """

    #Création du path complet
    my_path = input("PATH : ")
    filename = input("Nom du fichier : ")
    my_path += "\\"
    my_path += filename

    if my_path[-4:] != ".txt": #Si le fichier est bien un .txt
        #ERREUR - MAUVAISE EXTENSION DE FICHIER
        print("==============")
        print("ERREUR - ajouter_langue - Mauvaise extension de fichier !")
        return
    elif not(os.path.exists(my_path)): #Et qu'il existe réellement
        #ERREUR - CHEMIN INCORRECT
        print("==============")
        print("ERREUR - ajouter_langue - Le chemin spécifié n'existe pas !")
        return
    else: #Alors

        langue = input("Acronyme de la langue : ")
        #Vérification
        verif = input("Etes vous sur ? [O/n]")
        if verif.lower() == "o":
            cdpath = os.getcwd() #On récupère le path depuis la racine
            shutil.copy2(my_path, cdpath+"\langues\\"+filename) #On copie le fichier spécifié au bon endroit
            new_filename = "mots_" + langue + ".txt"
            os.rename("./langues/"+filename, "./langues/"+new_filename) #Eton le renomme correctement en "mots_<>.txt"
        return

def del_langue():
    """
    Supprime une langue du répertoire (IRREVERSIBLE)
    """

    langue = input("Acronyme de la langue : ")
    path = "./langues/mots_" + langue + ".txt" #On construit le path correctement
    if not(os.path.exists(path)): #Si la langue existe bien
        #ERREUR - ACRONYME INCORRECT
        print("==============")
        print("ERREUR - del_langue - Cette langue n'existe pas !")
    else :
        #Vérification
        verif = input("Cette action est irréversible, vouslez vous continuer ? [O/n]")
        if verif.lower() == "o":
            os.remove(path) #Suppression du fichier désigné
        return

def main():
    titre = "Code Cesar (par Romb38)"
    #Menu des choix
    string = "1 - Coder un message\n"
    string += "2 - Décoder un message\n"
    string += "3 - Bruteforce le décodage\n"
    string += "4 - Ajouter une langue\n"
    string += "5 - Supprimer une langue\n"
    string += "0 - Quitter\n"
    string += "Choix (1/2/3/4/5/0) : "

    print(titre)
    
    choix = int(input(string))
    while choix != 0:
        if choix == 1: #Encoder
            message,decal = infos(choix)
            message_encode = c.encrypt_cesar(message,decal)
            print("==============")
            print(message_encode)

        elif choix == 2: #Décoder
            message,decal = infos(choix)
            message_decode = c.decrypt_cesar(message,decal)
            print("==============")
            print(message_decode)

        elif choix == 3: #BruteForce
            message,langue = infos_brute()
            message_decode = c.brutforce_decrypt_caesar(message,langue)
            print("message decodé, decalage, pourcentage de vérité")
            print("==============")
            print(message_decode)

        elif choix == 4: #Ajouter une langue
            ajouter_langue()
        elif choix == 5: #Supprimer une langue
            del_langue()

        print("==============")

        choix = int(input(string))
    return 0

if __name__ == "__main__":
    main()
import os
NB_ALPHA = 26 #Nombre de lettre dans l'alphabet classique
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def output_langues():
    """
    Récupère les langues disponibles dans la base de donnée 
    """
    langues  = os.listdir("./langues/") #Donne la liste des fichier
    langue_dispo = []
    for i in langues: #Pour chaque langue on ne récupère que l'acronyme

        if i[-4:] == ".txt": #On vérifie l'extension du fichier
            #Le nom de fichier est au format mots_<acronyme>.txt
            j = 0
            while i[j] != "_":
                j += 1
            langue_dispo.append(i[j+1:-4]) #Et on l'ajoute aux langues disponibles
        else:
            #ERREUR - EXTENSION DE FICHIER INCORRECT
            print("ERREUR - output_langue - Le fichier " + i + " n'est pas au bon format !")
        
    return langue_dispo
    


def encrypt_cesar(message,shift):
    """
    Chiffre un message avec le code cesar et un décalage donné
    """

    #Les commentaires sont les mêmes que pour decrypt_cesar
    
    encrypted_message = ""
    for letter in message:
        if letter.isalpha():
            if letter.lower() == letter:
                decal = 97
            else:
                decal = 65
            #Ici on ajoute le décalage au lieu de l'enlever (diff coder/décoder)
            encrypted_letter = chr((ord(letter) + shift - decal) % 26 + decal)
            encrypted_message += encrypted_letter
        else:
            encrypted_message += letter
    return encrypted_message


def decrypt_cesar(message, shift):
    """
    Décrypte un message avec un décalage (shift) donné en paramètre
    """
    encrypted_message = "" #Message chiffrer (vide au début)
    for letter in message: #Pour chaque charactère du message
        if letter.isalpha(): #Si c'est une lettre de l'alphabet

            #Pour ramener la lettre entre 0 et 26
            #C'est différent si la lettre est en MAJ ou en min
            if letter.lower() == letter: #Si la lettre est en min
                decal = 97 #égal a ord("a")
            else: #Sinon elle est en maj
                decal = 65 #égal a ord("A")

            #On récupère "l'ordre" de la lettre, on lui enleve le décalage
            #Et on ramène ce nombre entre 0 et 26 avant de récupérer la lettre associée
            encrypted_letter = chr((ord(letter) - shift - decal) % 26 + decal)

            #On ajoute la lettre encrypté au message chiffrer
            encrypted_message += encrypted_letter
        else:
            #Si ce n'est pas une lettre alphabetique, on l'ajoute simplement au message
            encrypted_message += letter
            
    #On renvoie le message chiffré
    return encrypted_message

def string_to_array(message):
    """
    Transforme un message en un tableau de mots
    """
    
    tab_mot = [] #Tableau de tous les mots du message
    mot_actu = "" #mot du message que l'on est en train de regarder
    for lettre in message:
        if lettre.isalpha(): #Si c'est une lettre alphabetique (MAJ/min)
            mot_actu += lettre #On l'ajoute au mot actuel
        elif mot_actu != "": #Sinon (et si le mot actuel n'est pas vide)
            tab_mot.append(mot_actu) #On ajoute le mot a tab_mot
            mot_actu = "" #Et on remet le mot actuel a vide

    if mot_actu != "":#Si le message se finit par une lettre alors
        tab_mot.append(mot_actu) #Il faut ajouter le dernier mot au tableau
        
    return tab_mot


def compar_mot(mot1,mot2):
    """
    Compare 2 mots et renvoie 
        - -1 si mot1 < mot2
        - 0 si mot1 = mot2
        - 1 si mot1 > mot2
    """
    l1 = len(mot1)
    l2 = len(mot2)
    lg = min([l1,l2]) #On récupère le nombre de lettre du mot le plus court

    for i in range(0,lg):
        #On récupère l'ordre des deux lettres courantes
        i1 = ALPHABET.find(mot1[i])
        i2 = ALPHABET.find(mot2[i])

        if i1<i2: #On les compares
            return -1
        if i1>i2:
            return 1
    # ici, les lg 1ers car. sont identiques: le mot le plus court est avant
    if l1==l2:
        return 0
    else:
        return int(abs(l1-l2)/(l1-l2)) #On normalise le résultat (-1/1)

def dicho(mot,L):
    """
    Fait une recherche dichotomique dans une liste de mots triée
    """
    i,j = 0,len(L)-1
    while i != j:
        k = (j+i)//2 #On regarde le mots du millieu
        if compar_mot(mot,L[k]) == 0: #Si il est égal on dit qu'il existe
            return True
        elif compar_mot(mot,L[k]) == -1: #Si il est plus petit on regarde dans la première moitiée du dictionnaire
            j = k
        elif compar_mot(mot,L[k]) == 1: #Sinon dans la deuxième moitiée
            i = k+1
    return L[i] == mot #Si enfin la recheche s'arrête sur 1 seul mot, on le compare au mot demandé


def open_file(langue):
    file = open("langues/mots_"+langue+".txt", encoding="utf-8")
    words = list(line.strip().lower() for line in file) #On sort une liste de tous les mots
    return words

def exists_mot(mot,liste_mots):
    """
    Renvoie True si le mot existe dans la langue
    """
    return dicho(mot.strip().lower(),liste_mots) #Et on renvoie l'appartenance a cette liste

def liste_appartenance(tab_mot,langue_donne,langues_dispo):
    """
    Renvoie une liste du nombre de mot appartenant a chaque langue
    """
    appartenance = []
    pc = 0
    if langue_donne in langues_dispo: #Si une langue est imposée et qu'elle est dans les langues données
        langues = [langue_donne,"NP"] #(On rajoute les noms propres communs a toutes les langues)
        for langue in langues: #On comptes les mots qui appartiennent a cette langues
            compt = 0
            liste_mot = open_file(langue)
            for mot in tab_mot:
                if exists_mot(mot,liste_mot): #Et on ne parcours que celle la
                    compt += 1
            appartenance.append(compt)

            pc += 100/len(langues)
            print(langue + " - Validée - " + str(round(pc)) + "%")

    else : #Sinon on les fais toutes
        for langue in langues_dispo:
            compt = 0
            liste_mot = open_file(langue)
            tab_mot_copy = []
            for mot in tab_mot: #Et on compte le nombre de mots qui existe pour chaque langue
                if exists_mot(mot,liste_mot):
                    compt += 1
                else:
                    tab_mot_copy.append(mot)
            
            tab_mot = tab_mot_copy
            
            pc += 100/len(langues_dispo) #Pourcentage d'avancée dans le calcul
            print(langue + " - Validée - " + str(round(pc)) + "%")

            appartenance.append(compt)

    return appartenance

def potentialite(appartenance,tab_mot):
    """
    Donne le pourcentage de chance que la phrase donnée en entrée soit le message décodé

    Pour cela compte le nombre de mot existant dans 1 ou plusieurs langues et renvoie le décodage comptabilisant
    le plus de mots existants dans les langues disponible/imposée
    """
    
    som = 0 #On fait la somme du nombre de mots appartenant a chaque langues
    for i in appartenance:
        som += i

    som = (som * 100)/len(tab_mot) #Passage en %
    return som


def brutforce_decrypt_caesar(message,langue = ""):
    """
    in : 
    message : str - Message que l'on veut décoder
    (OPT) langue : str - Langue dans laquelle on veut décoder, si aaucune n'est donnée, on testera toutes les langues disponibles
    (OPT) precision : int - Pourcentage de chance minimal pour que le message soit considéré comme bon
    
    out :
    message_dcode : str - Message le plus probable dédcodé
    decal : int - Nombre de lettre de décalage
    maxi : int - Pourcentage de chance que ca soit le bon message

    Trouve le mot codé par le code caesar (sans connaitre le décalage)
    """

    langues_dispo = output_langues()
    potentiel = [] #Contient le pourcentage de chance que ce decalage soit le bon
    for decal in range(0,NB_ALPHA):
        print("Décalage n°" + str(decal+1) +"/"+str(NB_ALPHA))
        potentiel_decrypt = decrypt_cesar(message,decal)#On essaie avec un décalage
        tab_mot = string_to_array(potentiel_decrypt)#On sépare chaque mots
        appartenance = liste_appartenance(tab_mot,langue,langues_dispo) #Liste des mots appartenant a chaque langue
        potentiel.append(potentialite(appartenance,tab_mot)) 
    

    #Fonction de recherche d'indice maximum
    decal = 0
    maxi = potentiel[decal]
    for i in range(len(potentiel)):
        if potentiel[i] > maxi:
            maxi = potentiel[i]
            decal = i
        
    message_dcode = decrypt_cesar(message,decal) #On décode le message
    
    return message_dcode,decal,maxi #On renvoie le message décodé et le décalage nécessaire

from random import randint

def ChoisirMot(path, length):
    """Pioche un mot dans le fichier spécifié. Le fichier doit contenir un mot par ligne, et être de longueur connue."""
    
    # l'index du mot à choisir, tiré au sort aléatoirement
    index = randint(0, length)

    # ouvre le fichier, par défaut en lecture seule.
    file = open(path)

    # on parcourt les lignes du fichier, une par une.
    for i, word in enumerate(file):
        # si on est sur la bonne ligne, on retourne le mot
        if i == index:

            # on ferme le fichier, même si le laisser ouvert n'aurait sans doute
            # pas causé de problème étant donné qu'il est en lecture seule
            file.close()        
            
            # on utilise .strip() pour retirer l'éventuel '\n' à la fin
            return word.strip()
    
    # note : utiliser file.readlines aurait sans doute été plus simple, mais probablement
    #        moins performant avec un fichier contenant BEAUCOUP de mots.

# Remplacer * par une lettre 
def RemplaceLettre (mot_secret, lettre, etoiles):
    letoiles=list(etoiles)
    for i in range(0 ,len(mot_secret)):
        if lettre == mot_secret [i] :
            letoiles[i] = lettre
    etoiles="".join(letoiles)
    return etoiles

etapes_pendu = [
    "          \n          \n          \n          \n          \n          \n        ",
    "          \n          \n          \n          \n          \n          \n _______",
    "          \n| /       \n|/        \n|         \n|         \n|         \n|_______",
    "|______   \n| /    |  \n|/        \n|         \n|         \n|         \n|_______",
    "|______   \n| /    |  \n|/      0 \n|         \n|         \n|         \n|_______",
    "|______   \n| /    |  \n|/      0 \n|     /|\ \n|     / \ \n|         \n|_______"
]

print('Bienvenue dans le pendu !')
print('Vous devez deviner le mot en faisant moins de 5 erreurs.')
print('Bonne chance !')

while True:
    compteur_pendu = 0

    # on pioche un mot secret
    mot_secret=ChoisirMot('mots.txt', 50)

    # Afficher la longueur du mot en etoiles
    etoiles= len(mot_secret)*'*'
    while compteur_pendu!=5:
        print(etoiles)

        # Demande une lettre au joueur
        demandelettre= input("Veuillez donner une lettre (minuscule, entre A et Z) : ")
        if demandelettre in mot_secret:
            etoiles=RemplaceLettre(mot_secret,demandelettre,etoiles)
            
            if etoiles==mot_secret:
                print ("FELICITATION VOUS AVEZ GAGNE !")
                break
            else:
                print('Bravo, cette lettre fait partie du mot secret !')
        else:
            compteur_pendu += 1
            print ("Cette lettre ne fait pas partie du mot secret, vous avez fait", compteur_pendu ,"erreur(s).")
            if compteur_pendu == 4:
                print ("Ceci est votre dernière chance, donc réfléchissez bien...")
            if compteur_pendu == 5:
                print ("VOUS AVEZ PERDU !!!")

        print(etapes_pendu[compteur_pendu])

    print('Le mot était', mot_secret)
    
    reponse_rejouer = input('Voulez-vous rejouer ? ("oui" pour rejouer) : ')
    
    if reponse_rejouer.lower() == 'oui' :
        continue # on pourrait s'en passer mais c'est plus explicite
    else:
        break # on arrête le jeu
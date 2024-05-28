def NewBoard(n):
    tableau = []
    for i in range(n):
        tableau.append([]) # ajoute une nouvelle colone
        for j in range(n):
            tableau[i].append(0) # ajoute le nombre de 0 nécessaire
    return tableau

def DisplayBoard(tableau,n):
    tableau_string = "\n" # nouvelle ligne entre chaque affichage
    for i in range(n):
        tableau_string = tableau_string + str(i+1)+" | " # affiche les numéros de colonnes
        # remplace les nombres par les pions correspondants
        for j in range(n):
            if tableau[i][j] == 0:
                tableau_string = tableau_string + "." + "  "
            elif tableau[i][j] == 1:
                tableau_string = tableau_string + "X" + "  "
            elif tableau[i][j] == 2:
                tableau_string = tableau_string + "O" + "  "
        
        tableau_string += "\n"
    tableau_string = tableau_string + "  " + "-"*(n*3) + "\n" # affiche la ligne du bas
    tableau_string = tableau_string + "    " # espace pour alligner les numéros de colonnes

    for i in range(n): # affiche les numéros de lignes
        tableau_string = tableau_string + str(i+1) + "  "
    print(tableau_string)

def DisplayScore(score):
    print("score du joueur 1: " + str(score[0]))
    print("score du joueur 2: " + str(score[1]))

def PossibleSquare(tableau,n,i,j):
    if i < 0 or i >= n or j < 0 or j >= n: # vérifie que les coordonées soient dans le tableau
        return False
    elif tableau[i][j] != 0: # vériifie que la case soit vide
        return False
    else: # si tout est bon on renvoie True
        return True
    
def SelectSquare(tableau,n):
    coord = input("Entrez les coordonnées de la case séparés d'une virgule: ")
    j = int(coord.split(",")[0]) - 1 # -1 pour correspondre à l'index
    i = int(coord.split(",")[1]) - 1 # -1 pour correspondre à l'index
    return i,j

def UpdateBoard(tableau,player,i,j):
    tableau[i][j] = player # on ajoute le numéro du joueur à la case

def UpdateScore(tableau,n,player,score,i,j):
    # j = x ; i = y
    score_update = [0,0]  # scores temporaires pour les diagonales
    score_update2 = [0,0] # scores temporaires pour les diagonales
    corner = False
    # vérifie si la case est un coin
    if (j == 0 and i == 0) or (j == n-1 and i == n-1) or (j == n-1 and i == 0) or (j == 0 and i == n-1):
        corner = True
    i2 = i # i2 et j2 vont servir pour détecter une autre diagonale
    j2 = j
    for a in range(n): # on récupère les coordonées du point opposé numéro 1
        if i > 0 and j > 0:
            i = i - 1
            j = j - 1
    for a in range(n): # on récupère les coordonées du point opposé numéro 2
        if i2 > 0 and j2 < n-1:
            i2 = i2 - 1
            j2 = j2 + 1
    
    # comptage des pions sur la diagonale 1
    for a in range(n):
        if i + a < n and j + a < n: # vérification pour éviter l'erreur de dépassement de tableau
            if tableau[i+a][j+a] == player: # vérifie si le pion est du joueur
                score_update[player-1] = score_update[player-1] + 1 # ajoute 1 au score du joueur
            if tableau[i+a][j+a] == 0: # sinon si la case est vide on arrête le comptage
                score_update[player-1] = 0 # et on remet le score à 0
                break

    # comptage des pions sur la diagonale 2
    for a in range(n):
        if j2 - a >= 0 and i2 + a < n: # vérification pour éviter l'erreur de dépassement de tableau
            if tableau[i2+a][j2-a] == player: # vérifie si le pion est du joueur
                score_update2[player-1] = score_update2[player-1] + 1 # ajoute 1 au score du joueur
            if tableau[i2+a][j2-a] == 0: # sinon si la case est vide on arrête le comptage
                score_update2[player-1] = 0 # et on remet le score à 0
                break
    
    score[0] = score[0] + score_update[0] + score_update2[0] # on ajoute les scores temporaires au score final pour le joueur 1
    score[1] = score[1] + score_update[1] + score_update2[1] # on ajoute les scores temporaires au score final pour le joueur 2
    if corner == True: # si le pion est un coin on enlève 1 au score
        score[player - 1] = score[player - 1] - 1

def again(board,n):
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0: # on vérifie si il y a encore des cases vides dans le tableau
                return True
    return False

def win(score):
    if score[0] > score[1]: # si le score du joueur 1 est plus grand que celui du joueur 2
        print("Le joueur 1 a gagné avec un score de " + str(score[0]) + " contre " + str(score[1]))
    elif score[0] < score[1]: # si le score du joueur 2 est plus grand que celui du joueur 1
        print("Le joueur 2 a gagné avec un score de " + str(score[1]) + " contre " + str(score[0]))
    else: # si les deux scores sont égaux
        print("Egalité avec un score de " + str(score[0]))

def diagonals():
    '''
    lance le jeu des diagonales
    '''
    n = int(input("Entrez la taille du tableau: "))
    tableau = NewBoard(n)
    score = [0,0]
    player = 1
    while again(tableau,n): # tant qu'il reste des cases vides
        DisplayBoard(tableau,n)
        DisplayScore(score)
        i,j = SelectSquare(tableau,n) # on demande les coordonées de la case
        while not PossibleSquare(tableau,n,i,j): # tant que la case n'est pas valide
            print("Case non valide")
            i,j = SelectSquare(tableau,n) # on redemande les coordonées de la case
        UpdateBoard(tableau,player,i,j) # on ajoute le numéro du joueur à la case
        UpdateScore(tableau,n,player,score,i,j) # on met à jour le score
        # on change de joueur
        if player == 1:
            player = 2
        else:
            player = 1
    win(score) # on affiche le gagnant

diagonals() # on lance le jeu

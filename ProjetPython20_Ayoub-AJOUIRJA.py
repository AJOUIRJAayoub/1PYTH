import tkinter as tk #importation de tkinter
import os #importation de os et de sys pour pouvoir relancer le programme
import sys



class jeu:
    def __init__(self):
        self.DemandeNombreColonne() # demande à l'utilisateur le nombre de colonnes
        self.DemandeNombreLigne() #demande à l'utilisateur le nombre de lignes
        self.DemandeNombrejoueurs() #demande à l'utilisateur le nombre de joueurs
        self.couleurs = ['red','lime','royal blue','orange','purple','pink','cyan','magenta']  # liste des couleurs des joueurs
        self.joueurs = self.couleurs[:self.joueurs] #liste des <self.joueurs> premières de self.couleurs
        self.joueur_actif_num = 0 #numéro du joueur actif
        self.joueur_actif = self.joueurs[self.joueur_actif_num] #le joueur actuel est le premier joueur de la liste
        self.elimines = [] #liste des joueurs éliminés
        self.root = tk.Tk() #la fenêtre
        self.root.title("pions divergeants") #titre de la fenêtre
        self.root.geometry(str(self.colonnes * 75) + "x" + str(self.lignes * 75)) #taille de la fenêtre
        self.canvas = tk.Canvas(self.root, width=self.colonnes * 75, height=self.lignes * 75, bg="black")
        self.pions = self.init_case() #initialisation des cases
        self.root.resizable(False, False) #pour ne pas pouvoir redimensionner la fenêtre
        self.ecran_de_fin = False #booléen pour savoir si l'écran de fin est affiché
        self.canvas.pack(side="top", fill="both", expand=True) #ajout du canvas à la fenêtre
    



    #retourne le nombre de colonne que souhaite l'utilisateur
    def DemandeNombreColonne(self):
        self.colonnes = int(input("Nombre de colonnes : "))
        if self.colonnes <= 2 or self.colonnes > 12:
            print("nombre de colonnes invalide")
            self.DemandeNombreColonne()
    
    #retourne le nombre de lignes que souhaite l'utilisateur
    def DemandeNombreLigne(self):
        self.lignes = int(input("Nombre de lignes : "))
        if self.lignes <= 2 or self.lignes > 10:
            print("nombre de lignes invalide")
            self.DemandeNombreLigne()
    #retourne le nombre de joueurs que souhaite l'utilisateur
    def DemandeNombrejoueurs(self):
        self.joueurs = int(input("Nombre de joueurs : "))
        if self.joueurs <= 1 or self.joueurs > 8:
            print("nombre de joueurs invalide")
            self.DemandeNombrejoueurs()





    class case:
        def __init__(self, x, y,canvas ,capacite,cliquer):
            self.x = x
            self.y = y
            self.canvas = canvas
            self.capacite = capacite #nombre maximum de pions que peut contenir la case
            self.couleur = None #couleur des pions de la case
            self.nombre = 0
            self.clique = cliquer
            self.creer() #création de la case sur le canvas à son initialisation

        def supprimer_pions(self):
            self.canvas.delete("pion_" + str(self.x) + "_" + str(self.y)) #recupère les élements du canvas ayant le tag "pion_x_y" et les supprime
            self.nombre = 0 #remet le nombre de pions à 0
            self.couleur = None #et la couleur à None

        def definir_nombre_pions(self, nombre , couleur):
            self.supprimer_pions()
            #coordonées de la case
            x1 = self.x * 75
            y1 = self.y * 75
            x2 = self.x * 75 + 75
            y2 = self.y * 75 + 75
            self.nombre = nombre #assimilation du nombre de pions à la variable nombre
            self.couleur = couleur #assimilation de la couleur des pions à la variable couleur
            if nombre == 1:
                self.canvas.create_oval(x1 + 30, y1 + 30, x2 - 30, y2 - 30, fill=couleur, tags=("pion", "pion_" + str(self.x) + "_" + str(self.y))) #case du milieu
            elif nombre == 2:
                self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 50, y2 - 50, fill=couleur,  tags=("pion", "pion_" + str(self.x) + "_" + str(self.y))) #cases du coin haut gauche
                self.canvas.create_oval(x1 + 50, y1 + 50, x2 - 10, y2 - 10, fill=couleur,  tags=("pion", "pion_" + str(self.x) + "_" + str(self.y))) #cases du coin bas droit
            elif nombre == 3:
                self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 50, y2 - 50, fill=couleur, tags=("pion", "pion_" + str(self.x) + "_" + str(self.y))) #cases du coin haut gauche
                self.canvas.create_oval(x1 + 30, y1 + 30, x2 - 30, y2 - 30, fill=couleur, tags=("pion", "pion_" + str(self.x) + "_" + str(self.y))) #case du milieu
                self.canvas.create_oval(x1 + 50, y1 + 50, x2 - 10, y2 - 10, fill=couleur, tags=("pion", "pion_" + str(self.x) + "_" + str(self.y))) #cases du coin bas droit
        
        def ajouter_un_pion(self, couleur):
            if self.nombre == self.capacite: #si la capacité est atteinte
                self.supprimer_pions()
                return False #on retourne false
            
            #on defini le nombre de pions pour en avoir +1
            if self.nombre == 0:
                self.definir_nombre_pions(1, couleur)
            elif self.nombre == 1:
                self.definir_nombre_pions(2, couleur)
            elif self.nombre == 2:
                self.definir_nombre_pions(3, couleur)
            elif self.nombre == 3:
                self.definir_nombre_pions(0, couleur)

        def creer(self):
            #coordonnées de la case
            x1 = self.x * 75
            y1 = self.y * 75
            x2 = self.x * 75 + 75
            y2 = self.y * 75 + 75

            self.rectangle = self.canvas.create_rectangle(x1,y1,x2,y2, fill="black", outline="red" ,tags=("case", "case_" + str(self.x) + "_" + str(self.y))) #création de la case avec le tag case_x_y
            self.canvas.tag_bind(self.rectangle, "<Button-1>", lambda event : self.clique(self.x,self.y)) #assignation du clic gauche sur une des case à la fonction clic
        
        def definir_couleur(self, couleur):
            self.canvas.itemconfig("case_" + str(self.x) + "_" + str(self.y), outline=couleur) # changement de la couleur de la bordure 

     




    def capacite(self,x,y):
        #calcul de la capacite maximale de pions que peux contenir la case
        return 1 if (x in [0, self.colonnes-1] and y in [0, self.lignes-1]) else 2 if (x in [0, self.colonnes-1] or y in [0, self.lignes-1]) else 3

    
    def init_case(self):
        self.liste_case = [] #liste 2d des cases crées
        for y in range(self.lignes):
            self.liste_case.append([])
            for x in range(self.colonnes):
                case = self.case(x,y,self.canvas, self.capacite(x,y),self.cliquer)
                self.liste_case[y].append(case) #ajout de la case crée á la liste

    #methode du clic de la case
    def cliquer(self,x,y):
        case = self.liste_case[y][x] #case cliquée
        if case.couleur == None or case.couleur == self.joueur_actif: #si la case n'est pas détenu par un joueur ou par le joueur actuel
            case.couleur = self.joueur_actif #on donne la case au joueur actuel
            if case.ajouter_un_pion(self.joueur_actif) == False: #si la case est pleine
                self.propagation(x,y) #on propage les pions
            self.elimination_victoire() #on vérifie si des pions sont éliminés ou si il y a victoire
            self.tour_suivant() #on passe le tour au joueur suivant

    #propagations des pions aux cases alentours
    def propagation(self, x, y):
        #toutes les cases autour de la case à propager (incluant les None)
        cases_autour_none = [self.liste_case[y][x-1] if x > 0 else None, self.liste_case[y][x+1] if x < self.colonnes-1 else None, self.liste_case[y-1][x] if y > 0 else None, self.liste_case[y+1][x] if y < self.lignes-1 else None]
        cases_autour = [v for v in cases_autour_none if v is not None] #on enlève les None
        for i in cases_autour:
            i.couleur = self.joueur_actif #on donne la couleur du joueur actif à la case qui est envahi
            if i.ajouter_un_pion(self.joueur_actif) == False: #on revérifie si la case est pleine
                self.propagation(i.x,i.y)
        self.elimination_victoire()

    def elimination_victoire(self):
        joueurs_tableau = [j.couleur for i in self.liste_case for j in i if j.couleur is not None] #recuperation de toutes lees couleurs de tous les pions dans le tableau
        nombre_total_pions = sum([j.nombre for i in self.liste_case for j in i if j.couleur is not None]) #compte de tous les pions dans le tableau
        if nombre_total_pions >= len(self.joueurs): #si tous les joueurs ont pû jouer
            for joueur in self.joueurs: 
                if joueur not in joueurs_tableau: #si le joueur n'es pas dans le tableau
                    if joueur not in self.elimines: #et qu'il n'est pas deja éliminé
                        self.elimines.append(joueur) #on l'ajoute aux éliminés
                        popup = tk.Toplevel() #on fait la popup

                        label = tk.Label(popup, text=f"Le joueur {joueur} a été éliminé.") #on ajoute le test 
                        label.pack()

                        button = tk.Button(popup, text="OK", command=popup.destroy) #on fait un bouton ok pour fermer
                        button.pack()

            if len(self.elimines) == len(self.joueurs) - 1: #si il y a tous les joueurs éliminés sauf 1
                    if self.ecran_de_fin == False: 
                        self.ecran_de_fin = True #on met la variable ecran_de_fin à true pour éviter d'en afficher plusieurs
                        popup = tk.Toplevel()

                        label = tk.Label(popup, text=f"victoire du joueur {self.joueur_actif}")
                        label.pack()

                        button = tk.Button(popup, text="Quitter", command=exit)
                        button.pack()

                        button2 = tk.Button(popup, text="Recommencer", command=self.relancer_partie)
                        button2.pack()
    
    def relancer_partie(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) #on relance le programme avec les mêmes arguments
            
    def tour_suivant(self):
        if self.joueur_actif_num == len(self.joueurs)-1: #pour éviter que le numero du joueur actif dépasse le nombre de joueur total
            self.joueur_actif_num = 0
        else:
            self.joueur_actif_num += 1
        self.joueur_actif = self.joueurs[self.joueur_actif_num] #nouveau joueur actif

        if self.joueur_actif in self.elimines: 
            self.tour_suivant() #si le joueur est éliminé on repasse un tour
        self.joueur_actif = self.joueurs[self.joueur_actif_num]
        self.changement_couleur() #on change les couleurs des cases pour la couleur du joueur actif
    
    def changement_couleur(self):
        for i in self.liste_case:
            for j in i:
                j.definir_couleur(self.joueur_actif) #on change la couleur pour tous les joueurs dans la liste
    



jeu = jeu()
jeu.root.mainloop()



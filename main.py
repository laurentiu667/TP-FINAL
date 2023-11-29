import tkinter as tk
import random
import helper as hp

class Joueur:
    def __init__(self, argent_initial):
        self.argent = argent_initial

class Creep:
    def __init__(self, parent, niveau_actuel, vitesse, valeur, couleur, taille, chemin):
        self.parent = parent
        self.mana = 25 * niveau_actuel
        self.vitesse = vitesse
        self.valeur = valeur
        self.couleur = couleur
        self.taille = taille
        self.chemin_courant = 0
        self.x = chemin[0][0]
        self.y = chemin[0][1]
        self.x_cible = chemin[0][2]
        self.y_cible = chemin[0][3]
        self.angle = hp.Helper.calcAngle(self.x, self.y, self.x_cible, self.y_cible)

    def deplacer(self):
        self.x, self.y = hp.Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        dist = hp.Helper.calcDistance(self.x, self.y, self.x_cible, self.y_cible)
        if dist <= self.vitesse:
            self.chemin_courant += 1
            if self.chemin_courant < len(self.parent.chemin):
                chemin = self.parent.chemin[self.chemin_courant]
                self.x = chemin[0][0]
                self.y = chemin[0][1]
                self.x_cible = chemin[0][2]
                self.y_cible = chemin[0][3]
                self.angle = hp.Helper.calcAngle(self.x, self.y, self.x_cible, self.y_cible)
            else:
               self.parent.supprimer_creep(self)

class Modele:
    def __init__(self):
        self.temps_avant_niveau = 100
        self.timer_id = None
        self.vies_chateau = 20
        self.joueur = Joueur(argent_initial=100)
        self.creeps = []
        self.creeps_en_jeu = []
        self.niveau_actuel = 0
        self.delai_depart = 0
        self.delai_depart_max = 25

        self.chemin = [
            [(200,    0,  200, 640), "white"],
            [(200,  640,  440, 640), "white"],
            [(440,  640,  440, 120), "white"],
            [(440,  120, 1100, 120), "white"],
            [(1100, 120, 1100, 400), "white"],
            [(1100, 400,  760, 400), "white"],
            [(760,  400,  760, 640), "white"],
            [(760,  640, 1100, 640), "white"]
        ]

        self.creer_niveau()

        self.chateau = [
            [(1100, 550, 1100, 670), "grey"],
            [(1100, 550, 1050, 550), "grey"],
            [(1150, 550, 1100, 550), "grey"]
        ]

    def supprimer_creep(self):
        self.vies_chateau -= 1
        self.creeps_en_jeu.remove(self)
        # add creep dans une liste de creep_mort[]
        # puis lorsque les creeps ont fini de bouger, enlever creep de la liste de creep en jeu

    def jouer_coup(self):
        for creep in self.creeps_en_jeu:
            creep.deplacer()
        if self.creeps:
            if self.delai_depart == 0:
                creep = self.creeps.pop()
                self.creeps_en_jeu.append(creep)
                self.delai_depart = self.delai_depart_max
            else:
                self.delai_depart -= 1

    def creer_niveau(self):
        for i in range(20):
            vitesse = 15
            valeur = 10
            couleur = "red"
            taille = int(random.randrange(80, 120) / 2)
            creep = Creep(self, self.niveau_actuel, vitesse, valeur, couleur, taille, self.chemin[0])
            self.creeps.append(creep)

class Vue:
    def __init__(self, parent, modele):
        self.parent = parent
        self.modele = modele

        self.root = tk.Tk()
        self.root.title("Tower Defense")
        self.container = tk.Frame(self.root)
        self.container.pack()

        self.container_palette_infos = tk.Frame(self.root)
        self.canvas = tk.Canvas(self.container, width=1200, height=960, bg="black")
        self.canvas.pack()

        self.dessiner_jeu()

        self.vies_label = tk.Label(self.container, text=f"Vies restantes : {self.modele.vies_chateau}",
                                   font=("Helvetica", 16),
                                   fg="white", bg="black")
        self.vies_label.pack(side=tk.RIGHT)

    def dessiner_jeu(self):
        for p in self.modele.chemin:
            coords, color = p
            x1, y1, x2, y2 = coords
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width="75", capstyle="round")

        for c in self.modele.chateau:
            coords, color = c
            x1, y1, x2, y2 = coords
            self.canvas.create_line(x1, y1, x2, y2, fill=color,width="50")

    def afficher_jeu(self):
        self.canvas.delete("dynamique")

        for creep in self.modele.creeps_en_jeu:
            largeur = 20
            hauteur = 20
            self.canvas.create_oval(creep.x - largeur, creep.y - hauteur, creep.x + largeur, creep.y + hauteur, fill="red", outline="white",
                                    tags=("dynamique", "creep"))

    def update_vies_label(self):
        self.vies_label.config(text=f"Vies restantes : {self.modele.vies_chateau}")

class Controleur:
    def __init__(self):
        self.no_iteration = 0
        self.modele = Modele()
        self.vue = Vue(self, self.modele)
        self.vue.root.after(100, self.boucler_jeu)
        self.vue.root.mainloop()

    def boucler_jeu(self):
        self.no_iteration += 1
        self.modele.jouer_coup()
        self.vue.afficher_jeu() # affiche uniquement les choses dynamique du jeu
        self.vue.root.after(50, self.boucler_jeu)

def main():
    Controleur()

if __name__ == "__main__":
    main()
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
        self.x = chemin[0][0] * self.parent.cell_size
        self.y = chemin[0][1] * self.parent.cell_size
        self.x_cible = (chemin[0][2] * self.parent.cell_size) - self.parent.cell_size / 2
        self.y_cible = (chemin[0][3] * self.parent.cell_size) - self.parent.cell_size / 2
        self.angle = hp.Helper.calcAngle(self.x,self.y,self.x_cible,self.y_cible)

    def deplacer(self):
        self.x, self.y = hp.Helper.getAngledPoint(self.angle,self.vitesse,self.x,self.y)
        dist = hp.Helper.calcDistance(self.x,self.y,self.x_cible,self.y_cible)
        if dist <= self.vitesse:
            self.chemin_courant += 1
            if self.chemin_courant < len(self.parent.chemin):
                chemin = self.parent.chemin(self.chemin_courant)
                self.x = chemin[0][0] * self.parent.cell_size
                self.y = chemin[0][1] * self.parent.cell_size
                self.x_cible = (chemin[0][2] * self.parent.cell_size) - self.parent.cell_size / 2
                self.y_cible = (chemin[0][3] * self.parent.cell_size) - self.parent.cell_size / 2
                self.angle = hp.Helper.calcAngle(self.x, self.y, self.x_cible, self.y_cible)
            else:
               pass
               # tuer creep + chatelin

class Modele:
    def __init__(self, root=None):
        self.cell_size = 40
        self.temps_avant_niveau = 100
        self.timer_id = None
        #self.root = root
        self.vies_chateau = 20
        self.joueur = Joueur(argent_initial=100)
        self.creeps = []
        self.creeps_en_jeu = []
        #self.positions_pixels = []
        self.niveau_actuel = 0
        self.delai_depart = 0
        self.delai_depart_max = 20

        self.chemin = [
            [(5, 0, 7, 16), "white"],
            [(7, 14, 11, 16), "white"],
            [(11, 3, 13, 16), "white"],
            [(13, 3, 30, 5), "white"],
            [(28, 5, 30, 10), "white"],
            [(19, 8, 28, 10), "white"],
            [(19, 10, 21, 16), "white"],
            [(21, 14, 29, 16), "white"]
        ]
        self.creer_niveau()
        #self.creer_creeps()

        self.chateau = [
            [(29, 13, 31, 16), "grey"],
            [(28, 12, 29, 13), "grey"],
            [(31, 12, 32, 13), "grey"]
        ]

    def jouer_coup(self):
        for i in self.creeps_en_jeu:
            i.deplacer()
        if self.creeps:
            if self.delai_depart == 0:
                creep = self.creeps.pop()
                self.creeps_en_jeu.append(creep)
                self.delai_depart = self.delai_depart_max
            else:
                self.delai_depart -= 1

    def creer_niveau(self):
        for i in range(20):
            vitesse = 1
            valeur = 10
            couleur = "red"
            taille = int(random.randrange(80, 120) / 2)
            creep = Creep(self, self.niveau_actuel, vitesse, valeur, couleur, taille, self.chemin[0])
            self.creeps.append(creep)

class Vue:
    def __init__(self, parent, modele):
        self.parent = parent
        self.modele = modele

        #self.root.geometry("1920x1080")
        self.root = tk.Tk()
        self.root.title("Tower Defense")
        self.container = tk.Frame(self.root)
        self.container.pack()

        self.container_palette_infos = tk.Frame(self.root)
        self.canvas = tk.Canvas(self.container, width=1320, height=960, bg="black")
        self.canvas.pack()

        self.dessiner_jeu()

        #self.timer_running = True
        #self.start_time = time.time()
        #self.update_timer()

        self.vies_label = tk.Label(self.container, text=f"Vies restantes : {self.modele.vies_chateau}",
                                   font=("Helvetica", 16),
                                   fg="white", bg="black")
        self.vies_label.pack(side=tk.RIGHT)

        self.root.bind("<space>", self.ignore_timer)

    def dessiner_jeu(self):
        for p in self.modele.chemin:
            coords, color = p
            x1, y1, x2, y2 = coords
            x1 *= self.modele.cell_size
            y1 *= self.modele.cell_size
            x2 *= self.modele.cell_size
            y2 *= self.modele.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        for c in self.modele.chateau:
            coords, color = c
            x1, y1, x2, y2 = coords
            x1 *= self.modele.cell_size
            y1 *= self.modele.cell_size
            x2 *= self.modele.cell_size
            y2 *= self.modele.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def afficher_jeu(self):
        self.canvas.delete("dynamique")
        #x_start = 5.5 * self.modele.cell_size
        #y = 2 * self.modele.cell_size

        for creep in self.modele.creeps_en_jeu:
            largeur = self.modele.cell_size / 2
            hauteur = self.modele.cell_size / 2
            #self.canvas.create_oval(x_start, y, x_start + width, y + height, fill="red", outline="white")
            self.canvas.create_oval(creep.x - largeur, creep.y - hauteur, creep.x + largeur, creep.y + hauteur, fill="red", outline="white",
                                    tags=("dynamique", "creep"))

    def ignore_timer(self, event):
        self.timer_running = False
        self.canvas.delete("timer")

    def update_vies_label(self):
        self.vies_label.config(text=f"Vies restantes : {self.modele.vies_chateau}")

class Controleur:
    def __init__(self):
        self.no_iteration = 0
        self.modele = Modele(self)
        self.vue = Vue(self, self.modele)
        self.vue.root.after(100, self.boucler_jeu)
        self.vue.root.mainloop()

    def boucler_jeu(self):
        self.no_iteration += 1
        self.modele.jouer_coup()
        self.vue.afficher_jeu() # affiche uniquement les choes dinq;iaue du jeu
        self.vue.root.after(50, self.boucler_jeu)

def main():
    c = Controleur()
    #c.demarrer()

if __name__ == "__main__":
    main()
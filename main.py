import tkinter as tk
import time
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
        self.x = chemin[0][0] * self.parent.cell_size
        self.y = chemin[0][1] * self.parent.cell_size
        self.x_cible = chemin[0][2] * self.parent.cell_size
        self.y_cible = chemin[0][3] * self.parent.cell_size
        self.angle = hp.Helper.calcAngle(self.x,self.y,self.x_cible,self.y_cible)
        self.chemin_courant = 0

    def deplacer(self):
        self.x, self.y = hp.Helper.getAngledPoint(self.angle,self.vitesse,self.x,self.y)
        dist = hp.Helper.calcDistance(self.x,self.y,self.x_cible,self.y_cible)
        if dist <= self.vitesse:
            self.chemin_courant += 1
            chemin = self.parent.chemin(self.chemin_courant)
            self.x = chemin[0][0] * self.parent.cell_size
            self.y = chemin[0][1] * self.parent.cell_size
            self.x_cible = chemin[0][2] * self.parent.cell_size
            self.y_cible = chemin[0][3] * self.parent.cell_size
            self.angle = hp.Helper.calcAngle(self.x, self.y, self.x_cible, self.y_cible)

class Modele:
    def __init__(self, root=None):
        self.cell_size = 40
        self.temps_avant_vague = 5000
        self.timer_id = None
        self.root = root
        self.vies_chateau = 20
        self.joueur = Joueur(argent_initial=100)
        self.creeps = []
        self.creeps_en_jeu = []
        self.positions_pixels = []
        self.niveau_actuel = 1
        self.delai_depart = 0
        self.delai_depart_max = 3

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

        self.creer_creeps()

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

    def creer_creeps(self):
        for i in range(20):
            vitesse = 1
            valeur = 10
            couleur = "red"
            taille = int(random.randrange(80, 120) / 2)
            creep = Creep(self, self.niveau_actuel, vitesse, valeur, couleur, taille, self.chemin[0])
            self.creeps.append(creep)

class Vue:
    def __init__(self, root, modele):
        self.root = root
        self.root.title("Tower Defense")
        self.root.geometry("1920x1080")

        self.container = tk.Frame(root)
        self.container.pack()

        self.container_palette_infos = tk.Frame(root)
        self.canvas = tk.Canvas(self.container, width=1320, height=960, bg="black")
        self.canvas.pack()

        self.modele = modele
        self.dessiner_jeu()

        self.timer_running = True
        self.start_time = time.time()
        self.update_timer()

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

    def dessiner_creeps(self):
        x_start = 5.5 * self.modele.cell_size
        y = 2 * self.modele.cell_size

        for creep in self.modele.creeps:
            width = self.modele.cell_size
            height = self.modele.cell_size
            self.canvas.create_oval(x_start, y, x_start + width, y + height, fill="red", outline="white")
            x_start += 0 * width

    def dessiner_creep(self, position):
        width = self.modele.cell_size
        height = self.modele.cell_size
        self.canvas.create_oval(position[0], position[1],
                                position[0] + width, position[1] + height,
                                fill="red", outline="white")

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = max(5 - elapsed_time, 0)

            self.canvas.delete("timer")

            minutes = remaining_time // 60
            seconds = remaining_time % 60

            self.canvas.create_text(100, 700,
                                    text=f"Chrono:\n {minutes:02d}:{seconds:02d}",
                                    font=("Helvetica", 16),
                                    fill="white", tags="timer")

            if remaining_time == 0:
                self.dessiner_creeps()

            self.root.after(1000, self.update_timer)

    def ignore_timer(self, event):
        self.timer_running = False
        self.canvas.delete("timer")
        self.dessiner_creeps()

    def update_vies_label(self):
        self.vies_label.config(text=f"Vies restantes : {self.modele.vies_chateau}")

class Controleur:
    def __init__(self):
        self.root = tk.Tk()
        self.modele = Modele(self.root)
        self.vue = Vue(self.root, self.modele)

    def demarrer(self):
        self.root.mainloop()

def main():
    c = Controleur()
    c.demarrer()

if __name__ == "__main__":
    main()
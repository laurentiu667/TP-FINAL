import tkinter as tk
import random

class Tour:
    def __init__(self):
        self.hauteur = 40
        self.largeur = 40
        self.posX = 0
        self.posY = 0
        self.couleur = ["blue", "yellow", "purple"]
        self.type_tour = [""]


class Creeps:
    def __init__(self):
        self.nombre_creeps = 20
        self.mana = 100
        self.revenu_mort = 20

    def level_up_vie(self):
        pass


class Modele:
    def __init__(self):
        self.cell_size = 40
        self.creeps_list = []
        self.creer_creeps()
        self.largeur = 40
        self.hauteur = 40

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

        self.chateau = [
            [(29, 13, 31, 16), "grey"],
            [(28, 12, 29, 13), "grey"],
            [(31, 12, 32, 13), "grey"]
        ]

    def creer_creeps(self):
        n = Creeps().nombre_creeps
        for i in range(n):
            couleur = "red"
            taille = int(random.randrange(80, 120) / 2)
            creep = Creeps()
            self.creeps_list.append(creep)


class Vue:
    def __init__(self, root, modele):
        self.root = root
        self.root.title("Tower Defense")
        self.root.geometry("1920x1080")

        self.container = tk.Frame(root)
        self.container.pack()

        self.canvas = tk.Canvas(self.container, width=1320, height=960, bg="black")
        self.canvas.pack()

        self.modele = modele
        self.dessiner_tour()

        self.btn_creer_tour = tk.Button(self.container, text="Créer Tour", command=self.creer_tour, background="red")
        self.btn_creer_tour.place(x=100, y=300)
    def creer_tour(self):
        tour = Tour()
        tour.posX = random.randint(0, 10) * self.modele.cell_size  # Position X aléatoire
        tour.posY = random.randint(0, 10) * self.modele.cell_size  # Position Y aléatoire
        tour.couleur = random.choice(tour.couleur)  # Couleur aléatoire
        self.dessiner_tour(tour)

    def dessiner_tour(self, tour):
        x1 = tour.posX
        y1 = tour.posY
        x2 = x1 + tour.largeur
        y2 = y1 + tour.hauteur
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=tour.couleur, outline="")


class Controleur:
    def __init__(self):
        self.modele = Modele()
        self.root = tk.Tk()
        self.vue = Vue(self.root, self.modele)
    def demarrer(self):
        self.root.mainloop()

def main():
    c = Controleur()
    c.demarrer()

if __name__ == "__main__":
    main()

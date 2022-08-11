from tkinter import Tk, Canvas

W, H = 600, 600
MRG = 80

fen = Tk()
fen.title("Jeu du Carré Rouge")
can = Canvas(fen, width=W, height=H, bg="black")
can.pack()


with open("high_score.txt", mode='r') as fichier:
        meilleur_temps = float(fichier.read())


def lancer_partie():
    global temps, xr, yr, dx, dy, tx, ty, rect, carre, xc, yc, etat, chrono
    etat = "initial"
    can.delete("all")
    can.create_rectangle(MRG, MRG, W - MRG, H - MRG,
                         fill="white")
    temps = 0
    # rectangles
    xr, yr = [0, 580, 0, 565], [0, 0, 585, 555]
    dx, dy = [13, -11, 17, -19], [17, 14, -12, -11]
    tx, ty = [50, 20, 60, 35], [50, 70, 15, 45]
    rect = []
    for i in range(4):
        rect.append(can.create_rectangle(xr[i],
                                         yr[i],
                                         xr[i] + tx[i],
                                         yr[i] + ty[i],
                                         fill="blue",
                                         width=3))
    # carré
    xc, yc = W/2 - 20, H/2 -20
    carre = can.create_rectangle(xc, yc, xc + 40, yc + 40,
                                 fill="red",
                                 outline="red4",
                                 width=3)
    # chrono
    chrono = can.create_text(W-10, H-10, text="0.00",
                        font=("liberation mono", 25),
                        fill="white",
                        anchor="se")
    can.create_text(10, H-10, text=f"best = {meilleur_temps/1000:.2f}",
                    font=("liberation mono", 25),
                    fill="white",
                    anchor="sw")

def touche_bord():
    return xc + 40 > W - MRG or xc < MRG\
        or yc + 40 > H - MRG or yc < MRG

def touche_rect():
    for i in range(4):
        if intersection(xr[i], yr[i], tx[i], ty[i]):
            return True
    return False

def intersection(x, y, lx, ly):
    return (xc + 40 > x and xc < x + lx)\
       and (yc + 40 > y and yc < y + ly)

def update():
    global temps, xc, yc, etat, meilleur_temps
    # toutes les 5 secondes, la vitesse augmente de 10%
    if temps % 5000 == 0:
        for i in range(4):
            dx[i] *= 1.1
            dy[i] *= 1.1
    # met à jour le chrono
    can.itemconfig(chrono, text= f"{temps/1000:.2f}",
                   fill = "red" if temps > meilleur_temps else "white")
    # on vérifie si on a perdu
    if touche_bord() or touche_rect():
        can.create_text(W/2, H/2, text="         VA ETUDIER !!!,\n A LA PLACE DE JOUER",
                        font=("liberation mono",23))
        etat = "final"
        if temps > meilleur_temps:
            with open("high_score.txt", mode='w') as fichier:
                fichier.write(str(temps))
            meilleur_temps = temps

        return
    temps += 40
    # on bouge le carre
    xs = fen.winfo_pointerx() - fen.winfo_rootx()
    ys = fen.winfo_pointery() - fen.winfo_rooty()
    xc = xs - decx
    yc = ys - decy
    can.coords(carre, xc, yc, xc + 40, yc + 40)
    # on bouge les rectangles
    for i in range(4):
        xr[i] += dx[i]
        yr[i] += dy[i]
        if xr[i] + tx[i] > W:
            xr[i] = W - tx[i]
            dx[i] = -dx[i]
        elif xr[i] < 0:
            xr[i] = 0
            dx[i] = -dx[i]
        if yr[i] + ty[i] > H:
            yr[i] = H - ty[i]
            dy[i] = -dy[i]
        elif yr[i] < 0:
            yr[i] = 0
            dy[i] = -dy[i]
        can.coords(rect[i],
                   (xr[i], yr[i],
                    xr[i] + tx[i], yr[i] + ty[i]))

    # le format .2f impose 2 chiffres après la virgule
    fen.after(40, update)

def clic(event):
    global decx, decy, etat
    if etat == "en cours":
        return
    if etat == "final":
        lancer_partie()
        return
    xs = fen.winfo_pointerx() - fen.winfo_rootx()
    ys = fen.winfo_pointery() - fen.winfo_rooty()
    decx, decy = xs - xc, ys - yc # décalage entre souris et coin du carre
    if 0 <= decx <= 40 and 0 <= decy <= 40:
        update()
        etat = "en cours"

lancer_partie()

fen.bind("<1>", clic)
fen.mainloop()
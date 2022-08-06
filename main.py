from tkinter import *
from threading import Thread
from time import sleep

x_d = 20
x_a = -20
once_lose = False
cor_x_tijolo = 0
cor_y_tijolo = 0
lines = 16
dic_rects = {}
coordinates = []
velocity = 3
points = 0

def NumbersTijolo(number):
    global cor_x_tijolo, cor_y_tijolo, lines, dic_rects, coordinates

    if coordinates:
        for coordinate in coordinates:
            rect = canvas.create_rectangle(coordinate[0], coordinate[1], coordinate[2], coordinate[3], fill="purple")
            dic_rects[rect] = canvas.coords(rect)
            coordinates = []
    else:
        for c in range(0, number):
            Tijolo(cor_x_tijolo, cor_y_tijolo)
            cor_x_tijolo += 30
            if c == lines:
                lines += 17
                cor_x_tijolo = 0
                cor_y_tijolo += 30
        cor_x_tijolo, cor_y_tijolo, lines = 0, 0, 16
    print(canvas.find_all())

def Tijolo(cor_x, cor_y):
    rect = canvas.create_rectangle(cor_x + 1, cor_y + 1, cor_x + 30, cor_y + 30, fill="purple")
    dic_rects[rect] = canvas.coords(rect)

def MovePlayer1(key):
    global x_d, x_a

    key = key.char
    if key == "d":
        canvas.move(player1, x_d, 0)
    if key == "a":
        canvas.move(player1, x_a, 0)
    if canvas.coords(player1)[0] >= 391:
        x_d = 0
    else:
        x_d = 20
    if canvas.coords(player1)[0] <= 9:
        x_a = 0
    else:
        x_a = -20

def StopBall():
    canvas.move(ball, 0, 0)

def MainBallGame():
    global once_lose, x, y, velocity

    x = -velocity
    y = -velocity
    while True:
        canvas.move(ball, x, y)
        if canvas.coords(ball)[0] >= 480:
            x = -velocity
        if canvas.coords(ball)[1] >= 580:
            if once_lose == False:
                Lose()
                StopBall()
                once_lose = False
                break
        if canvas.coords(ball)[0] <= -2:
            x = velocity
        if canvas.coords(ball)[1] <= -2:
            y = velocity
        x_plataform1, x_plataform2 = canvas.coords(player1)[0], canvas.coords(player1)[2]
        if x_plataform1 <= canvas.coords(ball)[0] <= x_plataform2 and canvas.coords(ball)[1] >= 540:
            print("collid")
            y = -velocity
        BreakBrick()
        sleep(0.0001)

def BreakBrick():
    global x, y, coordinates, velocity, points

    to_delete = ""
    for coords in dic_rects.items():
        if canvas.coords(ball)[0] <= ((coords[1][2] + coords[1][0]) / 2) <= canvas.coords(ball)[2] and canvas.coords(ball)[1] <= ((coords[1][1] + coords[1][3]) / 2) <= canvas.coords(ball)[3]:
            canvas.delete(coords[0])
            velocity += 0.005
            y = velocity
            to_delete = coords[0]
            coordinates.append(coords[1])
            points += 1
            canvas.itemconfig(points_label, text=f"Points:{points}")
    if to_delete != "":
        del dic_rects[to_delete]
    
def Lose():
    global once_lose, points
  
    lose_label = Label(main_root, text="You are lose")
    lose_label.pack(anchor=CENTER, expand=1)
    lose_label.config(font=("Courier", 18), background="blue")
    button_try = Button(main_root, text="Click for retry", background="blue",
                        activebackground="blue", bd=0, command=lambda: StartAndDestroy(lose_label, button_try))
    button_try.place(x=195, y=320)
    once_lose = True

def StartAndDestroy(widget1, widget2):
    widget1.destroy()
    widget2.destroy()
    points = 0
    canvas.itemconfig(points_label, text=f"Points:{points}")
    Thread(target=MainBallGame).start()
    NumbersTijolo(136)

main_root = Tk()
main_root.geometry("500x600")
main_root.resizable(0, 0)
canvas = Canvas(main_root, width=800, height=600, background="blue")
canvas.place(x=-2, y=-2)
player1 = canvas.create_rectangle(250, 570, 350, 580, fill="red")
ball = canvas.create_oval(284, 535, 315, 565, fill="yellow", outline="yellow")
main_root.bind("<Key>", MovePlayer1)
Thread(target=MainBallGame).start()
NumbersTijolo(136)
points_label = canvas.create_text(420, 14, text="Points:0", font=("Courier", 16), fill="white",)
main_root.mainloop()

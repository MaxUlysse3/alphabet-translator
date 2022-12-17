import tkinter as tk

class Writer:
    def __init__(self, win : tk.Canvas, posX : int, posY : int, size : int):
        self.win = win
        self.posX = posX
        self.posY = posY
        self.size = size

class Char:
    
    offsets = [
            (0, 0, 0, 4), # L0
            (0, 4, 4, 2), # L1
            (4, -1, 4, -4), # L2
            (0, -2, 4, -4), # L3
            (0, 2, 2, 3), # L4
            (0, 2, 2, 1), # L5
            (2, 1, 4, 2), # L6
            (2, 1, 2, 3), # L7
            (2, 0, 2, 1), # L8
            (2, -1, 2, -3), # L9
            (0, -2, 2, -3), # L10
            (2, -1, 4, -2), # L11
            (4, -2, 2, -3)] # L12
    
    def __init__(self, posX : int, posY : int, size : int):
        self.posX = posX
        self.posY = posY
        self.size = size
        self.unit = self.size / 4
        
        self.displayed = [True for _ in range(13)]
        self.coords = self.genCoords()

    def genCoords(self):
        for i in enumerate(self.offsets):
            if self.displayed[i[0]]:
                yield (self.posX + i[1][0] * self.unit,
                        self.posY - i[1][1] * self.unit,
                        self.posX + i[1][2] * self.unit,
                        self.posY - i[1][3] * self.unit)

class CharDrawer:
    def __init__(self, win : tk.Canvas, posX : int, posY : int, size : int):
        self.win = win
        self.posX = posX
        self.posY = posY
        self.size = size
        
        self.char = Char(posX, posY, size)

    def draw(self):
        self.win.create_line(self.posX, self.posY, self.posX + self.size, self.posY)
        for i in self.char.genCoords():
            self.win.create_line(i[0], i[1], i[2], i[3])

root = tk.Tk()
root.geometry("500x300")
root.configure(bg="black")

textPanel = tk.PanedWindow(root, bg="black")
textPanel.pack(side=tk.BOTTOM)

text = tk.Entry(textPanel)
text.pack(side=tk.LEFT)

confirm = tk.Button(textPanel, text="Confirmer")
confirm.pack(side= tk.RIGHT)

canva = tk.Canvas(root, width=500, height=300, bg="white")
canva.pack()

c = CharDrawer(canva, 10, 100, 40)

c.draw()

root.mainloop()


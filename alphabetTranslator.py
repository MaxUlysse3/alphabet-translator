import tkinter as tk
import threading

class Writer:
    vowelsList = {
            "": [],
            "a": [1, 2], # a dans "casser"
            "oe": [0], # e dans "peur"
            "e": [0, 2], # e dans "feutre"
            "i": [3], # i dans "image"
            "o": [0, 1, 2, 3], # o dans "objet"
            "u": [0, 2, 3], # u dans "mur"
            "ee": [0, 1, 2], # é dans "épautre"
            "ai": [0, 1, 3], # ai dans "raie"
            "ou": [1, 3], # ou dans "cou"
            "oo": [1, 2, 3], # on dans "ongle"
            "ei": [0, 3], # en dans "lent"
            "ii": [0, 1], # in dans "pain"
            "oa": [2, 3], # o dans "licorne"
            "oi": [1] # o dans "mauve"
            }

    consonantsList = {
            "": [],
            "b": [4, 7, 8, 11],
            "s": [5, 6, 10, 11],
            "d": [4, 5, 6, 11],
            "f": [4, 5, 6, 10, 11, 12],
            "gg": [6, 8, 9, 11],
            "gn": [4, 5, 8, 10, 11],
            "ch": [7, 8, 11, 12],
            "j": [7, 8, 10, 11, 12],
            "k": [4, 5, 6, 7, 8, 10, 12],
            "l": [5, 6, 7, 8, 9, 10, 11],
            "m": [5, 6, 9, 10, 11, 12],
            "n": [5, 6, 10, 11, 12],
            "p": [4, 5, 6, 8, 9],
            "r": [5, 6, 8, 9, 10, 11, 12],
            "z": [4, 5, 11, 12],
            "t": [5, 6, 7, 8, 9],
            "v": [5, 6, 12],
            "w": [4, 5, 6, 7, 8, 10],
            "xs": [5, 11],
            "xz": [5, 8, 9, 11],
            "y": [6, 7, 8, 9, 10]
            }

    def __init__(self, win : tk.Canvas, posX : int, posY : int, size : int):
        self.win = win
        self.posX = posX
        self.posY = posY
        self.size = size

        self.cursor = 0

    def write(self, consonant:str="", vowel:str="", vowelFirst:bool=False, consonantLink:bool=False, vowelLink:bool=False):
        segList = []
        segList += self.vowelsList[vowel]
        segList += self.consonantsList[consonant]
        character = CharDrawer(self.win, self.posX + self.size * self.cursor, self.posY, self.size, segList, [vowelFirst, vowelLink, consonantLink])
        character.draw()

        self.cursor += 1

    def space(self):
        self.cursor += 1

    def changePosY(self, posY):
        self.posY = posY
        self.cursor = 0

    def newLine(self):
        self.posY += self.size * 3
        self.cursor = 0


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
            (0, -2, 2, -1), # L10
            (2, -1, 4, -2), # L11
            (4, -2, 2, -3)] # L12
    
    def __init__(self, posX : int, posY : int, size : int, segList, extraList):
        self.posX = posX
        self.posY = posY
        self.size = size
        self.extraList = extraList
        self.unit = self.size / 4
        
        self.setDisplayed(segList)
        self.coords = self.genCoords()

    def setDisplayed(self, segList):
        self.displayed = [False for _ in range(13)]
        for i in segList:
            self.displayed[i] = True

    def genCoords(self):
        for i in enumerate(self.offsets):
            if self.displayed[i[0]]:
                yield (self.posX + i[1][0] * self.unit,
                        self.posY - i[1][1] * self.unit,
                        self.posX + i[1][2] * self.unit,
                        self.posY - i[1][3] * self.unit)

class CharDrawer:
    def __init__(self, win : tk.Canvas, posX : int, posY : int, size : int, segList, extraList):
        self.win = win
        self.posX = posX
        self.posY = posY
        self.size = size

        self.unit = self.size / 4
        
        self.char = Char(posX, posY, size, segList, extraList)

    def draw(self):
        self.win.create_line(self.posX, self.posY, self.posX + self.size, self.posY)
        for i in self.char.genCoords():
            self.win.create_line(i[0], i[1], i[2], i[3])

        if self.char.extraList[0]:
            self.win.create_oval(self.posX + 3 * self.unit, self.posY - self.size, self.posX + 3 * self.unit, self.posY - self.size)

        if self.char.extraList[1]:
            self.win.create_oval(self.posX + 3.5 * self.unit, self.posY, self.posX + 4.5 * self.unit, self.posY + self.unit)

        if self.char.extraList[2]:
            self.win.create_oval(self.posX + 1.5 * self.unit, self.posY, self.posX + 2.5 * self.unit, self.posY + self.unit)

def writeSentence(writer:Writer, sentence:str):
    words = sentence.split(" ")
    for word in words:
        chars = word.split(".")
        for char in chars:
            c = ""
            v = ""
            vf = False
            cl = False
            vl = False

            if len(char) == 1:
                if char.lower() in Writer.consonantsList:
                    c = char
                elif char.lower() in Writer.vowelsList:
                    v = char
                else:
                    continue

            elif len(char) == 2:
                if char.lower() in Writer.consonantsList:
                    c = char
                elif char.lower() in Writer.vowelsList:
                    v = char
                elif char[1].lower() in Writer.consonantsList:
                    c = char[1]
                    v = char[0]
                    vf = True
                else:
                    c = char[0]
                    v = char[1]

            elif len(char) == 4:
                if (char[2] + char[3]).lower() in Writer.consonantsList:
                    c = char[2] + char[3]
                    v = char[0] + char[1]
                    vf = True
                else:
                    c = char[0] + char[1]
                    v = char[2] + char[3]

            elif len(char) == 3:
                if (char[1] + char[2]).lower() in Writer.consonantsList:
                    c = char[1] + char[2]
                    v = char[0]
                    vf = True
                elif char[2].lower() in Writer.consonantsList:
                    c = char[2]
                    v = char[0] + char[1]
                    vf = True
                elif (char[0] + char[1]).lower() in Writer.consonantsList:
                    c = char[0] + char[1]
                    v = char[2]
                else:
                    c = char[0]
                    v = char[1] + char[2]


            if c.lower() != c:
                cl = True
            if v.lower() != v:
                vl = True

            v = v.lower()
            c = c.lower()
            writer.write(c, v, vf, cl, vl)
        writer.space()

root = tk.Tk()
root.geometry("1200x600")
root.configure(bg="black")

canva = tk.Canvas(root, width=1200, height=600, bg="white")
canva.pack()

writer = Writer(canva, 100, 100, 20)

vow = ""
for i, it in enumerate(list(writer.vowelsList)):
    print(f"{i} -> {it}")
    vow += f"{it} "

con = ""
for i, it in enumerate(list(writer.consonantsList)):
    print(f"{i} -> {it}")
    con += f"{it} "

writeSentence(writer, vow)
writer.newLine()
writeSentence(writer, con)
writer.newLine()

toWrite = str(input("Ecrire : "))
writeSentence(writer, toWrite)

root.mainloop()

import tkinter as tk

class Writer:
    vowelsList = {
            "": [],
            "a": [1, 2],
            "oe": [0],
            "e": [0, 2],
            "i": [3],
            "o": [0, 1, 2, 3],
            "u": [0, 2, 3],
            "ee": [0, 1, 2],
            "ai": [0, 1, 3],
            "ou": [1, 3],
            "oo": [1, 2, 3],
            "ei": [0, 3],
            "ii": [0, 1],
            "oa": [2, 3],
            "oi": [1]
            }

    consonantsList = {
            "": [],
            "b": [4, 7, 8, 11],
            "s": [5, 6, 10, 11],
            "d": [4, 5, 6, 11],
            "f": [4, 5, 6, 10, 11, 12],
            "gu": [6, 8, 9, 11],
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
            toWrite = []
            if len(char) == 1:
                if char in Writer.consonantsList:
                    toWrite.append(char)
                elif char in Writer.vowelsList:
                    toWrite.append("")
                    toWrite.append(char)
                else:
                    continue

            elif len(char) == 2:
                if char in Writer.consonantsList:
                    toWrite.append(char)
                elif char in Writer.vowelsList:
                    toWrite.append("")
                    toWrite.append(char)
                elif char[1] in Writer.consonantsList:
                    toWrite.append(char[1])
                    toWrite.append(char[0])
                    toWrite.append(True)
                else:
                    toWrite.append(char[0])
                    toWrite.append(char[1])

            elif len(char) == 4:
                if char[2] + char[3] in Writer.consonantsList:
                    toWrite.append(char[2] + char[3])
                    toWrite.append(char[0] + char[1])
                    toWrite.append(True)
                else:
                    toWrite.append(char[0] + char[1])
                    toWrite.append(char[2] + char[3])

            elif len(char) == 3:
                if char[1] + char[2] in Writer.consonantsList:
                    toWrite.append(char[1] + char[2])
                    toWrite.append(char[0])
                    toWrite.append(True)
                elif char[2] in Writer.consonantsList:
                    toWrite.append(char[2])
                    toWrite.append(char[0] + char[1])
                    toWrite.append(True)
                elif char[0] + char[1] in Writer.consonantsList:
                    toWrite.append(char[0] + char[1])
                    toWrite.append(char[2])
                else:
                    toWrite.append(char[0])
                    toWrite.append(char[1] + char[2])


            writer.write(*toWrite)
        writer.space()

root = tk.Tk()
root.geometry("1000x500")
root.configure(bg="black")

textPanel = tk.PanedWindow(root, bg="black")
textPanel.pack(side=tk.BOTTOM)

text = tk.Entry(textPanel)
text.pack(side=tk.LEFT)

confirm = tk.Button(textPanel, text="Confirmer")
confirm.pack(side= tk.RIGHT)

canva = tk.Canvas(root, width=1000, height=500, bg="white")
canva.pack()

writer = Writer(canva, 100, 100, 30)

writeSentence(writer, "boo.jou.r")

writer.changePosY(200)

writeSentence(writer, "fi.lee.as")

writeSentence(writer, "jo.ak.im")

writer.changePosY(300)

writeSentence(writer, "xzi.lo.foa.n")
writeSentence(writer, "ka.o")
writeSentence(writer, "ar.mo.ni")

writer.changePosY(400)

writeSentence(writer, "je su.i un li.koa.r.n")


root.mainloop()


import os.path
from tkinter import *
import tkinter.messagebox as GUI
import random
import tkinter


#main.pyw 文件，可以生成exe文件执行时没有黑框
class StudyAssistant:

    def __init__(self):
        self.content = []
        self.current = -1
        self.randomPath = ""
        # for mac os
        wave = os.path.expanduser("~")
        # self.savePath = wave+"/memory_assistant_data/"
        self.savePath = wave+"/python/memory-assistant/hs_data/" # TODO-hs change path
        if not os.path.exists(self.savePath):
            os.mkdir(self.savePath)
    def run(self):
        #main window
        win = Tk()
        win.title("memory assistant")
        win.geometry('900x750')
        # win.configure(bg="gray")

        # input entity
        self.text = Text(win, width=65, height=15, autoseparators=False, font='宋体 16 bold')
        self.text.grid()
        #output entity
        self.var = StringVar()
        Label(win, textvariable=self.var, bg='white', font=('宋体', 15, "bold"), width=65, height=15, justify='left', wraplength=600).place(x=1, y=370)
        #button: add
        Button(win, text='Add', command=self.add).place(x=750, y=80, width=120, height=70)
        button: random
        Button(win, text='One Day random', command=self.randomContent(self.savePath+"1day.txt"), font=('Arial', 12)).place(x=0, y=300, width=150, height=60)
        Button(win, text='Three Days random', command=self.randomContent(self.savePath+"3day.txt"), font=('Arial', 12)).place(x=150, y=300, width=150, height=60)
        Button(win, text='Week random', command=self.randomContent(self.savePath+"7day.txt"), font=('Arial', 12)).place(x=300, y=300, width=150, height=60)
        Button(win, text='Month random', command=self.randomContent(self.savePath+"30day.txt"), font=('Arial', 12)).place(x=450, y=300, width=150, height=60)
        Button(win, text='History random', command=self.randomContent(self.savePath+"history.txt"), font=('Arial', 12)).place(x=600, y=300, width=150, height=60)
        #button: migrate
        Button(win, text='One Day', command=self.migrate(self.savePath+"1day.txt"), font=('Arial', 12)).place(x=0, y=670, width=150, height=60)
        Button(win, text='Three Days', command=self.migrate(self.savePath+"3day.txt"), font=('Arial', 12)).place(x=150, y=670, width=150, height=60)
        Button(win, text='Week', command=self.migrate(self.savePath+"7day.txt"), font=('Arial', 12)).place(x=300, y=670, width=150, height=60)
        Button(win, text='Month', command=self.migrate(self.savePath+"30day.txt"), font=('Arial', 12)).place(x=450, y=670, width=150, height=60)
        Button(win, text='History', command=self.migrate(self.savePath+"history.txt"), font=('Arial', 12)).place(x=600, y=670, width=150, height=60)
        #button: next
        Button(win, text='Next', command=self.next).place(x=750, y=410, width=120, height=70)
        #button: delete
        Button(win, text='Delete', command=self.realDelete).place(x=750, y=520, width=120, height=70)

        win.mainloop()

    # maxNum is contained
    def getRandomList(self, size, maxNum):
        if size > maxNum:
            return list(range(maxNum + 1))
        a = []
        mid = maxNum // 2
        while len(a) < size:
            index = random.randint(0, maxNum)
            if index > mid and random.randint(0, 2) > 0:
                continue
            if index not in a:
                a.append(index)
        return a

    def writeContent(self, file, content):
        if content in ("","\n","\r\n"):
            return
        content = content.replace("\r", "")
        sentences = content.split("\n")
        ret=''
        for s in sentences:
            if s=='':
                continue
            ret+=(s+'\n')
        if len(ret)==0:
            return
        file.write(ret)
        file.flush()
        file.close()

    def tip4ExceedLength(self):
        GUI.showinfo(title='Tip~', message='content exceed max length.')

    def tip4Nothing(self):
        GUI.showinfo(title='Tip~', message='This tag have nothing.')

    def add(self):
        content = self.text.get("0.0", END)
        if len(content) > 100000:
            self.tip4ExceedLength()
            return
        file = open(self.savePath+"1day.txt", "a", encoding="utf8")
        self.writeContent(file, content)
        self.text.delete("0.0", END)

    def randomContent(self, path):
        def func():
            file = open(path, "r", encoding="utf8")
            self.randomPath = path
            data = file.read()
            if not data:
                self.var.set("")
                self.tip4Nothing()
                return
            self.content = []
            self.current = -1
            data = data.split("\n")
            newData = []
            for idx, d in enumerate(data):
                if d != "":
                    newData.append(d)
            randomNum = 20
            if len(newData) <= randomNum:
                self.content = newData
            else:
                randomList = self.getRandomList(randomNum, len(newData) - 1)
                for i in randomList:
                    self.content.append(newData[i])
            self.current += 1
            self.var.set(self.content[self.current])

        return func

    def migrate(self, path):
        def func():
            file = open(path, "a", encoding="utf8")
            if self.current >= len(self.content):
                return
            data = self.content[self.current]
            self.writeContent(file, data)
            # delete
            self.delete()
            # next
            self.next()

        return func

    def realDelete(self):
        result = tkinter.messagebox.askquestion(title='Tip~', message='Are you sure to delete？')
        if result == "yes":
            self.delete()
            self.next()

    def delete(self):
        content = self.var.get()
        if content == "":
            return
        file = open(self.randomPath, "r", encoding="utf8")
        data = file.read().split("\n")
        newData = []
        firstMatch = False
        for d in data:
            if d=="":
                continue
            if not firstMatch and d == content:
                firstMatch = True
                continue
            newData.append(d)
        toWrite = "\n".join(newData)
        if toWrite != "":
            toWrite = toWrite + "\n"
        file.close()
        file = open(self.randomPath, "w", encoding="utf8")
        file.write(toWrite)
        file.flush()
        file.close()

    # next
    def next(self):
        self.current += 1
        if self.current >= len(self.content):
            self.var.set("")
            self.tip4Nothing()
            return
        self.var.set(self.content[self.current])


# main
if __name__ == '__main__':
    StudyAssistant().run()
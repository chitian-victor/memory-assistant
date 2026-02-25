import os.path
from tkinter import *
import tkinter.messagebox as GUI
import random
import tkinter


class StudyAssistant:

    def __init__(self):
        self.content = []
        self.current = -1
        self.random_path = ""

        # for mac os
        wave = os.path.expanduser("~")
        self.save_path = wave + "/my_github/memory-assistant/data/"  # TODO-hs debug path
        # self.save_path = wave + "/memory-assistant/data/"  # TODO-hs prod path

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def run(self):
        # main window
        win = Tk()
        win.title("memory assistant")
        win.geometry('900x750')

        # input entity (修正为 place 布局)
        self.text = Text(win, autoseparators=False, font=('宋体', 16, 'bold'))
        self.text.place(x=10, y=10, width=720, height=260)

        # output entity
        self.var = StringVar()
        Label(win, textvariable=self.var, bg='white', font=('宋体', 15, "bold"), justify='left', wraplength=600).place(
            x=10, y=370, width=720, height=280)

        # button: add
        Button(win, text='Add', command=self.add).place(x=750, y=80, width=120, height=70)

        # button: random
        Button(win, text='One Day random', command=self.random_content(self.save_path + "1day.txt"),
               font=('Arial', 12)).place(x=0, y=300, width=150, height=60)
        Button(win, text='Three Days random', command=self.random_content(self.save_path + "3day.txt"),
               font=('Arial', 12)).place(x=150, y=300, width=150, height=60)
        Button(win, text='Week random', command=self.random_content(self.save_path + "7day.txt"),
               font=('Arial', 12)).place(x=300, y=300, width=150, height=60)
        Button(win, text='Month random', command=self.random_content(self.save_path + "30day.txt"),
               font=('Arial', 12)).place(x=450, y=300, width=150, height=60)
        Button(win, text='History random', command=self.random_content(self.save_path + "history.txt"),
               font=('Arial', 12)).place(x=600, y=300, width=150, height=60)

        # button: migrate
        Button(win, text='One Day', command=self.migrate(self.save_path + "1day.txt"), font=('Arial', 12)).place(x=0,
                                                                                                                 y=670,
                                                                                                                 width=150,
                                                                                                                 height=60)
        Button(win, text='Three Days', command=self.migrate(self.save_path + "3day.txt"), font=('Arial', 12)).place(
            x=150, y=670, width=150, height=60)
        Button(win, text='Week', command=self.migrate(self.save_path + "7day.txt"), font=('Arial', 12)).place(x=300,
                                                                                                              y=670,
                                                                                                              width=150,
                                                                                                              height=60)
        Button(win, text='Month', command=self.migrate(self.save_path + "30day.txt"), font=('Arial', 12)).place(x=450,
                                                                                                                y=670,
                                                                                                                width=150,
                                                                                                                height=60)
        Button(win, text='History', command=self.migrate(self.save_path + "history.txt"), font=('Arial', 12)).place(
            x=600, y=670, width=150, height=60)

        # button: next
        Button(win, text='Next', command=self.next).place(x=750, y=410, width=120, height=70)

        # button: delete
        Button(win, text='Delete', command=self.real_delete).place(x=750, y=520, width=120, height=70)

        win.mainloop()

    # max_num is contained
    def get_random_list(self, size, max_num):
        if size > max_num:
            return list(range(max_num + 1))

        a = []
        mid = max_num // 2
        while len(a) < size:
            index = random.randint(0, max_num)
            if index > mid and random.randint(0, 2) > 0:
                continue
            if index not in a:
                a.append(index)
        return a

    def write_content(self, file, content):
        if content in ("", "\n", "\r\n"):
            return

        content = content.replace("\r", "")
        sentences = content.split("\n")
        ret = ''

        for s in sentences:
            if s == '':
                continue
            ret += (s + '\n')

        if len(ret) == 0:
            return

        file.write(ret)
        file.flush()
        file.close()

    def tip_for_exceed_length(self):
        GUI.showinfo(title='Tip~', message='content exceed max length.')

    def tip_for_nothing(self):
        GUI.showinfo(title='Tip~', message='This tag have nothing.')

    def add(self):
        content = self.text.get("0.0", END)
        if len(content) > 100000:
            self.tip_for_exceed_length()
            return

        file = open(self.save_path + "1day.txt", "a", encoding="utf8")
        self.write_content(file, content)
        self.text.delete("0.0", END)

    def random_content(self, path):
        def func():
            file = open(path, "r", encoding="utf8")
            self.random_path = path
            data = file.read()

            if not data:
                self.var.set("")
                self.tip_for_nothing()
                return

            self.content = []
            self.current = -1
            data = data.split("\n")
            new_data = []

            for idx, d in enumerate(data):
                if d != "":
                    new_data.append(d)

            random_num = 20
            if len(new_data) <= random_num:
                self.content = new_data
            else:
                random_list = self.get_random_list(random_num, len(new_data) - 1)
                for i in random_list:
                    self.content.append(new_data[i])

            self.current += 1
            self.var.set(self.content[self.current])

        return func

    def migrate(self, path):
        def func():
            file = open(path, "a", encoding="utf8")
            if self.current >= len(self.content):
                return
            data = self.content[self.current]
            self.write_content(file, data)
            # delete
            self.delete()
            # next
            self.next()

        return func

    def real_delete(self):
        result = tkinter.messagebox.askquestion(title='Tip~', message='Are you sure to delete？')
        if result == "yes":
            self.delete()
            self.next()

    def delete(self):
        content = self.var.get()
        if content == "":
            return

        file = open(self.random_path, "r", encoding="utf8")
        data = file.read().split("\n")
        new_data = []
        first_match = False

        for d in data:
            if d == "":
                continue
            if not first_match and d == content:
                first_match = True
                continue
            new_data.append(d)

        to_write = "\n".join(new_data)
        if to_write != "":
            to_write = to_write + "\n"

        file.close()

        file = open(self.random_path, "w", encoding="utf8")
        file.write(to_write)
        file.flush()
        file.close()

    # next
    def next(self):
        self.current += 1
        if self.current >= len(self.content):
            self.var.set("")
            self.tip_for_nothing()
            return
        self.var.set(self.content[self.current])


# main
if __name__ == '__main__':
    StudyAssistant().run()
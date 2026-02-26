import os.path
from tkinter import *
import tkinter.messagebox as GUI
from pathlib import Path
from v2.utils.cal_weight import *
from v2.model.item import *


# TODO-hs
# 2. 丢给 agent 优化一下 (已完成)
# 3. 支持手动调整条目数量
# 4. 调整按钮颜色

class MemoryAssistant:
    def __init__(self):
        # 基础常量
        self.separator = ', '  # 条目属性信息记录的分隔符，包括首次添加时间，上次背诵时间，不认识次数，权重
        self.file_name = "items.txt"
        self.review_amount=20 # todo-hs 支持修改,必须大于 0
        self.current_idx=0
        self.items=[]

        # 1. 初始化文件
        # for mac os
        wave = os.path.expanduser("~")
        self.save_path = wave + "/my_github/memory-assistant/v2/data/" + self.file_name  # TODO-hs debug path
        # self.save_path = wave + "/memory-assistant/data/" + self.file_name # TODO-hs prod path
        file_path = Path(self.save_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 2. 加载全部条目,重新计算权重
        with open(file_path, 'r+', encoding='utf-8') as f:
            data = f.read()
            if data.strip():
                self.items = self.parse_items(data)
                print_items(self.items)
    def parse_items(self, data):
        # [首次添加时间, 上次背诵时间, 不认识次数, 权重]
        data_list = data.split('\n')
        data_list = data_list[:-1]
        items = []
        for i in range(0, len(data_list), 2):
            item_idx, info_idx = i, i + 1
            info = data_list[info_idx]
            info_list = info.split(self.separator)

            item = ItemCls(data_list[item_idx], info_list[0], info_list[1], int(info_list[2]))
            item.weight = cal_item_weight(item)
            # 过滤掉不认识次数为 0 的 ，只在软件初始化的时候才会排除在外，之后会跟随刷新数据
            if item.forget_times <= 0:
                continue
            items.append(item)
        # 排序
        items=sorted(items,key=lambda x:x.weight,reverse=True)
        return items

    def run(self):
        # main window
        win = Tk()
        win.title("memory-assistant")
        win.geometry('900x750')
        # input entity
        self.text = Text(win, autoseparators=False, font=('宋体', 16, 'bold'))
        self.text.place(x=10, y=10, width=720, height=260)
        # output entity
        self.var = StringVar()

        (Label(win, textvariable=self.var, bg='white', font=('宋体', 15, "bold"), justify='left', wraplength=600).
         place(x=10, y=370, width=720, height=280))
        # button: add
        (Button(win, text='Add', command=self.add).
         place(x=750, y=80, width=120, height=70))
        # button: review
        (Button(win, text='Review', command=self.generate_review_list, font=('Arial', 12)).
         place(x=0, y=300, width=150,height=60))
        # button: know
        (Button(win, text='Know', command=self.next(True)).
         place(x=750, y=410, width=120, height=70))
        # button: don't know
        (Button(win, text="Don't know", command=self.next(False)).
         place(x=750, y=520, width=120, height=70))
        # button: delete
        (Button(win, text='Delete', command=self.delete).
         place(x=0, y=670, width=150, height=60))
        win.mainloop()
        # 软件结束之后将 items 覆盖写入
        print("[run] flush items, items.length=%d"%(len(self.items)))
        self.flush_items()
    def flush_items(self):
        file = open(self.save_path, "w", encoding="utf8")
        self.batch_write_items(file,self.items)

    def generate_review_list(self):
        self.current_idx=0
        self.items=sorted(self.items,key=lambda x:x.weight,reverse=True)
        if len(self.items)==0:
            self.tip_for_nothing()
            return
        self.var.set(self.items[self.current_idx].data)

    def convert_content_to_item(self,content):
        # support batch input
        if content in ("", "\n", "\r\n"):
            return
        content = content.replace("\r", "")
        item_data_list = content.split("\n")
        items=[]
        current_time = format_current_time()
        for item_data in item_data_list:
            if not item_data:
                continue
            item=ItemCls(item_data,current_time,current_time,3)
            item.weight=cal_item_weight(item)
            items.append(item)
        return items
    def batch_write_items(self,file,items):
        # iterate items
        ret = ''
        for item in items:
            ret += self.format_item(item) + '\n'
        if len(ret) == 0:
            return
        file.write(ret)
        file.flush()
        file.close()

    def format_item(self, item: ItemCls):
        # [首次添加时间, 上次背诵时间, 不认识次数, 权重]，不认识次数默认为 3
        ret = item.data + '\n' + self.separator.join([item.create_time,item.last_time, str(item.forget_times), str(item.weight)])
        return ret
    def add(self):
        content = self.text.get("0.0", END)
        if len(content) > 100000:
            self.tip_for_exceed_length()
            return

        file = open(self.save_path, "a", encoding="utf8")
        items = self.convert_content_to_item(content)
        # 添加到末尾
        self.items+=items
        self.batch_write_items(file, items)
        self.text.delete("0.0", END)

    def delete(self):
        if self.current_idx < len(self.items):
            item=self.items[self.current_idx]
            item.update_forget_times(0)
            item.update_last_time(format_current_time())
        self.next(True)()
        self.flush_items()

    # next
    def next(self,know: bool):
        def next_():
            if len(self.items)==0:
                return
            increment = -1 if know else 1
            item=self.items[self.current_idx]
            # next触发的时候，更新item及权重
            item.update_forget_times(max(0,item.forget_times+increment))
            item.update_last_time(format_current_time())
            self.current_idx+=1
            self.flush_items()
            if self.current_idx>=self.review_amount or self.current_idx >= len(self.items):
                self.var.set("")
                self.tip_for_nothing()
                return
            self.var.set(self.items[self.current_idx].data)
        return next_

    def tip_for_exceed_length(self):
        GUI.showinfo(title='Tip~', message='content exceed max length.')

    def tip_for_nothing(self):
        GUI.showinfo(title='Tip~', message='there is nothing to review.')

# main
if __name__ == '__main__':
    MemoryAssistant().run()
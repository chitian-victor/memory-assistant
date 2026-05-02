import os.path
from tkinter import *
import tkinter.messagebox as GUI
from pathlib import Path
from utils.cal_weight import *
from model.item import *
from tkmacosx import Button  # 从 tkmacosx 导入 Button 为了适配 mac 系统，解决按钮背景色不生效的问题

class MemoryAssistant:
    def __init__(self):
        # 基础常量
        self.info_separator = ', '  # 词条属性信息记录的分隔符，包括首次添加时间，上次背诵时间，不认识次数，权重
        self.item_separator = '\n'+'=*='*10+'\n'  # 词条之间的分隔符
        self.item_info_separator = '\n'+'--'*10+'\n'  # 词条与属性信息的分隔符
        self.review_target_text="Ready to Review. Target: %d / %d"
        self.file_name = "items.txt"
        self.review_amount=20
        self.current_idx=-1
        self.items=[]

        # 1. 初始化文件
        # for mac os
        wave = os.path.expanduser("~")
        # 我把自己的私有数据单独存入另一个 github 仓库了
        # self.save_path = wave + "/my_github/memory-assistant-private/v2/data/" + self.file_name # TODO-hs prod path
        self.save_path = wave + "/my_github/memory-assistant/v2/data/" + self.file_name  # TODO-hs debug path
        file_path = Path(self.save_path)
        # 不存在就创建文件夹及文件
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        # 2. 加载全部词条,重新计算权重
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
            if data.strip():
                self.items = self.parse_items(data)
                # print_items(self.items) # debug
    def parse_items(self, data):
        # 词条属性信息格式：[首次添加时间, 上次背诵时间, 不认识次数, 权重]
        data_list = data.split(self.item_separator)
        if not data_list[-1]:
            data_list = data_list[:-1]
        items = []
        for i in range(len(data_list)):
            item_str=data_list[i].split(self.item_info_separator)
            data=item_str[0]
            info = item_str[1]
            info_list = info.split(self.info_separator)

            item = ItemCls(data, info_list[0], info_list[1], int(info_list[2]))
            item.weight = cal_item_weight(item)
            # 过滤掉不认识次数为 0 的 ，只在软件初始化的时候才会排除在外，之后会跟随刷新数据
            if item.forget_times <= 0:
                continue
            items.append(item)
        # 排序
        items=sorted(items,key=lambda x:x.weight,reverse=True)
        return items

    def run(self):
        # main window setup
        win = Tk()
        win.title("Memory Assistant")
        win.geometry('900x750')
        win.configure(bg="#F5F5F7")  # 柔和的浅灰背景

        # --- SECTION 1: Input Area (支持滚动条滑动输入) ---
        Label(win, text="Add New Item:", bg="#F5F5F7", font=('Helvetica', 14, 'bold'),
              fg="#333333").place(x=20, y=10)

        # 使用 Frame 包裹输入框和滚动条
        self.input_frame = Frame(win, bg='white', highlightthickness=1, highlightbackground="#CCCCCC")
        self.input_frame.place(x=20, y=40, width=710, height=200)

        # 输入区滚动条
        self.input_scrollbar = Scrollbar(self.input_frame)
        self.input_scrollbar.pack(side=RIGHT, fill=Y)

        # 输入文本框
        self.text = Text(self.input_frame, autoseparators=False, font=('宋体', 16), bd=0,
                         yscrollcommand=self.input_scrollbar.set, wrap=WORD)
        self.text.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        self.input_scrollbar.config(command=self.text.yview)

        Button(win, text='Add', command=self.add, bg="#5AC8FA", fg="white", font=('Helvetica', 16, 'bold'),
               borderless=1).place(x=750, y=40, width=130, height=200)

        # Divider line
        Frame(win, bg="#D1D1D6").place(x=20, y=265, width=860, height=2)

        # --- SECTION 2: Review Area (左对齐展示区 + 动态复习数量) ---
        self.status_var = StringVar()
        self.status_var.set("Ready to Review. Target: 0 / 0")
        Label(win, textvariable=self.status_var, bg="#F5F5F7", font=('Helvetica', 14, 'italic'), fg="#666666").place(
            x=20, y=285)

        # 复习数量修改
        Label(win, text="Review Amount:", bg="#F5F5F7", font=('Helvetica', 13), fg="#8E8E93").place(x=540, y=288)

        self.entry_bg = Frame(win, bg="#E5E5EA", highlightthickness=0)  # 极浅的灰色背景
        self.entry_bg.place(x=670, y=285, width=60, height=30)

        self.amount_var = StringVar(value=str(self.review_amount))
        self.amount_entry = Entry(self.entry_bg, textvariable=self.amount_var, font=('Helvetica', 14, 'bold'),
                                  bg="#E5E5EA", fg="#333333", justify='center',
                                  bd=0, highlightthickness=0)
        # 让输入框完全填满底层的小 Frame
        self.amount_entry.pack(fill=BOTH, expand=True, padx=2, pady=2)
        # button review
        Button(win, text='Start Review', command=self.generate_review_list, bg="#63B8FF", fg="white",
               font=('Helvetica', 14, 'bold'), borderless=1).place(x=750, y=280, width=130, height=40)
        # 使用 Frame 包裹展示区和滚动条
        self.display_frame = Frame(win, bg='white', relief="groove", borderwidth=2)
        self.display_frame.place(x=20, y=340, width=860, height=250)

        # 展示区滚动条
        self.display_scrollbar = Scrollbar(self.display_frame)
        self.display_scrollbar.pack(side=RIGHT, fill=Y)

        # 展示文本框
        self.display_text = Text(self.display_frame, font=('宋体', 18), bg='white',
                                 yscrollcommand=self.display_scrollbar.set, wrap=WORD,
                                 highlightthickness=0, borderwidth=0)

        self.display_text.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        self.display_scrollbar.config(command=self.display_text.yview)
        self.display_text.config(state=DISABLED)  # 初始只读

        # --- SECTION 3: Action Controls ---
        Button(win, text='KNOW', command=self.next(True), bg="#A1E9B4", fg="#1E6130",
               font=('Helvetica', 16, 'bold'), borderless=1).place(x=20, y=620, width=320, height=80)

        Button(win, text="DON'T KNOW", command=self.next(False), bg="#FFF68F", fg="#8A1E1E",
               font=('Helvetica', 16, 'bold'), borderless=1).place(x=360, y=620, width=320, height=80)

        Button(win, text='Delete', command=self.delete, bg="#828282", fg="#FFFFFF", font=('Helvetica', 14),
               borderless=1).place(x=700, y=620, width=180, height=80)
        win.mainloop()
        print(f"[run] flush items, items.length={len(self.items)}")
        self.flush_items()

    def generate_review_list(self):
        self.update_review_amount()
        self.current_idx = 0
        self.items = sorted(self.items, key=lambda x: x.weight, reverse=True)
        if len(self.items) == 0:
            self.tip_for_nothing()
            return

        self.update_status_var()
        self.update_display_text(self.items[self.current_idx].data)
    def flush_items(self):
        with open(self.save_path, "w", encoding="utf8") as f:
            self.batch_write_items(f,self.items)

    def convert_content_to_items(self,content):
        # support batch input
        items=[]
        current_time = format_current_time()
        item=ItemCls(content,current_time,current_time,3)
        item.weight=cal_item_weight(item)
        items.append(item)
        return items
    def batch_write_items(self,file,items):
        # iterate items
        ret = ''
        for item in items:
            ret += self.format_item(item) + self.item_separator
        if len(ret) == 0:
            return
        file.write(ret)
        file.flush()
        file.close()

    def format_item(self, item: ItemCls):
        # [首次添加时间, 上次背诵时间, 不认识次数, 权重]，不认识次数默认为 3
        ret = item.data + self.item_info_separator + self.info_separator.join([item.create_time,item.last_time, str(item.forget_times), str(item.weight)])
        return ret
    def add(self):
        content = self.text.get("0.0", END)
        if len(content) > 100000:
            self.tip_for_exceed_length()
            return
        content=content.rstrip()
        if len(content)==0:
            return
        items = self.convert_content_to_items(content)
        # 添加到末尾
        self.items+=items
        with open(self.save_path, "a", encoding="utf8") as f:
            self.batch_write_items(f, items)
            self.text.delete("0.0", END)

    def delete(self):
        if 0<=self.current_idx < min(len(self.items),self.review_amount) :
            item=self.items[self.current_idx]
            item.update_forget_times(0)
            item.update_last_time(format_current_time())
            self.next(True)()
            self.flush_items()

    # next
    def next(self,know: bool):
        def next_():
            if len(self.items)==0 or self.current_idx>=min(self.review_amount,len(self.items))  or self.current_idx<0:
                return
            increment = -1 if know else 1
            item=self.items[self.current_idx]
            # next触发的时候，更新item及权重
            item.update_forget_times(max(0,item.forget_times+increment))
            item.update_last_time(format_current_time())
            self.current_idx+=1
            self.flush_items()
            self.update_status_var()
            if self.current_idx>=self.review_amount or self.current_idx >= len(self.items):
                self.update_display_text("")
                self.tip_for_nothing()
                return
            self.update_display_text(self.items[self.current_idx].data)
        return next_

    def update_status_var(self):
        review_target_text= self.review_target_text % (self.current_idx, self.review_amount)
        self.status_var.set(review_target_text)
    def update_display_text(self, content):
        """安全地更新展示区的文本内容（左对齐）"""
        self.display_text.config(state=NORMAL)
        self.display_text.delete("1.0", END)
        self.display_text.insert("1.0", content)
        # 默认左对齐
        self.display_text.config(state=DISABLED)
    def update_review_amount(self):
        try:
            input_amount = int(self.amount_var.get().strip())
            if input_amount > 0:
                self.review_amount = input_amount
            else:
                GUI.showwarning("Invalid Input", "Review amount must be greater than 0. Using previous value.")
                self.amount_var.set(str(self.review_amount))
        except ValueError:
            GUI.showwarning("Invalid Input", "Please enter a valid number. Using previous value.")
            self.amount_var.set(str(self.review_amount))
    def tip_for_exceed_length(self):
        GUI.showinfo(title='Tip~', message='content exceed max length.')

    def tip_for_nothing(self):
        GUI.showinfo(title='Tip~', message='there is nothing to review.')

# main
if __name__ == '__main__':
    MemoryAssistant().run()

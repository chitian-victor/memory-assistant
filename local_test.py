
import tkinter as tk
from tkinter import messagebox

print(tk.TkVersion)
def main():
    try:
        root = tk.Tk()
        root.title("测试窗口")
        label = tk.Label(root, text="这是一个测试标签")
        label.pack()
        root.mainloop()
    except Exception as e:
        messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    main()
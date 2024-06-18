# 创建：ZhengYL
# 创建日期：2024/05/02 16:43
# 描述：GUI窗体

import tkinter as tk
from tkinter import filedialog

# 弹窗获取文件夹
class PopUp:
    def __init__(self, name, left="浏览", right="提交") -> None:
        self.folder_path = ""
        self.root = tk.Tk()
        self.name = name
        self.left = left
        self.right = right
        self.folder_label = tk.Label(self.root, text="请选择文件夹")
        self.folder_label.pack(padx=5, pady=5)

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.folder_label.config(text=self.folder_path)

    def pop_up(self):
        self.root.title("{}".format(self.name))
        self.root.geometry("300x150")
        browse_button = tk.Button(self.root, text=self.left, command=self.browse_folder)
        browse_button.pack(padx=5, pady=5)
        upload_button = tk.Button(self.root, text=self.right, command=self.root.destroy)
        upload_button.pack(padx=5, pady=5)
        self.root.mainloop()
        return self.folder_path

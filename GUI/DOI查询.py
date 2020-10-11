import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import webbrowser
from win10toast import ToastNotifier
import base64
from icon import img
import os

tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()


# 定义Button的功能，即一个函数
# 窗口root后面再声明，在函数内部使用全局变量

def rootlabel(ev = None):
    global root
    doi = e1.get()
    ulr1 = 'https://doi.org/'+str(doi)
    item = cheack(ulr1)
    if item == 'Error: DOI Not Found':
        item = '抱歉，查询不到该DOI！'
    else:
        webbrowser.open(ulr1)
        toaster = ToastNotifier()
        toaster.show_toast(
            "恭喜！！", "论文已见刊!", icon_path="logo.ico", duration=5, threaded=True)
    listb.insert(0, item)
    # Label(root, text=cheack('https://doi.org/'+str(doi)), fg='#000000')

def cheack(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    return soup.title.text


# 定义一个窗口"root"
root = tk.Tk()

# 设置窗口大小
winWidth = 600
winHeight = 400
# 获取屏幕分辨率
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)

root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
root.title("DOI查询器")
root.iconbitmap('tmp.ico')

os.remove("tmp.ico")

l = ttk.Label(root, text='请输入DOI：')
l.grid(row=0, column=0, padx=15, sticky=tk.EW)

e1 = ttk.Entry(root)
e1.insert(0, '10.3233/JAE-209356')
e1.grid(row=0, column=1, sticky=tk.EW)

# 定义一个按钮"b1",在"root"中显示，显示文本"SCU"，命令为函数"rootlabel"
b1 = ttk.Button(root, text='DOI查询', command=rootlabel)

# 将"b1"布局出来
b1.grid(row=0, column=2, padx=10, pady=5)

# sp=tk.Separator(root,orient='horizontal').grid(row=1, columnspan=3)

b=ttk.Separator(root,orient='horizontal')
b.grid(row = 1, columnspan=3, sticky='EW')

root.rowconfigure(2,weight=1)
root.columnconfigure(1,weight=1)

listb = tk.Listbox(root, width=40, selectbackground='#1E6EFF')
listb.grid(row=2, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)


root.bind('<Return>', rootlabel)

# 定义窗口无边框
# root.overrideredirect(1)




root.maxsize(1500, 800)
root.minsize(700, 150)


# 主循环
root.mainloop()

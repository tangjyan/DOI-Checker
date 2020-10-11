import tkinter as tk
from tkinter.dialog import Dialog
from tkinter import messagebox
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import webbrowser
from win10toast import ToastNotifier
import base64
from icon import img
from datetime import datetime
import time
import threading
import winsound
import os

import ctypes
#告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
#获取屏幕的缩放因子
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)


tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()


class basedesk():
    def __init__(self, master):
        self.root = master
        self.root.config()
        # 设置窗口大小
        winWidth = 900
        winHeight = 400
        
        #设置程序缩放
        self.root.tk.call('tk', 'scaling', ScaleFactor/75) #适配高分屏

        # 获取屏幕分辨率
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        self.root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        self.root.title("DOI查询器")
        self.root.iconbitmap('tmp.ico')
        os.remove("tmp.ico")

        self.root.maxsize(1000, 600)
        self.root.minsize(500, 200)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # i1=clicface.__new__(clicface)
        # a1=autoface.__new__(autoface)

        self.menubar = tk.Menu(self.root)
        self.view_menu = tk.Menu(self.menubar, tearoff=False)
        self.view_menu.add_command(
            label='单次查询', underline=1, command=self.chInits, accelerator="Alt+W")
        self.view_menu.add_command(
            label='循环查询', underline=1, command=self.chAuto, accelerator="Alt+X")
        # self.view_menu.add_command(
        #     label='DOI网页', underline=1, command=self.chweb, accelerator="Alt+X")
        self.view_menu.add_separator()
        self.view_menu.add_command(
            label='退出', underline=1, command=self.root.destroy, accelerator="Ctrl+Q")
        self.about_menu = tk.Menu(self.menubar, tearoff=False)
        self.about_menu.add_command(
            label='关于', underline=1, command=self.menuabout)
        self.about_menu.add_command(
            label='说明', underline=1, command=self.menudoc)

        for (item1, item2) in zip(['视图', '关于'], [self.view_menu, self.about_menu]):
            self.menubar.add_cascade(label=item1, menu=item2)
        self.root.config(menu=self.menubar)
        self.root.bind("<Alt-w>", lambda event: self.chInits())
        self.root.bind("<Alt-x>", lambda event: self.chAuto())
        self.root.bind("<Control-q>", lambda event: os._exit(0))

        self.a1 = autoface(self.root)

    def chAuto(self):
        if frame_state == 2:
            self.c1.initface.destroy()
            self.a1 = autoface(self.root)

    def chInits(self):
        if frame_state == 1:
            self.a1.multface.destroy()
            self.c1 = clicface(self.root)

    def menuabout(self):
        # self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='1.gif'))
        # messagebox.showinfo('关于', '版本：V 0.3\n时间：2020年10月1日\n作者：小山神')
        Dialog(self.root, title='关于', text='版本：V 0.3\n时间：2020年10月1日\n作者：小山神',
               bitmap='', default=0, cancel=3, strings=('  关   闭  ',))

    def menudoc(self):
        Dialog(self.root, title='说明', text='      本软件可以查询DOI是否正式生效，在“单次查询”模式中为点击按钮触发查询，在“循环查询”模式中可以设定扫描时间，自动隔一段时间查询是否生效。',
               bitmap='info', default=0, cancel=3, strings=('  关   闭  ',))


class clicface():
    def __init__(self, master):
        global frame_state
        frame_state = 2
        self.master = master
        self.master.config(bg='green')

        self.initface = tk.Frame(self.master)
        self.initface.grid(sticky=tk.NSEW)
        self.initface.rowconfigure(2, weight=1)
        self.initface.columnconfigure(1, weight=1)

        self.l = ttk.Label(self.initface, text='请输入DOI：')
        self.l.grid(row=0, column=0, padx=5, sticky=tk.EW)

        self.e1 = ttk.Entry(self.initface)
        self.e1.insert(0, '10.3233/JAE-209356')
        self.e1.grid(row=0, column=1, sticky=tk.EW)

        # 定义一个按钮"b1",在"initface"中显示，显示文本"SCU"，命令为函数"rootlabel"
        self.b1 = ttk.Button(self.initface, text='DOI查询',
                             command=self.rootlabel)
        # 将"b1"布局出来
        self.b1.grid(row=0, column=2, padx=5, pady=5)
        self.b1.bind('<Return>', lambda event: self.rootlabel())

        self.sp = ttk.Separator(self.initface, orient='horizontal')
        self.sp.grid(row=1, columnspan=3, sticky=tk.EW)

        self.listb = tk.Listbox(self.initface, width=40,
                                selectbackground='#1E6EFF')
        self.listb.grid(row=2, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)

    def rootlabel(self):
        doi = self.e1.get()
        ulr1 = 'https://doi.org/'+str(doi)
        item = self.cheack(ulr1)
        if item == 'Error: DOI Not Found':
            item = '  抱歉，查询不到该DOI！'
        else:
            webbrowser.open(ulr1)
            toaster = ToastNotifier()
            toaster.show_toast(
                "  恭喜！！", "论文已见刊!", icon_path="logo.ico", duration=5, threaded=True)
        self.listb.insert(0, item)
        # Label(root, text=cheack('https://doi.org/'+str(doi)), fg='#000000')

    def cheack(self, url):
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        return soup.title.text


class autoface():
    def __init__(self, master):
        global frame_state
        frame_state = 1
        self.master = master
        # self.master.config(bg='green')

        self.multface = tk.Frame(self.master)
        self.multface.grid(sticky=tk.NSEW)
        self.multface.rowconfigure(2, weight=1)
        self.multface.columnconfigure(1, weight=1)

        self.l = ttk.Label(self.multface, text='请输入DOI：')
        self.l.grid(row=0, column=0, padx=5, sticky=tk.W)

        self.e1 = ttk.Entry(self.multface)
        self.e1.insert(0, '10.3233/JAE-209356')
        self.e1.grid(row=0, column=1, sticky=tk.EW)

        self.l2 = ttk.Label(self.multface, text='刷新周期:')
        self.l2.grid(row=0, column=2, padx=5, sticky=tk.E)

        self.e2 = tk.Entry(self.multface, width=4, bg='white')
        self.e2.insert(0, '1')
        self.e2.grid(row=0, column=3, sticky=tk.EW)

        self.l3 = ttk.Label(self.multface, text='min')
        self.l3.grid(row=0, column=4, sticky=tk.E)

        # 定义一个按钮"b1",在"multface"中显示，显示文本"SCU"，命令为函数"rootlabel"
        self.b1 = ttk.Button(self.multface, text='开始监控', width=10,
                             command=self.threadend)
        # 将"b1"布局出来
        self.b1.grid(row=0, column=5, padx=5, pady=5, sticky=tk.E)
        self.master.bind('<Return>', lambda event: self.threadend())

        # 定义一个按钮"b2",在"multface"中显示，显示文本"SCU"，命令为函数"rootlabel"
        self.b2 = ttk.Button(self.multface, text='停止', width=5,
                             command=self.endloop)
        # 将"b2"布局出来
        self.b2.grid(row=0, column=6, padx=5, pady=5, sticky=tk.E)
        self.master.bind('<Escape>', lambda event: self.endloop())

        self.sp = ttk.Separator(self.multface, orient='horizontal')
        self.sp.grid(row=1, columnspan=7, sticky=tk.EW)

        self.listb = tk.Listbox(self.multface, width=40,
                                selectbackground='#1E6EFF')
        self.listb.grid(row=2, columnspan=7, padx=5, pady=5, sticky=tk.NSEW)

    def rootlabel(self):
        i = 1
        doi = self.e1.get()
        url1 = 'https://doi.org/'+str(doi)
        global loopsig
        loopsig = True
        while loopsig:
            try:
                # "%H:%M:%S"
                tnum = '  第'+str(i)+'次-------' + \
                    datetime.now().strftime("%H:%M:%S") + '---------'

                ch1 = self.cheack(url1)
                if ch1 == 'Error: DOI Not Found':
                    ch1 = '  抱歉，查询不到该DOI！'
                    self.listb.insert(0, ch1)
                    self.listb.insert(0, tnum)
                    self.listb.update()
                else:
                    self.listb.insert(0, ch1)
                    self.listb.insert(0, tnum)
                    self.listb.update()
                    webbrowser.open(url1)
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        "恭喜！！", "论文已见刊!", icon_path="logo.ico", duration=5, threaded=True)
                    break
                # chtitile=self.cheack1(url3)

                deltime = int(float(self.e2.get())*60)
                time.sleep(deltime)
                i = i+1
            except:
                break

    def endloop(self):
        self.e2['bg'] = 'white'
        self.e2['fg'] = 'black'
        self.e2.update()
        global loopsig
        loopsig = False

    def threadend(self):
        self.listb.delete(0, tk.END)
        self.e2['bg'] = '#DD4F42'
        self.e2['fg'] = 'white'

        self.e2.update()
        t = threading.Thread(target=self.rootlabel)
        t.start()

    def cheack(self, url):
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')

        return soup.title.text

    # def Quit(self):
    #     # self.master.destroy()
    #     os._exit(0)


if __name__ == '__main__':
    root = tk.Tk()
    frame_state = 0
    basedesk(root)
    root.mainloop()

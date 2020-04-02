# _*_coding=utf-8 _*_
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from matplotlib.pylab import mpl

mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.sans-serif'] = ['SimHei']


# 读取文件
def file_reader(pa):
    file = open(pa, 'r', encoding='utf-8')
    words = file.read()
    file.close()
    return words


# 读取停用词表
def stopwords_input(pa):
    a = file_reader(pa)
    stop_words = a.split('\n')[1:-2]
    return stop_words


# 显示文本内容
def text_view(a):
    text_viewer.config(state=NORMAL)
    text_viewer.delete(1.0, END)
    text_viewer.insert(END, a)
    text_viewer.config(state=DISABLED)


# 主窗体
top = Tk()
top.title('文本编辑器')
top.geometry('1200x700')
top.resizable(0, 0)  # 不可改变窗体大小

# 输入区
entry_frame = Frame(top, borderwidth=2, relief=GROOVE, padx=20, pady=20)
path1 = StringVar()
path2 = StringVar()
datapath_label = Label(entry_frame, text='文本路径          ', anchor=W)  # 文本路径标签
datapath_entry = Entry(entry_frame, textvariable=path1, width=33)  # 文本路径输入框
path1.set(r'C:\Users\lenovo\AppData\Local\Programs\Python\Python37\文件\期末设计\Annabel Lee.txt')  # 默认文本路径
datapath_entry.xview(MOVETO, 1.0)  # 默认显示路径最右端
datapath_button = Button(entry_frame, text='选择路径', command=select_path_1)  # 通过窗口选择文本路径
stopwordspath_label = Label(entry_frame, text='停用词表路径    ', anchor=W)
stopwordspath_entry = Entry(entry_frame, textvariable=path2, width=33)
path2.set(r'C:\Users\lenovo\AppData\Local\Programs\Python\Python37\文件\期末设计\停用词表.txt')
stopwordspath_entry.xview(MOVETO, 1.0)
stopwordspath_button = Button(entry_frame, text='选择路径', command=selectpath2)
display_button = Button(entry_frame, text='开始统计', command=display)
exit_button = Button(entry_frame, text='退出程序', command=exit)
datapath_label.grid(row=0, column=0)
datapath_entry.grid(row=0, column=1)
stopwordspath_label.grid(row=1, column=0)
stopwordspath_entry.grid(row=1, column=1)
datapath_button.grid(row=0, column=3, padx=10)
stopwordspath_button.grid(row=1, column=3, padx=10)
display_button.grid(row=0, column=4)
exit_button.grid(row=1, column=4)
entry_frame.place(x=600, y=30, anchor=NW)

# 柱状图区
bar_frame = Frame(top, borderwidth=2, relief=GROOVE, pady=20)
bar_frame.place(x=300, y=30, anchor=N)

# 表格区
excel_frame = Frame(top, borderwidth=2, relief=GROOVE, padx=35, pady=20)
excel_frame.place(x=300, y=650, anchor=S)

# 文本预览区
text_frame = Frame(top, borderwidth=2, relief=GROOVE, padx=20, pady=20)
text_viewer = Text(text_frame, width=65, height=30)
text_label = Label(text_frame, text='文本预览\n', font=10)
text_viewer.insert(END, '欢迎使用文本编辑器 0.0.8')
tv_scr = Scrollbar(text_frame, orient=VERTICAL)
tv_scr.config(command=text_viewer.yview)
text_viewer.config(yscrollcommand=tv_scr.set)
text_label.grid(row=0, column=0, columnspan=2)
text_viewer.grid(row=1, column=0)
tv_scr.grid(row=1, column=1, sticky=NS)
text_frame.place(x=600, y=650, anchor=SW)

# 状态栏
statusbar = Frame(top, borderwidth=2, relief=GROOVE)
total_num = Label(statusbar, anchor=E)
total_num.config(text='单词总数量：？？ ')
total_num.pack(side=RIGHT)
text_num = Label(statusbar, anchor=E)
text_num.config(text='文本长度：？？ ')
text_num.pack(side=RIGHT)
statusbar.place(relx=0.5, rely=1, relwidth=1.0, anchor=S)

top.mainloop()
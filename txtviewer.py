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


# 去除标点符号，统一为小写
def cleaner(words):
    str1 = ''
    for letter in words:
        if (65 <= ord(letter) <= 90) or (97 <= ord(letter) <= 122):
            str1 += letter.lower()
        else:
            str1 += ' '
    global word_list
    word_list = str1.split()
    # 状态栏输出文本长度
    text_num.config(text='文本长度：%s ' % len(word_list))


# 词数、词频统计
def word_statistics():
    word_set = set(word_list)
    global word_dict
    word_dict = {}
    for item in word_set:
        word_dict[item] = word_list.count(item)
    # 状态栏输出总词数
    total_num.config(text='单词总数量：%s' % len(word_dict))
    return word_dict


# 用表格输出词频
def treeview(wd):
    global wordcount
    global tf_label
    # 尝试清空旧表格
    try:
        tf_label.destroy()
        wordcount.destroy()
    except:
        pass
    tf_label = Label(excel_frame, text='词频统计', font=10)
    wordcount = ttk.Treeview(excel_frame, show="headings")
    wordcount['columns'] = ('单词', '频数')
    wordcount.column('单词', width=180)
    wordcount.column('频数', width=180)
    wordcount.heading("单词", text="单词")
    wordcount.heading("频数", text="频数")
    wc_scr = Scrollbar(excel_frame, orient=VERTICAL)
    wc_scr.config(command=wordcount.yview)
    wordcount.config(yscrollcommand=wc_scr.set)
    j = 0
    for i in wd:
        wordcount.insert("", j, values=(i, wd[i]))
        j += 1
    tf_label.grid(row=0, column=0, columnspan=2)
    wordcount.grid(row=1, column=0)
    wc_scr.grid(row=1, column=1, sticky=NS)


# 关键词输出
def keywords_op(word_dict, stop_words):
    global c
    global d
    # 进行停用词的停用
    word_dict_copy = word_dict.copy()
    for key in word_dict:
        if key in stop_words:
            del word_dict_copy[key]
    # 筛选关键词
    word = list(word_dict_copy.keys())
    count = list(word_dict_copy.values())
    c = []
    d = []
    for j in range(6):
        m = max(count)
        ind = count.index(m)
        a = word.pop(ind)
        b = count.pop(ind)
        c += [a]
        d += [b]
    c = c[::-1]
    d = d[::-1]
    return c, d


# 输出子图
def bar_drawer(c, d):
    global f
    # 先尝试清空旧图像
    try:
        plt.cla()
    finally:
        pass
    # 绘制柱状图
    f = plt.figure(num=2, figsize=(4.5, 2.5), frameon=True)
    fig = plt.subplot(1, 1, 1)
    fig.barh(c, d)
    plt.yticks(fontsize=6.5)
    fig.grid()


# 输出画布
def picture_show():
    global ca
    global ca_label
    # 先尝试清空旧画布
    try:
        ca_label.destroy()
        ca._tkcanvas.destroy()
    except:
        pass
    # 在画布上显示柱状图
    ca_label = Label(bar_frame, text='关键词统计图', font=10)
    ca = FigureCanvasTkAgg(f, bar_frame)
    ca.draw()
    ca_label.pack()
    ca._tkcanvas.pack()



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
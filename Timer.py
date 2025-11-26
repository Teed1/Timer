import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from datetime import datetime

now = datetime.now()

def start_action():
    total_seconds = 0

    #  видаляє букви h, m, s, .replace("h", "") — видаляє всі символи "h" з рядка.
    #  розбиває рядок на числа, line.split(": ") → розбиває рядок за роздільником ": " "1: 23: 45".split(": ")  # ['1', '23', '45']
    #  зберігає їх у змінні h, m, s. map(int, [...]) → перетворює всі елементи списку в цілі числа map(int, ['1', '23', '45'])  # дає [1, 23, 45]
    with open("timer_python.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.replace("h", "").replace("m", "").replace("s", "")
            h, m, s = map(int, line.split(": "))
            total_seconds += h * 3600 + m * 60 + s

    # переводимо в чч:мм:сс
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    text = f"{hours:02}:{minutes:02}:{seconds:02}"

    tk.Label(win, text=text,
             font=('Arial', 15), bg='#8fc0eb'
             ).grid(row=5, column=2, sticky='wens')


win_01: Tk = tk.Tk()
win_01.title('Timer')
win_01.geometry('300x292+1100+600')
win_01.resizable(0, 0)


style = ttk.Style()
style.theme_use("default")  # можна пробувати "clam", "alt", "vista"

# Налаштовуємо стиль для вкладок
# колір коли кнопка не активна
style.configure("TNotebook.Tab",
                background="#58E3E8",  # фон вкладки
                foreground="black")  # колір тексту
# колір коли кнопка активна
style.map("TNotebook.Tab",
          background=[("selected", "#00BFFF")],  # активна вкладка
          foreground=[("selected", "white")])  # текст активної вкладки

# создаём Notebook
notebook = ttk.Notebook(win_01)
# notebook.pack(fill='both', expand=True)
notebook.grid()

# создаём фреймы для вкладок
win = tk.Frame(notebook, bg='lightblue')
win2 = tk.Frame(notebook, bg='lightgreen')

# добавляем вкладки в Notebook
notebook.add(win, text="    Timer    ")
notebook.add(win2, text="  Відрізки  ")

scrollbar = tk.Scrollbar(win2)
listbox = tk.Listbox(win2, yscrollcommand=scrollbar.set,
                     font=('Arial', 12))  ### связывает вертикальный скроллбар со списком.

scrollbar.config(command=listbox.yview)  ### Настройте Scrollbar так, чтобы он управлял Listbox:
### command=listbox.yview указывает скроллбару, какой метод вызывать при перемещении его ползунка, чтобы прокрутить Listbox.

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Размещаем скроллбар справа, заполняя вертикально
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Размещаем список слева, заполняя все доступное пространство
# expand заповнює все або частину
try:
    with open("timer_date_python.txt", "r", encoding="utf-8") as items:
        for item in items:
            listbox.insert(tk.END, item)  ### позволяет добавить элемент в список на указанную позицию
except FileNotFoundError:
    with open("timer_date_python.txt", "w", encoding="utf-8") as items:
        items.write("")

value_s = 0
value_m = 0
value_h = 0

# Змінна для тексту
time_s = tk.StringVar()
time_m = tk.StringVar()
time_h = tk.StringVar()
time_s.set("00")
time_m.set(": 00 :")
time_h.set("00")


def up_time():
    global value_s, value_m
    value_s += 1

    if value_s == 60:
        global value_m
        value_m += 1
        time_m.set(f": {value_m:02} :")
        value_s = 0

    if value_m == 60:
        global value_h
        value_h += 1
        time_h.set(f"{value_h:02}")
        value_m = 0
        time_m.set(f": {value_m:02} :")

    time_s.set(f"{value_s:02}")  # оновлюємо текст у Label

    global job_id  ### остановка таймера
    job_id = win.after(1000, up_time)  # снова вызвать через 1 сек
    btn.config(state="disabled")  # выключаем кнопку после первого клика


def stop_time():
    win.after_cancel(job_id)  ### остановка таймера
    btn.config(state="normal")


def clear_time():
    global value_s, value_m, value_h
    value_s = 0
    value_m = 0
    value_h = 0
    time_s.set('00')
    time_m.set("00")
    time_h.set("00")

    btn3.config(state="normal")


def record_time():
    global value_s, value_m, value_h
    with open('timer_python.txt', 'a', encoding='utf-8') as f:
        f.write(f"{value_h}h : {value_m}m : {value_s}s \n")
    with open('timer_date_python.txt', 'a', encoding='utf-8') as fin:
        fin.write(f"{now.strftime(" %d.%m.%Y     %H:%M:%S")}     {value_h}h : {value_m}m : {value_s}s \n")

    btn3.config(state="disabled")  # выключаем кнопку после первого клика
    start_action()  # відновлюемо загальний час


hours = tk.Label(win, text="годин", bg='lightblue')
minutes = tk.Label(win, text="хвилин", bg='lightblue')
seconds = tk.Label(win, text="секунд", bg='lightblue')

hours.grid(row=0, column=0, sticky='es')
minutes.grid(row=0, column=1, sticky='s')
seconds.grid(row=0, column=2, sticky='ws')

label_h = tk.Label(win, textvariable=time_h,
                   font=('Arial', 25, 'bold'), bg='lightblue'
                   )
label_m = tk.Label(win, textvariable=time_m,
                   font=('Arial', 25, 'bold'), bg='lightblue'
                   )
label_s = tk.Label(win, textvariable=time_s,
                   font=('Arial', 25, 'bold'), bg='lightblue'
                   )

label_h.grid(row=1, column=0, sticky='ne')
label_m.grid(row=1, column=1, sticky='n')
label_s.grid(row=1, column=2, sticky='wn')

btn = tk.Button(win, text="Start", command=up_time, bg='#8fc0eb')
btn1 = tk.Button(win, text="Stop", command=stop_time, bg='#8fc0eb')
btn2 = tk.Button(win, text="Clear", command=clear_time, bg='#8fc0eb')
btn3 = tk.Button(win, text="Record", command=record_time, bg='#8fc0eb')

btn.grid(row=2, column=0, sticky='wens')
btn1.grid(row=3, column=0, sticky='wens')
btn2.grid(row=4, column=0, sticky='wens')
btn3.grid(row=5, column=0, sticky='wens')

win.grid_columnconfigure(0, minsize=100)
win.grid_columnconfigure(1, minsize=100)
win.grid_columnconfigure(2, minsize=100)

win.grid_rowconfigure(0, minsize=60)
win.grid_rowconfigure(1, minsize=80)
win.grid_rowconfigure(2, minsize=40)
win.grid_rowconfigure(3, minsize=30)
win.grid_rowconfigure(4, minsize=30)
win.grid_rowconfigure(5, minsize=30)

win.after(0, start_action)  ### Вызов функции сразу после запуска окна
win.mainloop()
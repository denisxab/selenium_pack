"""
Модуль для Tkinter который будет управлять драйвером браузера

"""


import tkinter as tk


def btn_click():
    entered_text = text_entry.get()
    print(entered_text)


root = tk.Tk()
root.title("Tkinter App")

text_entry = tk.Entry(root)
text_entry.pack()

button1 = tk.Button(root, text="Button 1", command=btn_click)
button1.pack()

button2 = tk.Button(root, text="Button 2", command=btn_click)
button2.pack()

root.mainloop()

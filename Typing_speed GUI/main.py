from tkinter import *
import requests
import math

COUNT = 60
timer = None
time = 0
words = []

window = Tk()
window.title("Typing Speed Test")
window.config(pady=50, padx=40, bg='#6B728E')

main_label = Label(text="Test Your Typing Speed", bg='#6B728E', fg='#404258', font='Times 50 bold')
main_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=182)
type_img = PhotoImage(file="personal-computer-girl-typing.png")
canvas.create_image(100, 91, image=type_img)
canvas.grid(row=0, column=0)


def quotation():
    global words
    response = requests.get(url="https://api.kanye.rest")
    response.raise_for_status()
    quote = response.json()["quote"]
    words = list(quote.split())
    if len(words) > 30:
        quotation()
    else:
        return quote


def start_timer():
    global time
    global timer
    count_min = math.floor(time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = time % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_sec == 0:
        count_sec = "00"
    timer_text.config(text=f"{count_min}:{count_sec}")
    timer = window.after(1000, func=start_timer)
    time += 1


def stop_timer(event):
    global timer
    window.after_cancel(timer)


def reset_timer():
    global words, time
    correct_words = 0
    timer_text.config(text="00:00")
    typed_text = list(text_entry.get().split())
    for i in range(len(typed_text)):
        if typed_text[i] == words[i]:
            correct_words += 1
    speed = round(correct_words / 5 / (time / 60))
    acc = round(correct_words / len(words) * 100, 2)
    wpm_label = Label(text=f"Your typing speed: {speed} WPS(words per second)", bg='#6B728E', fg='#F5D5AE', font='arial 17')
    wpm_label.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
    acc_label = Label(text=f"Your typing accuracy: {acc}%", bg='#6B728E', fg='#F5D5AE', font='arial 17')
    acc_label.grid(row=6, column=0, padx=10, pady=10, columnspan=2)
    text_entry.delete(0, END)
    text_label.config(text=quotation())


text_label = Label(text=quotation(), bg='#6B728E', fg='#F0EBCE', font='arial 17')
text_label.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

start_button = Button(text="Start", bg='#F7A4A4', font='arial 20 bold', bd=3, fg='#404258', command=start_timer)
start_button.grid(row=2, column=0, padx=20, pady=20)

timer_text = Label(text="00:00", bg='#F7A4A4', font='arial 20 bold', fg='#404258')
timer_text.grid(row=2, column=1, padx=20, pady=20)

text_entry = Entry(width=100, bg='#FFFAD7', fg='#474E68', font="arial 16")
text_entry.focus()
text_entry.bind('<Return>', stop_timer)
text_entry.grid(row=3, column=0, padx=20, pady=20, columnspan=2, ipady=7)

reset_button = Button(text="Reset", bg='#F7A4A4', font='arial 20 bold', bd=3, fg='#404258', command=reset_timer)
reset_button.grid(row=4, column=0, padx=20, pady=20, columnspan=2)
window.mainloop()

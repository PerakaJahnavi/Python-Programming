from tkinter import *
from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog
from turtle import Screen
from functools import partial

window = Tk()


window.title("Image Watermarking Desktop App")
window.config(padx=70, pady=50, bg='#F8C4B4')

# Main Heading
main_label = Label(text="Add Watermark To Your Image", font="times 30 bold", bg='#F8C4B4', fg='#0E5E6F')
main_label.grid(row=0, column=0, ipady=20)


def add_watermark(filename, wf_entry):
    opened_image = Image.open(filename)
    image_width, image_height = opened_image.size
    draw = ImageDraw.Draw(opened_image)
    font_size = int(image_width / 25)
    font = ImageFont.truetype('arial.ttf', font_size)
    x, y = int(image_width / 2), int(image_height / 2)
    draw.text((x, y), wf_entry.get(), font=font, fill='#fff', stroke_width=1, anchor='ms')
    opened_image.show()


def select_file():
    filename = filedialog.askopenfilename(initialdir="C:/Users/jahna/OneDrive/Pictures/Saved Pictures", title='Select an Image: ')
    wf_label = Label(text="Enter Your watermark text", font="times 17 italic bold", bg='#F8C4B4', fg='#497174')
    wf_label.grid(row=3, column=0, ipady=20)

    wf_entry = Entry(width=28, bg='#E6CBA8')
    wf_entry.focus()
    wf_entry.grid(row=4, column=0, ipady=10)

    ok_button = Button(text="Ok", bg='#DEF5E5', bd=0, command=partial(add_watermark, filename, wf_entry))
    ok_button.grid(row=4, column=1)


select_label = Label(text="Select Your Image", font="times 20 italic bold", bg='#F8C4B4', fg='#393E46')
select_label.grid(row=1, column=0, ipady=20)

img = PhotoImage(file="select-modified.png")
selection_button = Button(image=img, bg='#F8C4B4', bd=0, command=select_file)
selection_button.grid(row=2, column=0, ipady=20)


window.mainloop()
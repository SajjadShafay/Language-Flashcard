import tkinter
import pandas
import random
from tkinter import messagebox
import sys
import os

# --------------- CONSTANTS ---------------
BACKGROUND_COLOR = "#B1DDC6"
word = ""

# --------------- READING CSV -------------
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/japanese_words.csv")
except pandas.errors.EmptyDataError:
    tkinter.messagebox.showinfo(title='Error', message="Word list is empty")
    os.remove('data/words_to_learn.csv')
    sys.exit()
finally:
    data = data.to_dict(orient='records')


# --------- NEW WORD FUNCTION -------------
def new_word():
    global word, timer
    window.after_cancel(timer)
    try:
        word = random.choice(data)
    except IndexError:
        tkinter.messagebox.showinfo(title='Error', message="Word list is empty")
    canvas.itemconfig(canvas_image, image=flashcard_front)
    canvas.itemconfig(language_title, text='Japanese', fill='black')
    canvas.itemconfig(word_text, text=f'{word['Japanese']}', fill='black')
    timer = window.after(3000, flip_card)


# ----------- CHECKMARK WORD --------------
def checkmark_word():
    global word
    data.remove(word)
    dataframe = pandas.DataFrame(data)
    dataframe.to_csv('data/words_to_learn.csv', index=False)
    new_word()


# -------------- CARD FLIP ----------------
def flip_card():
    global word
    canvas.itemconfig(canvas_image, image=flashcard_back)
    canvas.itemconfig(language_title, text='English', fill='white')
    canvas.itemconfig(word_text, text=f'{word['English']}', fill='white')


# -------------- UI SETUP -----------------
window = tkinter.Tk()
window.title("Language Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

word = random.choice(data)
canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
flashcard_front = tkinter.PhotoImage(file="images/card_front.png")
flashcard_back = tkinter.PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flashcard_front)
language_title = canvas.create_text(400, 150, text='Japanese', font=('Arial', 40, 'italic'))
word_text = canvas.create_text(400, 263, text=f'{word['Japanese']}', font=('Arial', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

cross_img = tkinter.PhotoImage(file="images/wrong.png")
cross_button = tkinter.Button(image=cross_img, highlightthickness=0, bd=0, command=new_word)
cross_button.grid(column=0, row=1)
checkmark_img = tkinter.PhotoImage(file="images/right.png")
checkmark_button = tkinter.Button(image=checkmark_img, highlightthickness=0, bd=0, command=checkmark_word)
checkmark_button.grid(column=1, row=1)

timer = window.after(3000, flip_card)

window.mainloop()

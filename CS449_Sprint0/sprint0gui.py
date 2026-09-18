from tkinter import *

window = Tk()

def click():
    print("Game Started!")

def display():
    if autoplay.get() == 1:
        print("Autoplay Enabled")
    else:
        print("Autoplay Disabled")

def select_difficulty():
    if x.get() == 1:
        print("Easy selected")
    elif x.get() == 2:
        print("Medium selected")
    elif x.get() == 3:
        print("Hard selected")

window.geometry("800x400")
window.title("Sprint 0 GUI")
window.config(background="#5cfcff")


label = Label(window, text="Peg Solitaire", font=("Arial", 24, 'bold'), fg='white', bg="green", relief=RAISED, bd=5, padx=10, pady=10)
label.pack(pady=20)

canvas = Canvas(
    window,
    width=700,
    height=2,
    bg="black",
    highlightthickness=0
)

canvas.pack(pady=10)

left_frame = Frame(window, bg="#5cfcff") 
right_frame = Frame(window, bg="#5cfcff") 
left_frame.pack(side=LEFT, expand=True) 
right_frame.pack(side=RIGHT, expand=True)


button = Button(left_frame, text="Start Game", font=("Arial", 16), fg='white', bg="green", relief=RAISED, bd=5, padx=10, pady=10)
button.config(command=click)
button.pack(pady=20)

autoplay = IntVar()
checkbox = Checkbutton(left_frame, text="Enable Autoplay", variable=autoplay, onvalue=1, offvalue=0, command=display, font=("Arial", 14), fg='white', bg="green", relief=RAISED, bd=5, padx=10, pady=10)
checkbox.pack(pady=20)

x = IntVar()
options = ["easy", "medium", "hard"]
for index in range(len(options)):
    radiobutton = Radiobutton(right_frame, text=options[index].capitalize(), variable=x, value=index+1, command=select_difficulty, font=("Arial", 14), fg='white', bg="green", relief=RAISED, bd=5, padx=10, pady=10)
    radiobutton.pack(pady=20)


window.mainloop()

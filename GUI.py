from tkinter import *
import tkinter.filedialog as fd

fpath=[]

def browseFiles():
    global fpath
    filename = fd.askopenfilenames(title='Choose a file')
    fpath=list(filename)
    window.destroy()

window = Tk()

window.title('File Explorer')

window.geometry("500x500")

window.config(background="grey")

label_file_explorer = Label(window,text="File Explorer using Tkinter",width=71, height=4,fg="blue")

button_explore = Button(window,text="Browse Files",command=browseFiles)

button_exit = Button(window,text="Exit",command=exit)

label_file_explorer.grid(column=1, row=1)

button_explore.grid(column=1, row=2)

button_exit.grid(column=1, row=3)

window.mainloop()

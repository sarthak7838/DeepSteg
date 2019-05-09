from tkinter import *
root = Tk()

def browsefunc():
    filename = filedialog.askopenfilename()
    pathlabel.config(text=filename)

browsebutton = Button(root, text="Browse", command=browsefunc)
browsebutton.pack()

pathlabel = Label(root)
pathlabel.pack()
root.mainloop()
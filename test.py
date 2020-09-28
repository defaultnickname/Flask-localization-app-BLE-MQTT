import tkinter as tk
from tkinter import filedialog


class Root(tk.Tk):
    """Creates root window."""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("the map poczatekxd")
        #self.geometry("%dx%d+0+0" % self.maxsize())
        #uncomment later


class MenuBar(tk.Frame):

    def OpenImage(self):
        self.root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("png files", "*.png"), ("all files", "*.*")))
        Canvas.Image(self.root, filename=self.root.filename)

    def CreateRectangle(self):
        Canvas.CreateRectangle(self.root)
        pass
    def donothing(self):
        pass

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Image", command=self.OpenImage)
        filemenu.add_command(label="Add rectangle", command=self.CreateRectangle)
        filemenu.add_command(label="Close", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        menubar.add_cascade(label="File", menu=filemenu)


        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)


        menubar.add_cascade(label="Edit", menu=editmenu)


        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)


class Canvas(tk.Canvas):
    """Creates drawing canvas."""

    def __init__(self, root, *args, **kwargs):
        tk.Canvas.__init__(self, root, *args, **kwargs)

        self.pack(fill="both", expand=True)


    def Image(self, filename):
        global img
        img = tk.PhotoImage(file=filename)

        canvas.create_image(0, 0, anchor=tk.NW, image=img)

    def CreateRectangle(self,x=10,y=10):
        canvas.create_rectangle(10,15,15,10, fill = 'red')


root = Root()
app = MenuBar(root)
canvas = Canvas(root)
root.mainloop()

#TO DO
#   Skalowanie zdjęcia razem z oknem
#   Przybliżanie i oddalanie zdjęcia
#   Przesuwanie kwadratów
#   Linijka żeby dobrze je odjebać
#   pomyśleć jak zrobić skalę ( może być związana z linijką w sumie)
#
#
#
#
#
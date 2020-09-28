"""This program demonstrates object-oriented Python GUI using tkinter.

Input:
    None

Output:
    Window canvas

Global variables:
    root (tkinter.root): top-level window
    canvas (tkinter.canvas): canvas

References:
    https://www.tutorialspoint.com/python/python_gui_programming.htm
    https://www.python-course.eu/python_tkinter.php
    https://stackoverflow.com/questions/22785949/subclassing-with-tkinter-in-python
    http://effbot.org/tkinterbook/canvas.htm
    http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
"""

# requires tkinter 8.6 or higher
import tkinter
import urllib.request

# Requires pip install Pillow
import PIL.Image
import PIL.ImageTk

# Bypass certificate verification
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Root(tkinter.Tk):
    """Creates root window."""

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title("tkinter Canvas Example")
        self.geometry("%dx%d+0+0" % self.maxsize())


class MainMenu(tkinter.Menu):
    """Creates Main menu."""

    def __init__(self, root, *args, **kwargs):
        tkinter.Menu.__init__(self, root, *args, **kwargs)

        file_menu = FileMenu(self, tearoff=0)
        self.add_cascade(label="File", menu=file_menu)

        root.config(menu = self)


class FileMenu(tkinter.Menu):
    """Creates File menu."""

    def __init__(self, root, *args, **kwargs):
        tkinter.Menu.__init__(self, root, *args, **kwargs)

        self.add_command(label="Exit", command=root.quit)


class Canvas(tkinter.Canvas):
    """Creates drawing canvas."""

    images = []

    def __init__(self, root, *args, **kwargs):
        tkinter.Canvas.__init__(self, root, *args, **kwargs)

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

        self.pack(fill="both", expand=True)

        self.create_text(450, 50, font=("Purisa", 24), text="tkinter Canvas Drawing Examples")

        self.create_line(175, 150, 275, 150, width=3, fill='darkred')
        self.create_rectangle(325, 100, 425, 200, outline='gold', fill='gold')
        self.create_oval(475, 100, 575, 200, outline='darkgreen', fill='darkgreen')
        self.create_polygon(675, 100, 625, 200, 725, 200, outline='darkblue', fill='darkblue')

        self.create_text(450, 510, font=("Purisa", 24), text="drag mouse to draw")

    def add_image(self, url, x, y, tags=None):
        """Adds image from URL to canvas at coordinates(x, y)."""
        response = urllib.request.urlopen(url)
        image = PIL.Image.open(response)
        photoimage = PIL.ImageTk.PhotoImage(image)
        canvas.create_image(x, y, anchor=tkinter.NW, image=photoimage, tags=tags)
        self.images.append(photoimage)

    def on_click(self, event):
        self.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, outline='black', fill='black')

    def on_drag(self, event):
        self.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, outline='black', fill='black')


if __name__ == "__main__":
    root = Root()
    menu = MainMenu(root)
    canvas = Canvas(root)



    root.mainloop()
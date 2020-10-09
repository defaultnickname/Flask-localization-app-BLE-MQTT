import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinter import ttk
import Target
import MQTT_READ
import threading
import sys

def idxfor3smallest(list):
    lcopy = list.copy()
    tmp = []

    for _ in range(3):
        i_i = lcopy.index(min(lcopy))
        tmp.append(i_i)
        lcopy[i_i] = sys.maxsize

    return [x+1 for x in tmp]


class Root(tk.Tk):
    """Creates root window."""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("the map poczatekxd")


        #self.geometry("%dx%d+0+0" % self.maxsize())
        #uncomment later


class MenuBar(tk.Frame):



    def OpenImage(self):

        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("png files", "*.png"), ("all files", "*.*")))
        icanvas.show_image(root.filename)

    def CreateRectangle(self):
        icanvas.my_create_rectangle(10,10)

    def go(self,*args,**kwargs):
        #threading.Timer(2.0, self.go).start()
        icanvas.canvas.delete("target")
        icanvas.canvas.delete('circ')

        TheTarget.distanceTab = []
        for i in range(1,8):
            topic = "test/" + str(TheTarget.targetID) + "/" + str(i)
            print(topic)
            v=con.read(topic)

            print(v.msg)

            TheTarget.distanceTab.append(float(v.msg))

            con.msg.msg = sys.maxsize

        print(TheTarget.distanceTab)

        #TheTarget.distanceTab=[250,250,250]
        #Targ.distanceTab=[150,200,250]

        l = idxfor3smallest(TheTarget.distanceTab)
        print(l)
        TheTarget.Update(l)
        #Targ.Update((1,2,3))
        icanvas.cr_circle(Target.Beacon.FindWithID(l[0]).x ,Target.Beacon.FindWithID(l[0]).y,TheTarget.distanceTab[l[0]-1])
        icanvas.cr_circle(Target.Beacon.FindWithID(l[1]).x, Target.Beacon.FindWithID(l[1]).y,TheTarget.distanceTab[l[1]-1])
        icanvas.cr_circle(Target.Beacon.FindWithID(l[2]).x, Target.Beacon.FindWithID(l[2]).y,TheTarget.distanceTab[l[2]-1])
        icanvas.create_target(TheTarget.x,TheTarget.y)
        #icanvas.create_target(Targ.x , Targ.y)

    def donothing(self):
        pass

    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.frame = tk.Frame(self.root)
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Image", command=self.OpenImage)
        filemenu.add_command(label="Add rectangle", command=self.CreateRectangle)
        filemenu.add_command(label="Close", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        menubar.add_cascade(label="File", menu=filemenu)


        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Go", command=self.go)
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
class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):

        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)


    def pack(self, **kw):

        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):

        raise tk.TclError('Cannot use place with this widget')

class Canvas(tk.Frame):
    """Creates drawing canvas."""
    relationtable=[]

    def __init__(self, root, *args, **kwargs):

        self.root = root
        self.frame = tk.Frame(self.root)
        vbar = AutoScrollbar(self.root, orient='vertical')
        hbar = AutoScrollbar(self.root, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')

        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.root, highlightthickness=2,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self._drag_data = {"x": 0, "y": 0, "item": None}



        self.canvas.grid(row=0, column=0, sticky='nswe')
        vbar.configure(command=self.canvas.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.canvas.xview)
        # Make the canvas expandable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # Bind events to the Canvas

        self.canvas.tag_bind("rec", "<ButtonPress-2>", self.drag_start)
        self.canvas.tag_bind("rec", "<ButtonRelease-2>", self.drag_stop)
        self.canvas.tag_bind("rec", "<B2-Motion>", self.drag)

        self.canvas.tag_bind("rec", "<ButtonPress-3>", self.drag_start)
        self.canvas.tag_bind("rec", "<ButtonRelease-3>", self.drag_stop)
        self.canvas.tag_bind("rec", "<B3-Motion>", self.drag)

        #self.canvas.bind('<ButtonPress-1>', self.move_from)
        #self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind('<MouseWheel>', imenu.go)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>', self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>', self.wheel)  # only with Linux, wheel scroll up

        self.imscale = 1.0
        self.imageid = None
        self.delta = 0.75
        self.text = self.canvas.create_text(0, 0, anchor='nw', text='')
        self.show_image(r'C:\Users\Majkster\PycharmProjects\KinterTESTING\biuro.png')
        width, height = self.image.size

        self.canvas.configure(scrollregion=self.canvas.bbox('all'))



    def show_image(self,path=None):

        if path==None:
            path = root.filename
        else:
            root.filename = path

        self.canvas.delete(self.imageid)
        self.imageid = None
        self.canvas.imagetk = None  # delete previous image from the canvas

        self.image = Image.open(path)

        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(self.canvas.coords(self.text),
                                                anchor='nw',state=tk.DISABLED, image=imagetk,tag='img')


        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
        self.bumpRectangles()



    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)


    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)



    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            scale *= self.delta
            self.imscale *= self.delta
        if event.num == 4 or event.delta == 120:
            scale /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))



    def drag_start(self, event):

        self._drag_data["item"] = self.canvas.find_enclosed(event.x-10 ,event.y-10,event.x+10,event.y+10)

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y





    def drag_stop(self, event):


        index = [x for x, y in enumerate(Canvas.relationtable) if y[0] == self._drag_data["item"][0]]


        Rec_to_update = Canvas.relationtable[index[0]][1]

        Rec_to_update.x = self._drag_data["x"]
        Rec_to_update.y = self._drag_data["y"]

        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

       # print(Rec_to_update,Canvas.relationtable[index[0]][0] )





    def drag(self, event):

        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        #print(self._drag_data)

        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y


    def my_create_rectangle(self, x , y):
        rec = self.canvas.create_rectangle(x * self.imscale, y * self.imscale, (x+5) * self.imscale, (y+5) *self.imscale,fill='red',activefill='black', tags='rec')
        x = (x * self.imscale + (x+5) * self.imscale) / 2
        y = (y * self.imscale + (y+5) * self.imscale) / 2

        anchor = Target.Beacon(x, y)
        Canvas.relationtable.append((rec,anchor))

    def create_target(self,x,y):
        tar = self.canvas.create_rectangle(x * self.imscale, y * self.imscale, (x + 5) * self.imscale,
                                           (y + 5) * self.imscale, fill='blue', activefill='black', tags='target')

    def cr_circle(self, x, y, r, **kwargs):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs,tag ='circ')



    def bumpRectangles(self):
        print("Bump")
        map(lambda x: self.canvas.lift(x), self.canvas.find_withtag('rec'))


root = Root()
imenu = MenuBar(root)
icanvas = Canvas(root)
con = MQTT_READ.MQTT(broker_address='127.0.0.1', clientname='P1')


TheTarget = Target.Tar(1)
Targ= Target.Tar(2)
root.mainloop()



#TO DO


#   Przesuwanie kwadratów  (bind manager w menubar -> unbind przesuwanie, bind przesuwanie kwadrat
#   Linijka żeby dobrze je odjebać
#   pomyśleć jak zrobić skalę ( może być związana z linijką w sumie)
#
#
#
#
#
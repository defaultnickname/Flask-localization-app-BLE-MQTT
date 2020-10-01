import tkinter as tk

def left_click(event):
    event.widget.configure(bg="green")

def right_click(event):
    event.widget.configure(bg="red")
    print(event.widget.par)

root = tk.Tk()
button = tk.Frame(root, width=20, height=20, background="gray")
button.pack(padx=0, pady=0)

button.bind("<Button-1>", left_click)
#button.bind("<ButtonPress-2>", right_click)
button.bind("<ButtonPress-3>", right_click)

root.mainloop()
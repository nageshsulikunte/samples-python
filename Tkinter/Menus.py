from Tkinter import *
 
from Tkinter import Menu
 
window = Tk()
 
window.title("Welcome to DRTTIT Seminar")
 
menu = Menu(window)
 
new_item = Menu(menu)
 
new_item.add_command(label='New')
 
new_item.add_separator()
 
new_item.add_command(label='Edit')
 
menu.add_cascade(label='File', menu=new_item)
 
window.config(menu=menu)
 
window.mainloop()


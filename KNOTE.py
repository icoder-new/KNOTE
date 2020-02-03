from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd

def help_():
	mb.showinfo('KNOTE 0.2',
		'KNOTE v0.2\nAuthor: Ilyosiddin Kalandar & Ehsonjon Gadoev\nilyosiddin_kalandar@mail.ru & priler05@gmail.com')
def find_bug():
	mb.showinfo('BUG REPORT','Hello,if you find bug please create issue on github\ngithub.com\ikalandar\KNOTE')

def open_file(event = None):
	global FILENAME
	FILENAME = fd.askopenfilename()
	root.title('KNOTE v0.2 - '+ FILENAME)
	f = open(FILENAME,'r')
	text.delete('1.0',END)
	text.insert(INSERT,f.read())

def save_file(event = None):
	global FILENAME
	if FILENAME:
		f = open(FILENAME,'w')
		f.write(text.get('1.0',END))
	else:
		extractText()

def extractText(event = None):
	global FILENAME
	FILENAME = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),('HTML file', '*.html'),("All files", "*.*") ))
	root.title('KNOTE v0.2 - ' + FILENAME)
	f = open(FILENAME,'w')
	f.write(text.get('1.0',END))
def exit(event = None):
	root.destroy()

def find_text(event = None):
	pass

FILENAME = ''
root = Tk()
root.title('KNOTE v0.2')
root.resizable(False,False)
text = Text(root)#width=100,height=30
text.pack()
global_menu = Menu(root)
root.config(menu=global_menu)
file_menu = Menu(global_menu, tearoff=0)
help_menu = Menu(global_menu, tearoff=0)
edit_menu = Menu(global_menu, tearoff=0)

file_menu.add_command(label='Open file',accelerator = 'Ctrl+O',command=open_file)
file_menu.add_command(label='Save file',accelerator = 'Ctrl+S',command=save_file)
file_menu.add_command(label='Save as',accelerator = 'Ctrl+Shift+S',command=extractText)
file_menu.add_command(label='Exit',accelerator = 'Alt+F4',command=exit)

def undo():
    text.event_generate("<<Undo>>")
    return "break"

def redo():
    text.event_generate("<<Redo>>")
    return 'break'

def cut():
    text.event_generate("<<Cut>>")
    return "break"

def copy():
    text.event_generate("<<Copy>>")
    return "break"

def paste():
    text.event_generate("<<Paste>>")
    return "break"

def find_callback():
	pass

def select_all_callback():
    pass

edit_menu.add_command(label="Undo", accelerator='Ctrl + Z', command=undo)
edit_menu.add_command(label="Redo", accelerator='Ctrl + Y', command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator='Ctrl + X', command=cut)
edit_menu.add_command(label="Copy", accelerator='Ctrl + C',  command=copy)
edit_menu.add_command(label="Paste", accelerator='Ctrl + V', command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Find", accelerator='Ctrl + F', command=find_callback)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", accelerator='Ctrl + A', command=select_all_callback)

help_menu.add_command(label='About program',command=help_)
help_menu.add_command(label='I find bug!',command=find_bug)

global_menu.add_cascade(label='File',menu=file_menu)
global_menu.add_cascade(label='Help',menu=help_menu)

root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-Shift-S>", extractText)
root.bind("<Alt-F4>", exit)
root.mainloop()

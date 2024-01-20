"""

Project by Ilyosiddin Kalandar (ikalandar)
Contribute by Ehsonjon Gadoev (icoder-new)

"""

from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk

def help_():
	mb.showinfo('KNOTE 0.3',
		'KNOTE v0.3\nAuthor: Ilyosiddin Kalandar & Ehsonjon Gadoev\nilyosiddin_kalandar@mail.ru & priler05@gmail.com')
def find_bug():
	mb.showinfo('BUG REPORT','Hello,if you find bug please create issue on github\ngithub.com\ikalandar\KNOTE')

def open_file(event = None):
	try:
		global FILENAME
		FILENAME = fd.askopenfilename()
		root.title('KNOTE v0.3 - '+ FILENAME)
		f = open(FILENAME,'r')
		text.delete('1.0',END)
		text.insert(INSERT,f.read())
	except FileNotFoundError:
		pass

def save_file(event = None):
	global FILENAME
	if FILENAME:
		f = open(FILENAME,'w')
		f.write(text.get('1.0',END))
	else:
		extractText()

def extractText(event = None):
	try:
		global FILENAME
		FILENAME = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),('HTML file', '*.html'),("All files", "*.*") ))
		root.title('KNOTE v0.3 - ' + FILENAME)
		f = open(FILENAME,'w')
		f.write(text.get('1.0',END))
	except FileNotFoundError:
		pass

def exit(event = None):
	root.destroy()

def find_text(event = None):
	pass

FILENAME = ''
root = Tk()
root.title('KNOTE v0.3')
root.resizable(False, False)
#root.geometry('1200x800')
root.wm_iconbitmap('mainicon.ico')
text = Text(root)#width=100,height=30
text.focus_set()
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

color_theme = Menu(root,tearoff=False)
global_menu.add_cascade(label='Color Theme',menu=color_theme)
theme_choice = StringVar()

color_dict = {
	'Light Default' :('#000000','#ffffff'),
	'Light Plus' :('#474747','#e0e0e0'),
	'Dark' : ('#c4c4c4', '#2d2d2d'),
	'Red' : ('#2d2d2d','#ffe8e8'),
	'Monokai' : ('#d3b774','#474747'),
	'Night Blue' :('#ededed','#6b9dc2')
}

def set_theme():
	choose_theme = theme_choice.get()
	color_tuple =color_dict.get(choose_theme)
	fg_color,bg_color =color_tuple[0], color_tuple[1]
	text.config(background=bg_color,fg=fg_color)

count = 0
for i in color_dict :
	color_theme.add_radiobutton(label = i, variable=theme_choice,compound=LEFT,command =set_theme)
	count+=1

status_bar = ttk.Label(root, text ='Status Bar')
status_bar.pack(side=BOTTOM)

text_changed = False

def changed(event=None):
    global text_changed
    if text.edit_modified():###checks if any character is added or not
        text_changed= True
        words = len(text.get(1.0, 'end-1c').split()) ##it even counts new line character so end-1c subtracts one char
        characters = len(text.get(1.0,'end-1c'))
        status_bar.config(text=f' Words: {words} Characters : {characters}')
    text.edit_modified(False)
text.bind('<<Modified>>',changed)

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

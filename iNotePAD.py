from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
#what i can do>
def help_():
	mb.showinfo('iNotePAD',
		'iNotePAD v0.2\nAuthor: Ilyosiddin Kalandar & Ehsonjon Gadoev\nilyosiddin_kalandar@mail.ru & priler05@gmail.com')
def find_bug():
	mb.showinfo('BUG REPORT','Hello,if you find bug please create issue on github\ngithub.com\ikalandar\KNOTE')

def open_file(event = None):
	global FILENAME
	FILENAME = fd.askopenfilename()
	root.title('iNotePAD v0.2 - '+ FILENAME)
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
	FILENAME = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),("All files", "*.*"), ('HTML file', '*.html') ))
	root.title('iNotePAD v0.1 - ' + FILENAME)
	f = open(FILENAME,'w')
	f.write(text.get('1.0',END))
def exit(event = None):
	root.destroy()
	
FILENAME = ' '
root = Tk()
root.title('iNotePAD v0.2')
text = Text(width=100,height=30)
text.pack()

global_menu = Menu(root)
root.config(menu=global_menu)
root.resizable(False,False)
file_menu = Menu(global_menu)
help_menu = Menu(global_menu)

file_menu.add_command(label='Open file',accelerator = 'Ctrl+O',command=open_file)
file_menu.add_command(label='Save file',accelerator = 'Ctrl+S',command=save_file)
file_menu.add_command(label='Save as',accelerator = 'Crtl+Shift+S',command=extractText)
file_menu.add_command(label='Exit',accelerator = 'Alt+F4',command=exit)

help_menu.add_command(label='About program',command=help_)
help_menu.add_command(label='I find bug!',command=find_bug)

global_menu.add_cascade(label='File',menu=file_menu)
global_menu.add_cascade(label='Help',menu=help_menu)

root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-Shift-S>", extractText)
root.bind("<Alt-F4>", exit)

root.mainloop()

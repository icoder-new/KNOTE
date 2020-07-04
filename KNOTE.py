import tkinter

from tkinter import messagebox as mb
from tkinter import filedialog as fdialog
from settings import *

class TextWiget(tkinter.Text):
	'''
		A custom Text widget
	'''
	def __init__(self, *args, *args, **kwargs):
		self.__init__(args, kwargs)
	
	def save_to_file(filename):
		pass
	
	def open_file(filename):
		pass

class App:
	'''
		A main class, a class of our app
		this class generate menus, read events and more...
	'''
	def __init__(self, app):
		self.app = app # app (root)
		self.main_menu = tkinter.Menu(app) # main menu (topmenu)
		self.file_menu = tkinter.Menu(self.main_menu) # cascade menu
		self.help_menu = tkinter.Menu(self.main_menu) # cascade menu too
		
		self.FILENAME = ''

		self.file_menu.add_command(label="New file", command=None)
		self.file_menu.add_command(label="Open File", command=self.text.open_file)
		self.file_menu.add_command(label="Save As", command=None)
		self.file_menu.add_command(label="Close file", command=self.text.close_file)
		self.file_menu.add_command(label='Copy')
		self.file_menu.add_command(label='Paste')
		self.file_menu.add_command(label="Undo", command=None)
		self.file_menu.add_command(label="Redo", command=None)

		self.main_menu.add_cascade(label='File', menu=self.file_menu)
		self.main_menu.add_cascade(label='Help', menu=self.help_menu)

	def move_or_resize(self, event):
		pass

	

if __name__ == '__main__':
	root = tkinter.Tk(WINDOW_SIZE)
	app = App(root)
	root.mainloop()
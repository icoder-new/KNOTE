import os, io, sys
try:
	# Python 3
	import tkinter
	from tkinter import font, ttk, scrolledtext, _tkinter
	from tkinter import messagebox as mb
	from tkinter import filedialog as fd
except ImportError:
	# Python 2
	import Tkinter as tkinter
	from Tkinter import ttk
	import tkFont as font
	import tkMessageBox as mb
	import tkFileDialog as fd
	import ScrolledText as scrolledtext

try:
	from pygments.lexers.python import PythonLexer
	from pygments.lexers.special import TextLexer
	from pygments.lexers.html import HtmlLexer
	from pygments.lexers.html import XmlLexer
	from pygments.lexers.templates import HtmlPhpLexer
	from pygments.lexers.perl import Perl6Lexer
	from pygments.lexers.ruby import RubyLexer
	from pygments.lexers.configs import IniLexer
	from pygments.lexers.configs import ApacheConfLexer
	from pygments.lexers.shell import BashLexer
	from pygments.lexers.diff import DiffLexer
	from pygments.lexers.dotnet import CSharpLexer
	from pygments.lexers.sql import MySqlLexer

	from pygments.styles import get_style_by_name
except ModuleNotFoundError:
	print("\x1b[31mYou must to install pygments module\x1b[39m")
	if sys.platform.startswith('win'):
		print('\x1b[32mpip install pygments\x1b[39m')
	else:
		print("\x1b[32mpython3 -m pip install pygments\x1b[39m")
	sys.exit(-1)

class App:
	"""
		KNOTE Simple Free OpenSource Text Editor with highlight!
		------------------------------------------------------------------
		KNOTE is the editor object, derived from class 'object'.
		It's instantiation initilizer requires the
		ubiquitous declaration of the 'self' reference
		implied at call time, as well as a handle to
		the lexer to be used for text decoration.
		-------------------------------------------------------------------
		We tested it on Elementry OS, Ubuntu, Linux Mint, Antix Linux, MX Linux,
		Windows 10, Windows 7, Windows XP!
		We never tested it on MacOS/Darwin! :(
	"""
	__module__ = 'builtins'
	def __init__(self, lexer):
		self.uiopts = []
		self.lexer = lexer
		self.lastRegexp = ""
		self.makedLine = 0
		self.root = tkinter.Tk()
		self.root.title('KNOTE v2.0')
		self.root.resizable(False, False)
		self.root.wm_iconbitmap('mainicon.ico')
		self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
		self.uiconfig()
		self.root.bind("<Key>", self.event_key)
		self.root.bind('<Control-KeyPress-q>', self.root.destroy)
		self.root.bind('<Button>', self.event_mouse)
		self.root.bind('<Configure>', self.eventmouse)
		self.text.bind('<Return>', self.autoindent)
		self.text.bind('<Tab>', self.tab2spaces4)
		###########################################
		self.root.bind('<Control-o>',  self.open_file)
		self.root.bind('<Control-s>',  self.save_file)
		self.root.bind('<Control-Shift-s>',  self.extractText)
		self.root.bind('<Alt-F4>',  self.root.destroy)
		self.root.bind('<F1>', self._help)
		self.root.bind('<F3>', self.find_bug)
		############################################
		self.create_tags()
		self.text.edit_modified(False)
		self.bootstrap = [self.recolorize]
		self.FILENAME = 'main.py'

		self.global_menu = tkinter.Menu(self.root)
		self.root.config(menu=self.global_menu)
		self.help_menu = tkinter.Menu(self.global_menu, tearoff=False)
		self.file_menu = tkinter.Menu(self.global_menu, tearoff=False)
		self.file_menu.add_command(label='Open file', accelerator='Ctrl+O', command= self.open_file)
		self.file_menu.add_command(label='Save file', accelerator='Ctrl+S', command= self.save_file)
		self.file_menu.add_command(label='Save as', accelerator='Ctrl+Shift+S', command= self.extractText)
		self.file_menu.add_command(label='Exit', accelerator='Ctrl+Q', command= self.root.destroy)
		
		if len(sys.argv) is 1:
			self.FILENAME = sys.argv[1]

		with open(self.FILENAME, "r") as f:
			self.loadfile(f.read())

	def uiconfig(self):
		"""
			this method sets up the main window and two text widgets (the editor widget, and a text entry widget for the commandline).
		"""

		self.uiopts = {
			"height": "60",
			"width": "132",
			"cursor": "xterm",
			"bg": "#00062A",
			"fg": "#FFAC00",
			"insertbackground": "#FFD310",
			"insertborderwidth": "1",
			"insertwidth": "3",
			"exportselection": True,
			"undo": True,
			"selectbackground": "#E0000E",
			"inactiveselectbackground": "#E0E0E0"
		}

		self.text = scrolledtext.ScrolledText(master=self.root, **self.uiopts)
		self.text.vbar.configure(
			width = "3m",
			activebackground = "#FFD310",
			borderwidth = "0",
			background = "#68606E",
			highlightthickness = "0",
			highlightcolor = "#00062A",
			highlightbackground = "#00062A",
			troughcolor = "#20264A",
			relief = "flat"
		)

		self.cli = tkinter.Text(self.root,{
								"height": "1",
								"bg": "#191F44",
								"fg": "#FFC014",
								"insertbackground": "#FFD310",
								"insertborderwidth": "1",
								"insertwidth": "3",
								"exportselection": True,
								"undo": True,
								"selectbackground": "#E0000E",
								"inactiveselectbackground": "#E0E0E0"
							})
		self.text.grid(column = 0, row = 0, sticky = ('nsew'))
		self.cli.grid(column = 0, row = 1, pady = 1, sticky = ('nsew'))
		self.cli.bind("<Return>", self.cmdlaunch)
		self.cli.visible = True
		self.root.grid_columnconfigure(0, weight = 1)
		self.root.grid_rowconfigure(0, weight = 1)
		self.root.grid_rowconfigure(1, weight = 0)

	def open_file(self, event=None):
		try:
			self.FILENAME = fd.askopenfilename()
			f =  open(self.FILENAME, 'r')
			self.text.delete('1.0', tkinter.END)
			self.text.insert(INSERT, f.read())
		except FileNotFoundError:
			print('[Error]: FileNotFoundError!')

	def save_file(self, event=None):
		if self.FILENAME:
			f = open(self.FILENAME, 'w')
			f.write(self.text.get('1.0', tkinter.END))
		else:
			self.extractText()

	def extractText(self, event=None):
		try:
			self.FILENAME = fd.asksaveasfilename(filetypes=(("TXT files", '*.txt'), ('HTML file', '*html'), ("All files", '*.*') ))
			f = open(self.FILENAME,'w')
			f.write(self.text.get('1.0', tkinter.END))
		except FileNotFoundError:
			print('[Error]: FileNotFoundError!')

	def _help(self, event=None):
		__text = """\
KNOTE project were opened by Ilyosiddin Kalandar
(c) iCoder-new (Ehsonjon Gadoev) for making better! ;)
Developers:
	Ilyosiddin Kalandar\t<ilyosiddin_kalandar@mail.ru>
	Ehsonjon Gadoev\t<priler05@gmail.com>
"""
		mb.showinfo("KNOTE [Info]", __text)
		del __text

	def find_bug(self):
		md.showinfo('KNOTE [BUG REPORT]', 
			"Hello!\nIf you found bug please create issue on https://github.com/ikalandar/KNOTE/issue =)")

	def updatetitlebar(self):
		"""
			this method updates the status information in the window title
		"""
		if self.text.edit_modified() == False:
			sb = "KNOTE - Text Editor"
		else:
			sb = "KNOTE - Text Editor [%s]" % self.FILENAME
		self.root.title(sb)
		self.root.update()

	def search(self, regexp, currentposition):
		"""
			this method implements the core functionality of the search feature arguments: the search target as a regular expression and the position from which to search.
		"""
		characters = tkinter.StringVar()
		index_start = ""
		index_end = ""

		try:
			index_start = self.text.search(
				regexp,
				currentposition + "+1c",
				regexp = True,
				count = characters
			)
		except _tkinter.TclError:
			index_start = "1.0"

		if index_start == "":
			index_start = self.text.index("insert")

		length = characters.get()

		if length == "":
			length = "0"

		index_end = "{0}+{1}c".format(index_start, length)
		return index_start, index_end

	def replace(self, regexp, subst, cp):
		"""
			this method implements the search+replace compliment to the search functionality
		"""
		index_start, index_end = self.search(regexp, cp)

		if index_start != index_end:
			self.text.delete(index_start, index_end)
			self.text.insert(index_start, subst)

		return index_start, index_end

	def gotoline(self, linenumber):
		"""
			this method implements the core functionality to locate a specific line of text by line position arguments: the target line number
		"""
		index_start = linenumber+".0"
		index_end = linenumber+".end"
		return index_start, index_end

	def cmd(self, cmd, index_insert):
		"""
			this method parses a line of text from the command line and invokes methods on the text as indicated for each of the implemented commands arguments: the command, and the insert position
		"""
		index_start = ""
		index_end  = ""
		regexp = ""
		linenumber = ""
		cmdchar = cmd[0:1] # truncate newline
		cmd = cmd.strip("\n")

		if len(cmdchar) == 1:
			regexp = self.lastRegexp
			linenumber = self.markedLine

		if cmdchar == "*":
			if len(cmd) > 1:
				regexp = cmd[1:]
				index_start, index_end = self.search(regexp, index_insert)
				self.lastRegexp = regexp
		elif cmdchar == "#":
			if len(cmd) > 1:
				linenumber = cmd[1:]
			index_start, index_end = self.gotoline(linenumber)
			self.markedLine = linenumber 
		elif cmdchar == "/":  
			if len(cmd) > 3:    #  the '/', delimter chr, 1 chr target, delimiter chr, null for minimum useful s+r
				snr = cmd[1:]
				token = snr[0]
				regexp = snr.split(token)[1]
				subst = snr.split(token)[2]
				index_start, index_end = self.replace(regexp,subst,index_insert)
		return index_start, index_end

	def cmdcleanup(self, index_start, index_end):
		"""
			this method cleans up post-command and prepares the command line for re-use arguments: index beginning and end. ** this needs an audit, as does the entire index start/end construct **
		"""
		if index_start != "":
			self.text.mark_set("insert", index_start)
			self.text.tag_add("sel", index_start, index_end)
			self.text.see(index_start)
			self.cli.delete("1.0", tkinter.END)

	def cmdlaunch(self, event):
		"""
			this method implements the callback for the key binding (Return Key) in the command line widget, wiring it up to the parser/dispatcher method. arguments: the tkinter event object with which the callback is associated
		"""
		cmd = self.cli.get("1.0", tkinter.END)
		index_insert = self.text.index("insert")

		if index_insert == None:
			index_insert = "1.0"
		self.text.tag_delete("sel")

		index_start, index_end = self.cmd(cmd, index_insert)

		if index_start != "-1.0":
			self.cmdcleanup(index_start, index_end)

		return "break"

	def autoindent(self, event):
		"""
			this method implements the callback for the Return Key in the editor widget. arguments: the tkinter event object with which the callback is associated
		"""
		indentation = ""
		lineindex = self.text.index("insert").split(".")[0]
		linetext = self.text.get(lineindex+".0", lineindex+".end")

		for character in linetext:
			if character in [" ","\t"]:
				indentation += character
			else:
				break

		self.text.insert(self.text.index("insert"), "\n"+indentation)
		return "break"
	
	def tab2spaces4(self, event):
		"""
			this method implements the callback for the indentation key (Tab Key) in the editor widget. arguments: the tkinter event object with which the callback is associated
		"""
		self.text.insert(self.text.index("insert"), "    ")
		return "break"

	def loadfile(self, text):
		"""
			this method implements loading a file into the editor. arguments: the scrollable text object into which the text is to be loaded
		"""
		if text:
			self.text.insert(tkinter.INSERT, text)
			self.text.tag_remove(tkinter.SEL, '1.0', tkinter.END)
			self.text.see(tkinter.INSERT)


	def event_key(self, event):
		"""
			this method traps the keyboard events. anything that needs doing when a key is pressed is done here. arguments: the associated event object
		"""
		keycode = event.keycode
		char = event.char
		self.recolorize()
		self.updatetitlebar()

	def event_write(self, event):
		"""
			the callback method for the root window 'ctrl+w' event (write the file to disk) arguments: the associated event object.
		"""
		with open(self.FILENAME, "w") as filedescriptor:
			filedescriptor.write(self.text.get("1.0", tkinter.END)[:-1])

		self.text.edit_modified(False)
		self.root.title("KNOTE: File Written.")

	def event_mouse(self, event):
		"""
			this method traps the mouse events. anything that needs doing when a mouse operation occurs is done here. arguments: the associated event object
		"""
		self.updatetitlebar()

	def mainloop(self):
		"""
			the classical tkinter event driver loop invocation, after running through any startup tasks
		"""

		for task in self.bootstrap:
			task()

		self.root.mainloop()

	def create_tags(self):
		"""
			thmethod creates the tags associated with each distinct style element of the source code 'dressing'
		"""
		bold_font = font.Font(self.text, self.text.cget("font"))
		bold_font.configure(weight=font.BOLD)
		italic_font = font.Font(self.text, self.text.cget("font"))
		italic_font.configure(slant=font.ITALIC)
		bold_italic_font = font.Font(self.text, self.text.cget("font"))
		bold_italic_font.configure(weight=font.BOLD, slant=font.ITALIC)
		style = get_style_by_name('colorful')

		for ttype, ndef in style:
			tag_font = None

			if ndef['bold'] and ndef['italic']:
				tag_font = bold_italic_font
			elif ndef['bold']:
				tag_font = bold_font
			elif ndef['italic']:
				tag_font = italic_font

			if ndef['color']:
				foreground = "#%s" % ndef['color'] 
			else:
				foreground = None

			self.text.tag_configure(str(ttype), foreground=foreground, font=tag_font)

	def eventmouse(self, event):
		self.recolorize()

	def recolorize(self):
		"""
			this method colors and styles the prepared tags
		"""
		code = self.text.get("1.0", "end-1c")
		tokensource = self.lexer.get_tokens(code)
		start_line=1
		start_index = 0
		end_line=1
		end_index = 0

		for ttype, value in tokensource:
			if "\n" in value:
				end_line += value.count("\n")
				end_index = len(value.rsplit("\n",1)[1])
			else:
				end_index += len(value)

			if value not in (" ", "\n"):
				index1 = "%s.%s" % (start_line, start_index)
				index2 = "%s.%s" % (end_line, end_index)

				for tagname in self.text.tag_names(index1): # FIXME
					self.text.tag_remove(tagname, index1, index2)

				self.text.tag_add(str(ttype), index1, index2)

			start_line = end_line
			start_index = end_index

if __name__ == "__main__":
	extens = ""

	try:
		extens = sys.argv[1].split('.')[1]
	except IndexError:
		pass

	if extens == "py" or extens == "pyw" or extens == "sc" or extens == "sage" or extens == "tac":
		ui_core = App(lexer = PythonLexer())
	elif extens == "txt" or extens == "README" or extens == "text":
		ui_core = App(lexer = TextLexer())
	elif extens == "htm" or extens == "html" or extens == "css" or extens == "js" or extens == "md":
		ui_core = App(lexer = HtmlLexer())
	elif extens == "xml" or extens == "xsl" or extens == "rss" or extens == "xslt" or extens == "xsd" or extens == "wsdl" or extens == "wsf":
		ui_core = App(lexer = XmlLexer())
	elif extens == "php" or extens == "php5":
		ui_core = App(lexer = HtmlPhpLexer())
	elif extens == "pl" or extens == "pm" or extens == "nqp" or extens == "p6" or extens == "6pl" or extens == "p6l" or extens == "pl6" or extens == "pm" or extens == "p6m" or extens == "pm6" or extens == "t":
		ui_core = App(lexer = Perl6Lexer())
	elif extens == "rb" or extens == "rbw" or extens == "rake" or extens == "rbx" or extens == "duby" or extens == "gemspec":
		ui_core = App(lexer = RubyLexer())
	elif extens == "ini" or extens == "init":
		ui_core = App(lexer = IniLexer())
	elif extens == "conf" or extens == "cnf" or extens == "config":
		ui_core = App(lexer = ApacheConfLexer())
	elif extens == "sh" or extens == "cmd" or extens == "bashrc" or extens == "bash_profile":
		ui_core = App(lexer = BashLexer())
	elif extens == "diff" or extens == "patch":
		ui_core = App(lexer = DiffLexer())
	elif extens == "cs":
		ui_core = App(lexer = CSharpLexer())
	elif extens == "sql":
		ui_core = App(lexer = MySqlLexer())
	else:
		ui_core = App(lexer = PythonLexer())    # default (no extension) lexer is python
	ui_core.mainloop()
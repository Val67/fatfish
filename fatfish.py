#!/usr/bin/python3
import tkinter, os

class fatfish(tkinter.Tk):
	def __init__(self,parent):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()
		
		self.files = ""
	
	def initialize(self):
		self.grid()

		self.query = tkinter.Entry(self)
		self.query.grid(column=0, row=0, sticky="NEWS")
		self.query.bind("<Return>", self.OnEnter)
		self.query.focus_set()

		self.results = tkinter.Listbox(self)
		self.results.grid(column=0, row=1, sticky="NEWS")
		self.results.bind("<Double-Button-1>", self.OnSelect)
		
		self.path = tkinter.Entry(self)
		self.path.grid(column=0, row=2, sticky="NEWS")
		self.path.insert(tkinter.END, "~")
		
		self.queryxcludeHidden = tkinter.StringVar()
		# See https://www.linuxquestions.org/questions/linux-general-1/how-to-tell-find-to-not-search-inside-hidden-folders-208169/#post1062166
		self.check = tkinter.Checkbutton(self, text="Show Hidden Files", var=self.queryxcludeHidden, offval="\( ! -regex '.*/\..*' \)", onval="", command=self.DoSearch)
		self.check.grid(column=0, row=3)
		
		self.grid_columnconfigure(0,weight=1)
		self.grid_rowconfigure(1,weight=1)
	
	def OnSelect(self, evt):
		f = self.results.curselection()[0]
		os.system("xdg-open \"" + self.files[f] + "\"")
		
	def OnEnter(self, evt):
		self.DoSearch()
		
	def DoSearch(self):
		self.files = os.popen("find " + self.path.get() + " " + self.queryxcludeHidden.get() + " -name \"*" + self.query.get() + "*\"").read().split("\n")
		
		self.results.delete(0, tkinter.END)
		
		for i, p in enumerate(self.files):
			self.results.insert(tkinter.END, p)
		
		self.results.delete(tkinter.END) # Removes the last element to correct find printing \n at the end

if __name__ == "__main__":
	app = fatfish(None)
	app.title("fatfish")
	app.geometry("400x300")
	app.mainloop()

from tkinter import *
import os

# Copyright 2017 Jon Stephan

#    This file is part of ChessViz.

#    ChessViz is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    ChessViz is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with ChessViz.  If not, see <http://www.gnu.org/licenses/>.

class Dialog(Toplevel):
    def __init__(self, parent, default_values, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        
        if title:
            self.title(title)
            
        self.parent = parent
        self.result = None
        
        body = Frame(self)
        self.initial_focus = self.body(body, default_values)
        body.pack( padx=5, pady=5 )
        
        self.buttonBox()
        
        self.grab_set()
        
        if not self.initial_focus:
            self.initial_focus = self
            
        self.protocol("WM_DELETE_WINDOW", self.cancel )
        self.geometry( "+%d+%d" % ( parent.winfo_rootx() + 50 , parent.winfo_rooty()+ 50 ) )
        
        self.initial_focus.focus_set()
        
        self.wait_window( self )
        
    def body(self, master, default_values):
        pass
    
    def buttonBox(self):
        box = Frame(self)
        
        w = Button( box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button( box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        
        box.pack()
        
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
        
    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()
        
    def validate(self):
        return 1
    
    def apply(self):
        pass
    
class MyDialog( Dialog ):
    #### example of creating an instance of this dialog
    def body(self, master):
        
        Label(master, text="First:").grid( row = 0)
        Label(master, text="Second:").grid( row = 1)
        
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        
        self.e1.grid( row = 0, column = 1)
        self.e2.grid( row = 1, column = 1)
        return( self.e1 ) # initial focus 
    
    def apply(self):
        first = int( self.e1.get() ) 
        second = int( self.e2.get() )
        print(first, second)
        
        
    

   
#root = Tk()
#Button(root, text="Hello!").pack()
#root.update()
   
#d = MyDialog( root) 
   
#root.wait_window() 
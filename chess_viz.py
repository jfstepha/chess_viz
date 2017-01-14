#!/usr/bin/python3
#chess_viz.py

# chess_viz
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
'''
chess_viz.py - visualizes the space of possible chess moves
'''
#from graphics import *
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import pickle
import dialog
import pgn_crunch

#root = tk.Tk()

from chessDB import *
import chess

################################################################################
def ptInRect(pnt, rec):
    p1 = (rec[0],rec[1])
    p2 = (rec[2],rec[3])
    if pnt[0] > p1[0] and pnt[0] < p2[0] and pnt[1] > p1[1] and pnt[1] < p2[1]:
        return True
    else:
        return False
################################################################################
def padValid(g, move_prefix):
        print("padding")
        
        a = chess.Board()

        # make the move_prefix moves:
        for m in move_prefix.split():
            a.push_san( m )

        a.generate_legal_moves()
        
        for b in a.legal_moves:
            str = a.san( b )
            #print("checking move %s" % str)
            i = g.findMoveInGamelist( str )
            if i == -1:
                g.gamelist.append( GameNode( str, 0,0))
                #print("move %s was not present, adding it" % str)
            i = g.findMoveInGamelist( str )
            g2 = g.gamelist[i].next_move
            a.push( b )
            a.generate_legal_moves()
            for c in a.legal_moves:
                str2 = a.san( c )
                #print( "  checking move %s %s" % (str, str2))
                j = g.findMoveInGamelist( str2 )
                if j == -1:
                    g2.gamelist.append( GameNode( str2, 0,0))
                    #print("  move %s %s not in the list, adding it" %( str, str2))

                
            a.pop()
            
################################################################################
################################################################################
class ReadConvertDialog(dialog.Dialog):
################################################################################
################################################################################
    def body(self, master, default_values):
        Label(master, text="Input PGN filename:").grid(row=0)
        Label(master, text="Output database filename:").grid(row=1)
        Label(master, text="Plys").grid( row = 2)
        
        self.e1 = Entry(master, width=80)
        self.e2 = Entry(master, width=80)
        self.e3 = Entry(master, width=80)
        
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        
        self.e1.insert(0, default_values[0] )
        self.e2.insert(0, default_values[1] )
        self.e3.insert(0, default_values[2] )

        return self.e1
    
    def apply(self):
        self.infilename = self.e1.get()
        self.outfilename = self.e2.get()
        self.max_levels = int( self.e3.get() )

################################################################################
################################################################################
class ReadFilenameDialog(dialog.Dialog):
################################################################################
################################################################################
    def body(self, master, default_values):
        Label(master, text="Filename:").grid(row=0)
        
        self.e1 = Entry(master, width=80)
        
        self.e1.grid(row=0, column=1)
        
        self.e1.insert(0, default_values[0] )

        return self.e1
    
    def apply(self):
        self.filename = self.e1.get()

################################################################################
################################################################################
class ChessGrid:
################################################################################
################################################################################
    ################################################################################
    def __init__ (self, drawObj, g, max_level, ul, lr, ylab_width=40, draw_frame=True, draw_ylab=True, move_prefix="" ):
        self.drawObj = drawObj
        self.ul = ul
        self.lr = lr
        self.ymoves = []
        self.ylabs = []
        self.read_in_progress = False
        if draw_ylab:
            self.ylab_width = ylab_width
            self.xgap=10
        else:
            self.ylab_width=0
            self.xgap=0
        self.draw_frame = draw_frame
        self.g = g
        self.ymoves = []
        self.draw_ylab = draw_ylab
        self.calcParams()
        self.move_prefix=move_prefix
        self.cg2 = []

    ################################################################################
    def calcParams(self):

        # first find all the existing 2nd ply moves
        # and calculate the max count while we're at it
        self.maxcount = 0
        for i in range( len( self.g.gamelist)):
            g2 = self.g.gamelist[i].next_move
            for j in range( len( g2.gamelist ) ):
                t = g2.gamelist[j].move
                if g2.gamelist[j].count > self.maxcount:
                    self.maxcount = g2.gamelist[j].count
                try:
                    k = self.ymoves.index( t )
                except ValueError:
                    self.ymoves.append( t )

        # set the left edge of the boxes
        if self.draw_ylab:
            self.box_left = self.ul[0] + self.ylab_width
        else:
            self.box_left = self.ul[0]

        # set the box height and width
        if len(self.ymoves )> 0 :
            self.box_height = (self.lr[1] - self.ul[1]) / len( self.ymoves ) 
        else:
            self.box_height = 1
            
        if len(self.g.gamelist) == 0:
            self.box_width = 1
        else:
            self.box_width = (self.lr[0] - self.ul[0] - self.ylab_width - self.xgap) / (len( self.g.gamelist ) )

        if self.draw_ylab:
            self.box_left = self.ul[0] + self.ylab_width

    ################################################################################
    def drawChessGrid(self, max_level ):

        # draw the ylabels
        if self.draw_ylab:
            self.ylabs = []
            for i in range( len( self.ymoves ) ):
                self.drawObj.text( ( self.ul[0]+2, self.box_height * i + self.box_height/2.4 + self.ul[1] ), self.ymoves[i], fill=0 )
                #self.ylabs.append( Text( Point( self.ul.x + self.ylab_width / 2, self.box_height * i + self.box_height/2 + self.ul.y), self.ymoves[i]  ) ) 
                
        # draw boxes
        self.boxes = []
        b = 0;
        for i in range( len( self.g.gamelist ) ):
            for k in range( len( self.ymoves ) ):
#                self.boxes.append( Rectangle( Point( self.box_left + i * self.box_width,  self.ul.y + k * self.box_height),
#                                         Point( self.box_left + (i+1)*self.box_width, self.ul.y + (k+1)*self.box_height )))
                j = self.g.gamelist[i].next_move.findMoveInGamelist( self.ymoves[k] )
                if j > -1:
                    if self.g.gamelist[i].next_move.gamelist[j].count == 0:
                        fill_color = ( 240, 240, 255) 
                    elif self.g.gamelist[i].next_move.gamelist[j].count == -1:
                        fill_color = ( 0,0,0 )
                    else:
                        fill_color = ( int( 255 - 255 * self.g.gamelist[i].next_move.gamelist[j].count / self.maxcount)  ,255,0) 
                else:
                    fill_color = ( 255,235,235)

                if self.draw_frame:
                    outline_color = ( 220,220,220 ) 
                else:
                    outline_color = fill_color
                box = [ self.box_left + i * self.box_width, self.ul[1] + k * self.box_height,
                        self.box_left + (i+1) * self.box_width, self.ul[1] + (k+1) * self.box_height ]
                self.boxes.append(box)
                
                self.drawObj.rectangle( box, outline = outline_color, fill=fill_color )
                b += 1
        return 
        
            
            
    ################################################################################
    def checkBoxClicked(self, pt):
        i=0
        for j in range( len( self.g.gamelist ) ):
            for k in range( len( self.ymoves ) ):
                if ptInRect( pt, self.boxes[i]):
                    return (j,self.ymoves[k])
                i += 1
                
        return( -1, -1 )

        

    ################################################################################
    def deleteAll(self):
        for b in self.boxes:
            b.undraw()
        for y in self.ylabs:
            y.undraw()
        for cg in self.cg2:
            cg.deleteAll()


################################################################################
################################################################################
class MainWindow (tk.Tk):
################################################################################
################################################################################

        
    ################################################################################
    def __init__(self, gamelist, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title( "Chess Viz" )
        self.read_in_progress = False
        self.topgamelist = gamelist
        self.gamelist = gamelist
        self.move_prefix = ""
        
        self.main_img_width = 1000
        self.main_img_height = 800
        
        self.frame = Frame()
        self.frame.pack()
        
        ### buttons 
        self.frmButtons = Frame(  )
        self.frmButtons.pack( side = TOP )
        
        self.btnQuit = Button( self.frmButtons, text="QUIT", command=self.frame.quit)
        self.btnQuit.pack( side = LEFT )
        
        self.btnRead = Button( self.frmButtons, text="ReadData", command=self.handleRead)
        self.btnRead.pack( side = LEFT )

        self.btnDraw = Button( self.frmButtons, text="DrawGrid", command=self.handleDraw)
        self.btnDraw.pack( side = LEFT )

        self.btnTop = Button( self.frmButtons, text="TOP", command=self.handleTop)
        self.btnTop.pack( side = LEFT )
        
        self.btnDown = Button( self.frmButtons, text="DOWN", command=self.handleDown)
        self.btnDown.pack( side=LEFT )

        self.btnSave = Button( self.frmButtons, text="SaveImage", command=self.handleSave)
        self.btnSave.pack( side=LEFT )
        
        self.btnConvertPGN = Button( self.frmButtons, text="ConvertPGN", command=self.handlePgn)
        self.btnConvertPGN.pack( side=LEFT )

        ### status bar
        self.frmStatus = Frame( )
        self.frmStatus.pack( side=TOP )
       
        self.statusText = StringVar()
        self.statusText.set("Program starting..." )
        self.lblStatus = Label( self.frmStatus, textvariable=self.statusText)
        self.lblStatus.pack( side=TOP)
        self.prog = ttk.Progressbar( self.frmStatus, orient="horizontal",
                        length=200, mode="determinate")
        self.prog.pack( side=TOP)
        
        ### chess grid frame
        self.frmChessGrid = Frame( )
        self.frmChessGrid.pack( fill=BOTH, expand=1)
        
        
        self.topGridImage = Image.new( 'RGB', (self.main_img_width,self.main_img_height), (200,200,200))
        self.topDraw = ImageDraw.Draw( self.topGridImage)
        self.topGridImg = ImageTk.PhotoImage( self.topGridImage )
        self.topGridLabel = Label( self.frmChessGrid, image=self.topGridImg)
        self.topGridLabel.bind( "<1>", self.handleGridClick)
        self.topGridLabel.pack( fill=BOTH, expand=1 )
        

        self.win_width = 0
        self.win_height = 0        

        self.frmChessGrid.bind("<Configure>", self.handleResize)

        #self.handleRead()
        self.statusText.set("Done initializing" )


    ################################################################################
    def deleteAll(self):
        self.lblText.undraw()
        for b in self.headerBox:
            b.undraw()
        for t in self.lblTextCol:
            t.undraw()
        self.chessGrid.deleteAll()

    ################################################################################
    def drawFirstMoveHeader(self, drawObj, g, textHeight ):
        xlabWidth = 40
        gap = 10
        colWidth = (drawObj.width - xlabWidth - gap) / (len(g.gamelist) )

        drawObj.text( (0,0), "move1", fill=0)

        for i in range( len ( g.gamelist ) ):
            t = g.gamelist[i].move
            if g.gamelist[i].count < 1:
                fill_color = ( 200,200,200) 
                print( "move: %s, count: %d, maxcount:%d color:%d" % (t, g.gamelist[i].count, g.maxcount, 200) )
            else:
                fill_color = (int( 255 - 255 * g.gamelist[i].count / g.maxcount)  ,255,0 ) 
#                print( "move: %s, count: %d, maxcount:%d color:%d" % (t, g.gamelist[i].count, g.maxcount, 255-255*g.gamelist[i].count / g.maxcount))
            drawObj.text( ( xlabWidth + i * colWidth + colWidth/2.5 , 0 ), t, fill=0 )
            drawObj.rectangle( [ xlabWidth + colWidth * i , textHeight ,
                                 xlabWidth + (i+1) * colWidth , textHeight*2 ],
                              outline = (0,0,0), fill=fill_color )

    ################################################################################
    def drawChess(self, g, drawObj, max_level=0, draw_firstmove_header = True, move_prefix="", draw_status=True):
    
        textHeight = 12
        ylab_width = 40
        padValid( g, move_prefix )
        ul_grid = (0,0)
        if draw_firstmove_header:
            self.drawFirstMoveHeader( drawObj, g, textHeight)
            ul_grid = ( 0, textHeight * 3)
        if draw_status:
            self.statusText.set( "game:%s maxcount:%d level:%d maxlevel:%d" % (move_prefix, g.maxcount, g.move_level, max_level) )
        lr_grid = (drawObj.width, drawObj.height)
        
        self.chessGrid = ChessGrid( drawObj, g, max_level, ul_grid, lr_grid, ylab_width )
        self.chessGrid.drawChessGrid( max_level )

    ################################################################################
    def handleDraw(self):
        if self.read_in_progress:
            return
        self.statusText.set("drawing grid... ")
        #self.topGridImage.resize( (self.main_img_width, self.main_img_height) )

        self.topGridImage = Image.new( 'RGB', (self.main_img_width,self.main_img_height), (200,200,200))
        
        self.topDraw = ImageDraw.Draw( self.topGridImage )
        self.topDraw.width = self.topGridImg.width()
        self.topDraw.height = self.topGridImg.height()
        self.topDraw.rectangle([0,0,self.main_img_width, self.main_img_height], (200,200,200))

        self.drawChess(self.gamelist, self.topDraw, move_prefix = self.move_prefix)

        self.topGridLabel.destroy()
        self.topGridImg = ImageTk.PhotoImage( self.topGridImage )
        self.topGridLabel = Label( self.frmChessGrid, image=self.topGridImg)
        self.topGridLabel.bind( "<1>", self.handleGridClick)
        self.topGridLabel.pack( fill=BOTH )

    ################################################################################
    def handleRead(self):
        d = ReadFilenameDialog( self, ["game_counts.txt"] )
        filename = d.filename 
        self.max_bytes = self.gamelist.openFile( filename )
        self.read_in_progress = True
        self.prog["value"] = 0
        self.prog["maximum"] = self.max_bytes
        #self.prog.start()
        self.myUpdateProgress()

    ################################################################################
    def myUpdateProgress(self):
        self.bytes_read = self.gamelist.readSomeBytes( )
        self.statusText.set( "Reading database file, read %d bytes of %d (%0.1f%%)" % (self.bytes_read, self.max_bytes,
                             (100.0 * self.bytes_read / self.max_bytes)) )
        if self.bytes_read != -1:
            self.prog["value"] = self.bytes_read
            self.after( 10, self.myUpdateProgress)
        else:
            self.statusText.set( "done reading")
            self.read_in_progress = False
            self.handleDraw()


    ################################################################################
    def handleTop(self):
        print(" top button clicked ")
        self.move_prefix = ""
        self.gamelist = self.topgamelist
        self.max_level = 0
        self.handleDraw()
        
    ################################################################################
    def handleDown(self):

        self.cg2 = []
        i=-1
        cgi=0
        ymoves = self.chessGrid.ymoves
        
        self.prog["maximum"] = len( self.gamelist.gamelist) * len( ymoves )
    
        for j in range( len( self.gamelist.gamelist) ):
            for k in range( len( ymoves )):
                i += 1
                print("drawing grid %d %d" % (j,k))
                print("  ymove: %s" % ymoves[k])
                l = self.gamelist.gamelist[j].next_move.findMoveInGamelist( ymoves[k] )
                if l < 0:
                    continue
                g2 = self.gamelist.gamelist[j].next_move.gamelist[l].next_move
                mp2 = "%s %s %s" % (self.move_prefix, self.gamelist.gamelist[j].move, self.gamelist.gamelist[j].next_move.gamelist[l].move)
                if len( g2.gamelist ) == 0:
                    print("  no games, skipping")
                else:
                    padValid( g2, mp2 )
                    ul = ( self.chessGrid.boxes[i][0] + 1, self.chessGrid.boxes[i][1] + 1)
                    lr = ( self.chessGrid.boxes[i][2] - 1, self.chessGrid.boxes[i][3] - 1)
                    print("   ul: (%d, %d), lr: (%d, %d) " % (ul[0], ul[1], lr[0], lr[1]))
                    self.cg2.append( ChessGrid( self.topDraw, g2, 9999, ul=ul, lr=lr, draw_ylab=False,draw_frame=False,move_prefix=mp2 ) )
                    self.cg2[cgi].drawChessGrid( 9999 )
                    cgi += 1

                    self.topGridLabel.destroy()
                    self.topGridImg = ImageTk.PhotoImage( self.topGridImage )
                    self.topGridLabel = Label( self.frmChessGrid, image=self.topGridImg)
                    self.topGridLabel.bind( "<1>", self.handleGridClick)
                    self.topGridLabel.pack( fill=BOTH, expand=1 )
                   
                self.prog["value"] = i 
                    
                self.update()
                


    
    ################################################################################
    def handleGridClick(self,event):
        print("Grid clicked at (%d,%d)" % (event.x, event.y))
        (j,ymove) = self.chessGrid.checkBoxClicked( (event.x, event.y) )
        k = self.gamelist.gamelist[j].next_move.findMoveInGamelist( ymove )
        if j == -1:
            return
        else:
            self.move_prefix = "%s %s %s" % (self.move_prefix, self.gamelist.gamelist[j].move, self.gamelist.gamelist[j].next_move.gamelist[k].move)
            self.gamelist = self.gamelist.gamelist[j].next_move.gamelist[k].next_move
            self.max_level = self.gamelist.move_level
            self.handleDraw()

    ################################################################################
    def handleResize(self, event):            
        print("resizing: %s" % str(event))
        if event.width != self.main_img_width or event.height != self.main_img_height:
            self.main_img_height = event.height
            self.main_img_width = event.width

    ################################################################################
    def handleSave(self):
        d = ReadFilenameDialog( self, ["grid.jpg"] )
        self.statusText.set( "Saving %s..." % d.filename )
        self.topGridImage.save( d.filename )
        self.statusText.set( "Done saving %s." % d.filename )
    ################################################################################
    def handlePgn(self):
        self.handleTop()
        d = ReadConvertDialog( self, ["scid_all6.pgn", "game_counts.txt", "5"])
        p = pgn_crunch.PGNImporter( )
        p.openPgn( d.infilename, d.max_levels)
        self.prog["maximum"] = p.filesize
        update_freq = 2
        while p.more_games:
            p.readAnotherGame()
            #status_str = "read game %i (%d/%d=%0.2f%%) %s vs %s" % (p.i, p.read_so_far, p.filesize, p.percent_read, p.white, p.black)
            #status_str = status_str + " " * (100 - len(status_str))
            status_str = "read game %i (%d/%d=%0.2f%%) " % (p.i, p.read_so_far, p.filesize, p.percent_read)
            self.statusText.set( status_str )
            self.prog["maximum"] = p.filesize
            self.prog["value"] = p.read_so_far
            self.update()
            if p.i % update_freq == 0:
                self.gamelist = p.gamelist
                self.topgamelist = p.gamelist
                self.handleDraw()
                self.handleDown()
            if p.i > 10:
                update_freq = 10
            if p.i > 100:
                update_freq = 100
            if p.i > 500:
                update_freq = 500
        self.gamelist = p.gamelist
        self.topgamelist = p.gamelist
        self.statusText.set("writing %s out" % d.outfilename)
        self.update()
        self.gamelist.writeToFile( d.outfilename, d.max_levels )
        self.statusText.set("done.")
        
    ################################################################################
def print_game_list( gamelist) :
    for g in gamelist:
        g.print_node()

    ################################################################################
def main():
    gamelist = GameList()

    mainWin = MainWindow( gamelist )
    mainWin.mainloop()
    
main()

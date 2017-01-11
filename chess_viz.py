#!/usr/bin/python3
#chess_viz.py
'''
chess_viz.py - visualizes the space of possible chess moves
'''
#from graphics import *
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk

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
                    fill_color = ( 255,200,200)

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
        
        #self.btnRead = Button( self.frmButtons, text="ReadData", command=self.handleRead)
        #self.btnRead.pack( side = LEFT )

        self.btnDraw = Button( self.frmButtons, text="DrawGrid", command=self.handleDraw)
        self.btnDraw.pack( side = LEFT )

        self.btnTop = Button( self.frmButtons, text="TOP", command=self.handleTop)
        self.btnTop.pack( side = LEFT )
        
        self.btnDown = Button( self.frmButtons, text="DOWN", command=self.handleDown)
        self.btnDown.pack( side=LEFT )

        self.btnSave = Button( self.frmButtons, text="SAVE", command=self.handleSave)
        self.btnSave.pack( side=LEFT )
        
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

        self.handleRead()
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
        self.topGridLabel.pack( fill=BOTH, expand=1 )

    ################################################################################
    def handleRead(self):
        self.max_bytes = self.gamelist.openFile( "gamecounts_scid_all6_10.txt")
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
        self.topGridImage.save( "grid.jpg")
            

        
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

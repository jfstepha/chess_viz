#!/usr/bin/python3
from graphics import *
WIN_WID=1700
WIN_HEIGHT=1000

from chessDB import *
import chess

################################################################################
def ptInRect(pnt, rec):
    p1 = rec.p1
    p2 = rec.p2
    if pnt.x > p1.x and pnt.x < p2.x and pnt.y > p1.y and pnt.y < p2.y:
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
    def __init__ (self, win, g, max_level, ul, lr, ylab_width=40, draw_frame=True, draw_ylab=True, move_prefix="" ):
        self.win = win
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
            self.box_left = self.ul.x + self.ylab_width
        else:
            self.box_left = self.ul.x

        # set the box height and width
        if len(self.ymoves )> 0 :
            self.box_height = (self.lr.y - self.ul.y) / len( self.ymoves ) 
        else:
            self.box_height = 1
            
        if len(self.g.gamelist) == 0:
            self.box_width = 1
        else:
            self.box_width = (self.lr.x - self.ul.x - self.ylab_width - self.xgap) / (len( self.g.gamelist ) )

        if self.draw_ylab:
            self.box_left = self.ul.x + self.ylab_width
                    


    ################################################################################
    def drawChessGrid(self, max_level ):

        # draw the ylabels
        if self.draw_ylab:
            self.ylabs = []
            for i in range( len( self.ymoves ) ):
                self.ylabs.append( Text( Point( self.ul.x + self.ylab_width / 2, self.box_height * i + self.box_height/2 + self.ul.y), self.ymoves[i]  ) ) 
                if( self.box_height < 10):
                    self.ylabs[i].setSize( self.box_height)
                else:
                    self.ylabs[i].setSize(10)
                self.ylabs[i].draw( self.win )
                
        # draw boxes
        self.boxes = []
        b = 0;
        for i in range( len( self.g.gamelist ) ):
            for k in range( len( self.ymoves ) ):
                self.boxes.append( Rectangle( Point( self.box_left + i * self.box_width,  self.ul.y + k * self.box_height),
                                         Point( self.box_left + (i+1)*self.box_width, self.ul.y + (k+1)*self.box_height )))
                j = self.g.gamelist[i].next_move.findMoveInGamelist( self.ymoves[k] )
                if j > -1:
                    if self.g.gamelist[i].next_move.gamelist[j].count == 0:
                        fill_color = color_rgb( 240, 240, 255) 
                    elif self.g.gamelist[i].next_move.gamelist[j].count == -1:
                        fill_color = color_rgb( 0,0,0 )
                    else:
                        fill_color = color_rgb( int( 255 - 255 * self.g.gamelist[i].next_move.gamelist[j].count / self.maxcount)  ,255,0) 
                else:
                    fill_color = color_rgb( 255,200,200)
                self.boxes[b].setFill( fill_color )
                if self.draw_frame:
                    self.boxes[b].setOutline( color_rgb( 220,220,220 ) )
                else:
                    self.boxes[b].setOutline( fill_color )
                
                self.boxes[b].draw( self.win ) 
                b += 1
        
        if max_level > self.g.move_level:
            print("drawing next level")
            self.cg2 = []
            i=-1
            cgi=0
            for j in range( len( self.g.gamelist) ):
                for k in range( len(self.ymoves )):
                    i += 1
                    print("drawing grid %d %d" % (j,k))
                    print("  ymove: %s" % self.ymoves[k])
                    l = self.g.gamelist[j].next_move.findMoveInGamelist( self.ymoves[k] )
                    if l < 0:
                        continue
                    g2 = self.g.gamelist[j].next_move.gamelist[l].next_move
                    mp2 = "%s %s %s" % (self.move_prefix, self.g.gamelist[j].move, self.g.gamelist[j].next_move.gamelist[l].move)
                    if len( g2.gamelist ) == 0:
                        print("  no games, skipping")
                    else:
                        padValid( g2, mp2 )
                        ul = Point( self.boxes[i].p1.x + 1, self.boxes[i].p1.y + 1)
                        lr = Point( self.boxes[i].p2.x - 1, self.boxes[i].p2.y - 1)
                        print("   ul: (%d, %d), lr: (%d, %d) " % (ul.x, ul.y, lr.x, lr.y))
                        self.cg2.append( ChessGrid( self.win, g2, max_level, ul=ul, lr=lr, draw_ylab=False,draw_frame=False,move_prefix=mp2 ) )
                        self.cg2[cgi].drawChessGrid(max_level)
                        cgi += 1
            
            
            
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
class MainWindow:
################################################################################
################################################################################

        
    ################################################################################
    def __init__(self, gamelist):
        self.win_width = WIN_WID
        self.win_height = WIN_HEIGHT
        
        self.win = GraphWin('My win',self.win_width, self.win_height)
        self.updatePositionVals()
        
        self.quitBtnBox = Rectangle( self.quitUL, self.quitLL)
        self.quitBtnBox.draw(self.win)
        self.quitBtnText = Text( self.quitTxtPt, 'Quit' )
        self.quitBtnText.setFace("courier")
        self.quitBtnText.setSize(8)
        self.quitBtnText.draw(self.win) 

        self.topBtnBox = Rectangle( self.topUL, self.topLL)
        self.topBtnBox.draw(self.win)
        self.topBtnText = Text( self.topTxtPt, 'Top' )
        self.topBtnText.setFace("courier")
        self.topBtnText.setSize(8)
        self.topBtnText.draw(self.win) 

        self.downBtnBox = Rectangle( self.downUL, self.downLL)
        self.downBtnBox.draw(self.win)
        self.downBtnText = Text( self.downTxtPt, 'Down' )
        self.downBtnText.setFace("courier")
        self.downBtnText.setSize(8)
        self.downBtnText.draw(self.win) 

        self.statusText = Text( self.statusPt, "status:" )
        self.statusText.setSize( 8 )
        self.statusText.draw( self.win )

    ################################################################################
    def updatePositionVals(self):
        self.btnHeight = 20
        self.btnWidth = 50
        self.quitUL = Point( 10,10 )
        self.quitLL = Point( 10 + self.btnWidth, 10 + self.btnHeight )
        self.topUL = Point( self.quitLL.x+10 ,self.quitUL.y )
        self.topLL = Point( self.topUL.x + self.btnWidth, self.quitLL.y)
        self.downUL = Point( self.topLL.x+10 ,self.topUL.y )
        self.downLL = Point( self.downUL.x + self.btnWidth, self.quitLL.y)
        self.quitTxtPt= Point( 10 + self.btnWidth / 2 , 10 + self.btnHeight / 2 )
        self.topTxtPt= Point( self.topUL.x + self.btnWidth / 2 , self.topUL.y + self.btnHeight / 2 )
        self.downTxtPt= Point( self.downUL.x + self.btnWidth / 2 , self.downUL.y + self.btnHeight / 2 )
        self.statusPt = Point(  self.win_width / 2, 40 )
        self.statusBarUL = Point( 10, self.topLL.y + 20 )
        self.statusBarLR = Point( self.win_width - 10, self.topLL.y + 40)
        

    ################################################################################
    def deleteAll(self):
        self.lblText.undraw()
        for b in self.headerBox:
            b.undraw()
        for t in self.lblTextCol:
            t.undraw()
        self.chessGrid.deleteAll()
        
    ################################################################################
    def drawFirstMoveHeader(self, g, ul, lr, textHeight ):
        xlabWidth = 40
        colWidth = (lr.x - ul.x - xlabWidth - 10) / (len(g.gamelist) )

        self.lblText = Text( Point(xlabWidth/2 + ul.x ,0 + ul.y ), "move1" )
        self.lblText.setSize( textHeight )
        self.lblText.draw( self.win )
        self.lblTextCol = []
        self.headerBox = []
        for i in range( len ( g.gamelist ) ):
            t = g.gamelist[i].move
            self.lblTextCol.append( Text( Point(xlabWidth + (i) * colWidth + colWidth/2 + ul.x, 0 + ul.y), t ) )
            self.lblTextCol[i].setSize( textHeight )
            self.lblTextCol[i].draw( self.win )
            
            self.headerBox.append( Rectangle( Point( xlabWidth + i * colWidth + ul.x, textHeight + ul.y ),
                                              Point( xlabWidth + (i+1) * colWidth + ul.x, textHeight*2+ul.y)))
            self.headerBox[i].draw( self.win )
            if g.gamelist[i].count < 1:
                self.headerBox[i].setFill( color_rgb( 200,200,200) )
                print( "move: %s, count: %d, maxcount:%d color:%d" % (t, g.gamelist[i].count, g.maxcount, 200) )
            else:
                self.headerBox[i].setFill( color_rgb( int( 255 - 255 * g.gamelist[i].count / g.maxcount)  ,255,0))
                print( "move: %s, count: %d, maxcount:%d color:%d" % (t, g.gamelist[i].count, g.maxcount, 255-255*g.gamelist[i].count / g.maxcount))

    ################################################################################
    def drawStatus(self, text ):
        self.statusText.setText(text)

    ################################################################################
    def addFileProgress(self):
        self.fileProgressFrame = Rectangle( self.statusBarUL, self.statusBarLR )
        self.fileProgressBar = Rectangle( self.statusBarUL, self.statusBarLR)
        self.fileProgressBar2 = Rectangle( self.statusBarUL, self.statusBarLR)
        self.fileProgressBar.setFill("blue")
        self.fileProgressBar2.setFill("blue")
        self.fileProgressFrame.draw( self.win )
        self.fileProgressBar.draw( self.win )
        self.fileProgressBar2.draw( self.win )
    ################################################################################
    def deleteFileProgress(self):
        self.fileProgressBar.undraw()
        self.fileProgressBar2.undraw()
        self.fileProgressFrame.undraw()
        
    ################################################################################
    def updateFileStatus(self, text, percent ):
        self.drawStatus( self.statusText.setText(text))
        self.fileProgressBar.p2 = Point( self.statusBarLR.x * percent/100, self.statusBarLR.y)
        self.fileProgressBar.undraw()
        self.fileProgressBar.draw( self.win )
        self.fileProgressBar2.p1 = self.fileProgressBar.p1
        self.fileProgressBar2.p2 = self.fileProgressBar.p2
        self.fileProgressBar2.undraw()
        self.fileProgressBar2.draw( self.win)

            

            
        
                
    ################################################################################
    def drawChess(self, g, max_level=0, ul=Point(10,80), lr=Point( WIN_WID, WIN_HEIGHT), draw_firstmove_header = True, move_prefix="", draw_status=True):
        textHeight = 8
        ylab_width = 40
        ul_grid = ul
        padValid( g, move_prefix )
        if draw_firstmove_header:
            self.drawFirstMoveHeader( g, ul, lr, textHeight)
            ul_grid = Point( ul.x , ul.y + textHeight*3 )
        if draw_status:

            self.drawStatus( "game:%s maxcount:%d level:%d maxlevel:%d" % (move_prefix, g.maxcount, g.move_level, max_level) )
        
        self.chessGrid = ChessGrid( self.win, g, max_level, ul_grid, Point( lr.x, lr.y-10), ylab_width )
        self.chessGrid.drawChessGrid(max_level)
                
    ################################################################################
    def mainLoop(self, gamelist):
        g = gamelist
        move_prefix=""
        max_level=0
        while True:
            mousePt = self.win.getMouse()
            if ptInRect(mousePt, self.quitBtnBox ):
                print("quitting")
                return
            elif ptInRect( mousePt, self.topBtnBox ):
                print("back to top")
                g = gamelist
                move_prefix=""
                max_level=0
            elif ptInRect( mousePt, self.downBtnBox ):
                print("down button")
                max_level += 2
             
            else:   
                # if click in one of the boxes:
                (j,ymove) = self.chessGrid.checkBoxClicked( mousePt )
                k = g.gamelist[j].next_move.findMoveInGamelist( ymove )
                if j == -1:
                    continue
                else:
                    move_prefix = "%s %s %s" % (move_prefix, g.gamelist[j].move, g.gamelist[j].next_move.gamelist[k].move)
                    g = g.gamelist[j].next_move.gamelist[k].next_move
                    max_level = g.move_level
            self.deleteAll()
            #mousePt = self.win.getMouse()
            self.drawChess(g, max_level=max_level, move_prefix=move_prefix)
                    


        
    ################################################################################
def print_game_list( gamelist) :
    for g in gamelist:
        g.print_node()

    ################################################################################
def main():
    gamelist = GameList()
    
    mainWin = MainWindow( gamelist )
    mainWin.addFileProgress()
    gamelist.readFile( mainWin, "game_counts_example.txt" )
    #print("GameList:")
    #gamelist.printList()
    mainWin.deleteFileProgress()
    
    mainWin.drawChess( gamelist )
    mainWin.mainLoop( gamelist )

main()

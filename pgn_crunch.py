# pgn_crunch.py
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

import chess
import chess.pgn
import sys

from chessDB import *
########################################################################
########################################################################
class PGNImporter():
########################################################################
########################################################################
    def __init__(self):
        self.gamelist = GameList()
        self.gamelist.move_level = 0
        self.pgn = None
        self.filesize=0
        self.read_so_far=0
        self.percent_read=0
        self.more_games = False
        self.game_no = 0
        self.i = 0
        self.white=None
        self.black=None
        

    ###################################################################
    def openPgn(self, filename='C:/temp/example.pgn', max_levels=15):
        print( "opeining %s" % filename)
        self.pgn = open( filename )
        self.filesize = os.stat( filename ).st_size
        self.more_games = True
        self.max_levels=max_levels
        self.i=1
        
    ###################################################################
    def readAnotherGame(self):
        g = chess.pgn.read_game( self.pgn ) 
        self.read_so_far = self.pgn.tell()
        self.percent_read = 100.0 * self.read_so_far / self.filesize
            
        # check to see if this is the last game in the file
        if g == None:
            print("game = none")
            self.more_games = False
            return
            
        # check to see if there are any moves
        if g.variations == []:
                print("No variations, continuing")
                return
            
        # initialize variables
        move_list = []
        self.white='none'
        self.black='none'
        move_no=0
        result=""
            
        if 'White' in g.headers:
            self.white = g.headers['White']
        if 'Black' in g.headers:
            self.black = g.headers['Black']
        if 'Result' in g.headers:
            result = g.headers['Result']
            

        # while there are more moves
        while g.variations != []:
            # print ( "  read move#%d: %s" % (move_no, g.variations[0].san()) )
            move_list.append( g.variations[0].san())

            g = g.variations[0]
            move_no += 1
                
                
        print( "read game %d (%d/%d %0.3f%%): %s vs %s " % (self.i, self.read_so_far, self.filesize, self.percent_read, self.white, self.black ) )
        self.gamelist.addSingleGameFromList( move_list, 0, self.max_levels, result)
        self.i += 1
        

def main():
    if len( sys.argv) < 4:
        print("usage: python pgn_crunch.py input_pgn output_database plys")
        return(-1)
    
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    max_level = int(sys.argv[3])
    
    p = PGNImporter()

    p.openPgn(infilename,  max_level)
    while p.more_games:
        p.readAnotherGame()
    print("done importing.")
    gamelist = p.gamelist
    gamelist.writeToFile( outfilename, max_level )
    print("done writing.")
    
if __name__ == "__main__": 
    main()

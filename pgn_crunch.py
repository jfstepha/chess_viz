import chess
import chess.pgn
from chessDB import *

def importPgn(filename='C:/temp/example.pgn', max_levels=15):
    gamelist = GameList()
    print( "opeining %s" % filename)
    pgn = open( filename )
    more_games = True
    i=1
    while more_games:
        g = chess.pgn.read_game( pgn ) 
        
        # check to see if this is the last game in the file
        if g == None:
            print("game = none")
            more_games = False
            continue
        
        # check to see if there are any moves
        if g.variations == []:
            print("No variations, continuing")
            continue
        
        # initialize variables
        move_list = []
        white='none'
        black='none'
        move_no=0
        
        if 'White' in g.headers:
            white = g.headers['White']
        if 'Black' in g.headers:
            black = g.headers['Black']

        # while there are more moves
        while g.variations != []:
            # print ( "  read move#%d: %s" % (move_no, g.variations[0].san()) )
            move_list.append( g.variations[0].san())

            g = g.variations[0]
            move_no += 1
            
            
        print( "read game %d: %s vs %s: %s " % (i, white, black, str(g)) )
        gamelist.addSingleGameFromList( move_list, 0, max_levels)
        if i % 100 == 0:
            gamelist.printList()
        i += 1
    return gamelist
        

def main():
    gamelist = importPgn()
    print("done importing.")
    gamelist.writeToFile( "pgn_parsed.txt" )
    print("done writing.")
    
main()

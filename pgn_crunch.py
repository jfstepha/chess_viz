import chess
import chess.pgn
from chessDB import *

def importPgn(filename='C:/temp/example.pgn', max_levels=15):
    gamelist = GameList()
    gamelist.move_level = 0
    print( "opeining %s" % filename)
    pgn = open( filename )
    filesize = os.stat( filename ).st_size
    more_games = True
    i=1
    while more_games:
        g = chess.pgn.read_game( pgn ) 
        read_so_far = pgn.tell()
        
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
        result=""
        
        if 'White' in g.headers:
            white = g.headers['White']
        if 'Black' in g.headers:
            black = g.headers['Black']
        if 'Result' in g.headers:
            result = g.headers['Result']
        

        # while there are more moves
        while g.variations != []:
            # print ( "  read move#%d: %s" % (move_no, g.variations[0].san()) )
            move_list.append( g.variations[0].san())

            g = g.variations[0]
            move_no += 1
            
            
        print( "read game %d: %s vs %s: %s (%d/%d: %0.2f%%)" % (i, white, black, str(g), read_so_far, filesize, 100.0*read_so_far/filesize ) )
        gamelist.addSingleGameFromList( move_list, 0, max_levels, result)
        i += 1
    return gamelist
        

def main():
    gamelist = importPgn("c:/temp/kingbase/kingbase_all.pgn", 30)
    #gamelist = importPgn("C:/Users/jfstepha/Dropbox/chess/scid_all6.pgn", 30)
    print("done importing.")
    #gamelist.writeToFile( "gamecounts_scid_all6_5.txt", max_level=5 )
    #gamelist.writeToFile( "gamecounts_scid_all6_10.txt", max_level=10 )
    gamelist.writeToFile( "gamecounts_kingbase_5.txt", max_level=5 )
    gamelist.writeToFile( "gamecounts_kingbase_10.txt", max_level=10 )
    gamelist.writeToFile( "gamecounts_kingbase_15.txt", max_level=15 )
    gamelist.writeToFile( "gamecounts_kingbase_20.txt", max_level=20 )
    gamelist.writeToFile( "gamecounts_kingbase_25.txt", max_level=25 )
    gamelist.writeToFile( "gamecounts_kingbase_30.txt", max_level=30 )
    print("done writing.")
    
main()

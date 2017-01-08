import os
from datetime import datetime

################################################################################
################################################################################
class GameList:
    ''' holds a list of GameNodes '''
################################################################################
################################################################################

    ################################################################################
    def __init__(self):
        ''' GameList constructor '''
        self.gamelist = []
        self.maxcount = 0
        self.move_level = 9999
        
    ################################################################################
    def findMoveInGamelist(self, move_str):
        if self.gamelist == []:
            return -1
        
        for i in range(0, len(self.gamelist)):
            if self.gamelist[i].move == move_str:
                return i
            
        return -1
        
    ################################################################################
    def readFile(self, win=[], filename='game_counts.txt'):
        ''' reads a file and inserts it in the GameList '''
        f = open(filename,'r')
        filesize = os.stat( filename ).st_size
        i=0
        cur_bytes = 0
        last_update = datetime.now()
        for line in f:
            cur_bytes += len( line ) + 1
            self.fileParseLine( line )
            c = datetime.now() - last_update
            if c.microseconds > 20000:
                percent = 100.0 * cur_bytes/filesize 
                if win!=[]:

                    win.updateFileStatus( "Reading %s: read line %d (%0.2f%%)" % (filename, i, percent ), percent )
                last_update = datetime.now()
            i+=1
            
    ################################################################################
    def fileParseLine(self, line):
        ''' parses a single line and inserts it in the GameList '''
        sline = line.split(',')
        game_str = sline[0]
        if len( sline ) > 1:
            count = int(sline[1])
            self.addGame( game_str, count)
    ################################################################################
    def addMove(self, move_list, move_level, count):
        ''' take a move list with stats, and add the move at move_list[move_level] 
        if there are more moves, call addMove to this level's move list '''
        self.move_level = move_level
        move = move_list[ move_level ]
        if count > self.maxcount:
            self.maxcount = count
        
        i = self.findMoveInGamelist( move )
        if i == -1:
            # this move is not found
            i = len( self.gamelist )
            self.gamelist.append( GameNode( move, count, move_level ))
            
        #else:
            #print("game %s already found" % str( move_list ))
            
        # if the game is found, don't do anything, but add the next level
            
        if len( move_list ) > move_level + 1:
            # if there are more moves to add
            self.gamelist[i].next_move.addMove( move_list, move_level+1, count)


    ################################################################################
    def addGame(self, game_str, count ):
        ''' takes a game string (representing stats of one game) and adds it to the list '''
        moves = game_str.split()
        #print("moves: %s " % str(moves))
        self.addMove( moves, 0, count)

    ################################################################################
    def addSingleGameFromList(self, move_list, move_level, max_level):
        ''' takes a single game (list of moves) and increments the stats in the gamelist '''
        move = move_list[ move_level ]
        i = self.findMoveInGamelist( move )
        if i==-1:
            i = len( self.gamelist )
            self.gamelist.append( GameNode( move, 1, move_level))
        else:
            self.gamelist[i].count += 1
            
        if len( move_list ) > move_level + 1 and move_level <= max_level:
            self.gamelist[i].next_move.addSingleGameFromList( move_list, move_level+1, max_level)
        
    ################################################################################
    def printList(self, level=0):
        for move in self.gamelist:
            move.print_node()

    ################################################################################
    def writeList(self, filehandle, max_level, movestr):
        for move in self.gamelist:
            move.write_node( filehandle, max_level, movestr )

            
    ################################################################################
    def writeToFile( self, filename, max_level=5 ):
        f = open( filename, 'w' )
        self.writeList( f, max_level, "")
        f.close()
            
            


    
################################################################################
################################################################################
class GameNode:
################################################################################
################################################################################
    def __init__(self, move, count=0, level=0, next_move=None ):
        self.move = move
        self.count = count
        self.level = level
        self.next_move = GameList()

    ################################################################################
    def __str__(self):
        "m:%s c:%d l:%d" % (self.move, self.count, self.level)

    ################################################################################
    def print_node(self):
        indentstr = ' ' * self.level
        print("%s m:%s c:%d l:%d" % (indentstr, self.move, self.count, self.level))
        self.next_move.printList()

    ################################################################################
    def write_node(self, filehandle, max_level, movestr):
        if movestr == "":
            mymovestr = self.move
        else:
            mymovestr = movestr + " " + self.move
        filehandle.write( "%s,%d\n" % ( mymovestr, self.count ) )
        self.next_move.writeList( filehandle, max_level, mymovestr )

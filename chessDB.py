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
    def openFile(self, filename='game_counts_example.txt'):
        ''' reads a file and inserts it in the GameList '''
        self.f = open(filename,'r')
        filesize = os.stat( filename ).st_size
        self.cur_bytes = 0
        return filesize

    ################################################################################
    def readSomeBytes(self ):
        bytes_read_this_time = 0
        start_time = datetime.now()
        for line in self.f:
            self.cur_bytes += len( line ) + 1
            bytes_read_this_time += len( line ) + 1
            self.fileParseLine( line )
            c = datetime.now() - start_time
            if c.microseconds > 10000:
                    break
        if bytes_read_this_time == 0:
            self.f.close()
            return -1
        else:
            return self.cur_bytes
            
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
    def addSingleGameFromList(self, move_list, move_level, max_level, result="*"):
        ''' takes a single game (list of moves) and increments the stats in the gamelist '''
        if move_list == []:
            print ("empty move list")
            return
        if move_level >= len( move_list ):
            print ("past the end of list")
            return
        move = move_list[ move_level ]
        i = self.findMoveInGamelist( move )
        if i==-1:
            i = len( self.gamelist )
            self.gamelist.append( GameNode( move, 1, move_level))
            self.gamelist[i].move_level = move_level
        else:
            self.gamelist[i].count += 1

        if result == "0-1":
            self.gamelist[i].black_wins += 1
        elif result == "1-0":
            self.gamelist[i].white_wins += 1
        elif result == "1/2-1/2":
            self.gamelist[i].draws += 1
            
        if len( move_list ) > move_level + 1 and move_level <= max_level:
            self.gamelist[i].next_move.addSingleGameFromList( move_list, move_level+1, max_level, result )
            self.gamelist[i].next_move.move_level = move_level+1
        
    ################################################################################
    def printList(self, level=0):
        for move in self.gamelist:
            move.print_node()

    ################################################################################
    def writeList(self, filehandle, level, max_level, movestr):
        if self.move_level > level:
            return
        if self.move_level == level:
            for move in self.gamelist:
                move.write_this_node( filehandle, movestr )
            return
        else:
            for m in self.gamelist:
                #move.write_sub_nodes( filehandle, level, movestr )
                if movestr == "":
                    mymovestr = m.move 
                else:
                    mymovestr = movestr + " " + m.move
                m.next_move.writeList( filehandle, level, max_level, mymovestr )


            
    ################################################################################
    def writeToFile( self, filename, max_level=5 ):
        f = open( filename, 'w' )
        for level in range( max_level ):
            self.writeList( f, level, max_level, "")
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
        self.black_wins = 0
        self.white_wins = 0
        self.draws = 0

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
        filehandle.write( "%s,%d,%d,%d,%d\n" % ( mymovestr, self.count,self.white_wins, self.black_wins, self.draws ) )
        self.next_move.writeList( filehandle, max_level, mymovestr )

    ################################################################################
    def write_this_node(self, filehandle, movestr):
        if movestr == "":
            mymovestr = self.move
        else:
            mymovestr = movestr + " " + self.move
        filehandle.write( "%s,%d,%d,%d,%d\n" % ( mymovestr, self.count,self.white_wins, self.black_wins, self.draws ) )


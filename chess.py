import pdb
import random

class ChessEngine(object):
    # white on bottom, black on top
   
    def __init__(self):
        allqueen = ['WQ','WQ','WQ','WQ','Wk','WQ','WQ','WQ']
        firstrow = ['Wr','WN','WB','WQ','Wk','WB','WN','Wr'] # r is a R that hasn't moved
        wpawnrow = ['Wp','Wp','Wp','Wp','Wp','Wp','Wp','Wp'] # p is a P that hasn't moved
        blnkrow2 = ['00','00','00','00','00','00','00','00']
        blnkrow3 = ['00','00','00','00','00','00','00','00']
        blnkrow4 = ['00','00','00','00','00','00','00','00']
        blnkrow5 = ['00','00','00','00','00','00','00','00']
        bpawnrow = ['Bp','Bp','Bp','Bp','Bp','Bp','Bp','Bp']
        lastrow  = ['Br','BN','BB','BQ','Bk','BB','BN','Br'] # k is a K that hasn't moved
        self.board = [allqueen, wpawnrow, blnkrow2, blnkrow3,
                     blnkrow4, blnkrow5, bpawnrow, lastrow]
                     
        self.moverules = {'WR':[[0,7],[0,-7],[7,0],[-7,0]],
                          'Wr':[[0,7],[0,-7],[7,0],[-7,0]],
                          'WB':[[7,7],[7,-7],[-7,7],[-7,-7]],
                          'WQ':[[0,7],[0,-7],[7,0],[-7,0],
                               [7,7],[7,-7],[-7,7],[-7,-7]],
                          'WK':[[0,1],[0,-1],[1,0],[-1,0],
                               [1,1],[1,-1],[-1,1],[-1,-1]],
                          'Wk':[[0,1],[0,-1],[1,0],[-1,0],
                               [1,1],[1,-1],[-1,1],[-1,-1]],
                          'WN':[[2,1],[2,-1],[-2,1],[-2,-1],
                               [1,2],[1,-2],[-1,2],[-1,-2]],
                          'BR':[[0,7],[0,-7],[7,0],[-7,0]],
                          'Br':[[0,7],[0,-7],[7,0],[-7,0]],
                          'BB':[[7,7],[7,-7],[-7,7],[-7,-7]],
                          'BQ':[[0,7],[0,-7],[7,0],[-7,0],
                               [7,7],[7,-7],[-7,7],[-7,-7]],
                          'BK':[[0,1],[0,-1],[1,0],[-1,0],
                               [1,1],[1,-1],[-1,1],[-1,-1]],
                          'Bk':[[0,1],[0,-1],[1,0],[-1,0],
                               [1,1],[1,-1],[-1,1],[-1,-1]],
                          'BN':[[2,1],[2,-1],[-2,1],[-2,-1],
                               [1,2],[1,-2],[-1,2],[-1,-2]],
                          'WP':[[0,1],[-1,1],[1,1]],
                          'Wp':[[0,1],[0,2],[-1,1],[1,1]],
                          'BP':[[0,-1],[-1,-1],[1,-1]],
                          'Bp':[[0,-1],[0,-2],[-1,-1],[1,-1]]
                         }

        self.piecescore =  { '00': 0,
                             'Wp': 1,
                             'WP': 1,
                             'WN': 3,
                             'WB': 3,
                             'WR': 5,
                             'Wr': 5,
                             'WQ': 9, 
                             'Wk': 1000,
                             'WK': 1000,
                             'Bp': -1,
                             'BP': -1,
                             'BN': -3,
                             'BB': -3,
                             'BR': -5,
                             'Br': -5,
                             'BQ': -9, 
                             'Bk': -1000,
                             'BK': -1000,
                             
                            }  
                            
        self.whitepawnvaluebyrow = [1,1,1.1,1.2,1.6,2.3,2.5,9]
        self.blackpawnvaluebyrow = [-9,-2.5,-2.3,-1.6,-1.2,-1.1,-1,-1]                              
                         
        self.pawntopromote = [] # x,y location of the pawn that needs
                                # to be promoted 
        self.blackenpassantx = -1  # column where a black pawn can be capture via en passant
        self.whiteenpassantx = -1  # column where a white pawn can be capture via en passant 
                 
        self.movecount = 0  # number of valid moves that have been made
        self.currentopening = None
                 
        # the computer opens with a random opening if playing white
        # and a random defense if playing black.
        # Main purpose of the openings is to avoid a 4 move checkmate,
        # since the computer is only looking 3 moves ahead.
                 
        self.openings = [[[4,1,4,3],[6,0,7,2]],   # 1. e4 2. Nf3      - Ruy Lopez
                         [[4,1,4,3],[5,1,5,3]],   # 1. e4 2. f4       - King's Gambit
                         [[3,1,3,3],[2,1,2,3]]]   # 1. d4 2. c4       - Queen's Gambit

        self.defenses = [[6,6,6,5],             # 1. g6
                         [3,6,3,5]]            # 1. d6

        self.cpusourcex = 0    # the piece the cpu will search next
        self.cpusourcey = 0
        
        self.bestmove  = []
        self.bestscore = -30000
                        

    def printboard(self,board):
        for x in range(0,8):
            print board[7-x] 
            
    def getpiece(self, x, y):
        return self.board[y][x]        
            
    def getmovenotation(self, sourcex, sourcey, destx, desty):
        # return the algebraic notation of the move
        # for example
        
        # e4 e5    # pawn move
        # Nf3 Nc6  # knight move
        # Bb5 a6   # bishop move
        # Bd4 Bxe5 # bishop capture
        # e4xd6    # pawn capture
        # ex6d6e.p # en passant capture
        # Ra1 Ra8+ # check
        # e7 e8=Q  # pawn promotion.  
                   # for now, skip this, since our pawn 
                   # promotion is interactive.
        # 0-0      # kingside  castling
        # 0-0-0    # queenside castling
        
        notationstring = ""
        ranks = ['1','2','3','4','5','6','7','8'] # bottom to top
        files = ['a','b','c','d','e','f','g','h'] # left go right
        enpassant = False
        
        # get the piece
        colorpiece = self.board[sourcey][sourcex]
        color = colorpiece[0]
        piece = colorpiece[1]
        oppcolor = 'W'
        if color == 'W': oppcolor = 'B'
        if piece == 'r': piece = 'R'
        if piece == 'p' or piece == 'P': piece = ''
        if piece == 'k': piece = 'K'
        
        if piece == 'K' and abs(destx-sourcex) == 2:
            # castling.  Need to check queen or king side.        
            if destx < sourcex:
                notationstring = "0-0-0" # queenside castling
            else:
                notationstring = "0-0"   # kingside casting   
        else:
            notationstring = piece+files[sourcex]+ranks[sourcey]
            if piece != '': notationstring += ' '
            notationstring += piece
            # check for enpassant capture
            if piece == '' and abs(sourcex-destx) == 1 and self.board[sourcey][sourcex] == '00':
                enpassant = True
                notationstring += 'x'
            # check for capture
            destcolorpiece = self.board[desty][destx]
            destcolor = destcolorpiece[0]
            if destcolor != '0' and destcolor != color:
                notationstring += 'x'
            notationstring +=  files[destx]+ranks[desty]  
            # check if now in check
            newboard = self.fastcopy(self.board)  
            self.updateboardinplace(sourcex, sourcey, destx, desty,newboard)
            if self.checkifincheck(oppcolor, newboard):
                notationstring += '+'
        return notationstring   
    
    def checkifvalidmove(self, color, sourcex, sourcey, destx, desty):
        # if players piece not selected return False
        colorpiece = self.board[sourcey][sourcex]
        if colorpiece[0] != color:
            return False
        # if destination not in possible destinations return False
        if not self.checkifmoveispossibledest(sourcex, sourcey, destx, desty, self.board, True):
            return False
        return not self.wouldmoveexposecheck(sourcex,sourcey,destx,desty,self.board)
        
    def makevalidmove(self,sourcex, sourcey, destx, desty):
        print "DAGWOOD"
        colorpiece = self.board[sourcey][sourcex]
        self.updateboardinplace(sourcex,sourcey,destx,desty,self.board)  
        # set the en passant flag if necessary and clear the other 
        if colorpiece[0] == 'B': 
            self.whiteenpassantx = -1 # clear the other en passant flag
            if colorpiece[1] == 'p' and sourcey == 6 and desty == 4:
                self.blackenpassantx = sourcex
        else: 
            self.blackenpassantx = -1
            if colorpiece[1] == 'p' and sourcey == 1 and desty == 3:
                self.whiteenpassantx = sourcex
        self.movecount += 1
        
    def findoneoftwopieces(self, piece1, piece2, board):
        for y in range(0,8):
            if piece1 in board[y]:
                return board[y].index(piece1),y
            if piece2 in board[y]:
                return board[y].index(piece2),y
        return False,False
        
    def checkifincheck(self, color, board):
        # find the king
        kingx,kingy = self.findoneoftwopieces(color+'K', color+'k',board)
        for y in range(0,8):
            for x in range(0,8):
                # see if opponent piece can move to king
                piecetocheck = board[y][x]
                if piecetocheck[0] != '0' and piecetocheck[0] != color:
                    if self.checkifmoveispossibledest(x,y,kingx,kingy,board,False):
                        return True
        return False    
        
    def checkforpawnpromotion(self,color):
        # need one routine to detect the pawn promotion
        # another routine to promote the piece, since the user
        # will need to select which piece they want
        # they will likely want a queen
        # they may instead want a knight
        # they could conceivably want an even lesser piece
        # to avoid a stalemate.
        y = 0
        if color == 'W': y = 7
        for x in range(0,8):
            colorpiece = self.board[y][x]
            if colorpiece[1] == 'P':
                return x,y
        return -1,-1    
        
    def promotepawn(self,color,piece,x,y):
        colorpiece = color+piece
        self.board[y][x] = colorpiece
        return True

    def updateboardinplace(self,sourcex,sourcey,destx,desty,board):
        piece = board[sourcey][sourcex]
        if piece[1] == 'r': piece = piece[0]+'R'
        if piece[1] == 'k': piece = piece[0]+'K'
        if piece[1] == 'p': piece = piece[0]+'P'
        board[desty][destx] = piece
        board[sourcey][sourcex] = '00'
        # handle castle.  We moved the king.  Need to move the rook.
        if abs(sourcex - destx) == 2 and piece[1] == 'K':
            if sourcex < destx:
                rookpiece = board[sourcey][7]
                rookpiece = rookpiece[0]+'R'
                board[sourcey][5] = rookpiece
                board[sourcey][7] = '00'
            else:
                rookpiece = board[sourcey][0]
                rookpiece = rookpiece[0]+'R'
                board[sourcey][3] = rookpiece
                board[sourcey][0] = '00'
        # handle enpassant.
        if piece[0] == 'W':
            if desty == 5 and destx == self.blackenpassantx:
                board[4][self.blackenpassantx] = '00'       
      
        else:
            if desty == 2 and destx == self.whiteenpassantx:
                board[3][self.whiteenpassantx] = '00' 
                
    def fastcopy(self, b):
        return     [[b[0][0],b[0][1],b[0][2],b[0][3],b[0][4],b[0][5],b[0][6],b[0][7]],
                    [b[1][0],b[1][1],b[1][2],b[1][3],b[1][4],b[1][5],b[1][6],b[1][7]],
                    [b[2][0],b[2][1],b[2][2],b[2][3],b[2][4],b[2][5],b[2][6],b[2][7]],
                    [b[3][0],b[3][1],b[3][2],b[3][3],b[3][4],b[3][5],b[3][6],b[3][7]],
                    [b[4][0],b[4][1],b[4][2],b[4][3],b[4][4],b[4][5],b[4][6],b[4][7]],
                    [b[5][0],b[5][1],b[5][2],b[5][3],b[5][4],b[5][5],b[5][6],b[5][7]],
                    [b[6][0],b[6][1],b[6][2],b[6][3],b[6][4],b[6][5],b[6][6],b[6][7]],
                    [b[7][0],b[7][1],b[7][2],b[7][3],b[7][4],b[7][5],b[7][6],b[7][7]]]

    def wouldmoveexposecheck(self,sourcex,sourcey,destx,desty,board):
        
        colorpiece = board[sourcey][sourcex]
        color = colorpiece[0]
        newboard = self.fastcopy(board)
        self.updateboardinplace(sourcex,sourcey,destx,desty,newboard)
        return self.checkifincheck(color, newboard)

    def checkifcastleislegal(self, sourcex, sourcey, destx, desty, board):
        kingpiece = board[sourcey][sourcex]
        if kingpiece[1] != 'k': return False  # king has moved
        if destx < sourcex:
            if sourcex - destx != 2: return False
            rookx = 0
            rookpiece = board[sourcey][rookx]
            if rookpiece[1] != 'r': return False # rook has moved
            for x in range(1,4):
                colorpiece = board[sourcey][x]
                if colorpiece[1] != '0': return False  # square between king and rook occupied
            # check if in check at any intermediate positions
            for x in range(0,4):  # check if king would cross through check
                newboard = self.fastcopy(board) 
                newboard[sourcey][x] = kingpiece
                newboard[sourcey][sourcex] = '00'
                if self.checkifincheck(kingpiece[0],newboard): return False
        else:
            if destx - sourcex != 2: return False
            rookx = 7
            rookpiece = board[sourcey][rookx]
            if rookpiece[1] != 'r': return False # rook has moved
            for x in range(5,7):
                colorpiece = board[sourcey][x]
                if colorpiece[1] != '0': return False  # square between king and rook occupied
            # check if in check at any intermediate positions
            for x in range(5,8):  # check if king would cross through check
                newboard = self.fastcopy(board) 
                newboard[sourcey][x] = kingpiece
                newboard[sourcey][sourcex] = '00'
                if self.checkifincheck(kingpiece[0],newboard): return False
        return True

    def checkifmoveispossibledest(self, sourcex, sourcey, destx, desty, board, notcheckchecking):
        """ Return if a move is legal.
        notcheckchecking is a boolean.
        If False, then castle and en passant will not be checked.
        If True, castle and en passant will be checked.
        Use this when calling to see if a piece is checking the king,
        since a castle or en passant is never a checking move.
        """
        colorpiece = board[sourcey][sourcex]
        piececolor = colorpiece[0]
        piecetype  = colorpiece[1]
        potentialmoves = self.moverules[colorpiece] 
        if colorpiece[1] == 'P' or colorpiece[1] == 'p':      
            # handle the pawn separately from the other pieces
            for moverule in potentialmoves:
                checkx = sourcex
                checky = sourcey
                if checkx+moverule[0] == destx and checky+moverule[1] == desty:
                    if abs(moverule[0]) == 1:
                        # this is a capture rule
                        checkcolorpiece = board[desty][destx]
                        if checkcolorpiece[0] != piececolor and checkcolorpiece[0] != '0':
                            return True    # regular capture
                        if colorpiece[0] == 'W': # check for en passant
                            if desty == 5 and destx == self.blackenpassantx:
                                return True
                        else:
                            if desty == 2 and destx == self.whiteenpassantx:
                                return True
                    else: # check if moving 1 or 2
                        if abs(moverule[1]) == 2:
                           # 2 move initial case.
                           # need to make sure space in between is empty
                           checkx += moverule[0]/2
                           checky += moverule[1]/2
                           if board[checky][checkx] != '00': return False
                        if board[desty][destx] == '00': return True   # 1 move case
                                            # as well as destination of 2 move case
            return False
    
        # not a pawn
        for moverule in potentialmoves:
            checkx = sourcex
            checky = sourcey
            if abs(moverule[0]) == 7 or abs(moverule[1]) == 7:
                # process the range move
                # scale if down by 7
                scaledmoverule = [0,0]
                scaledmoverule[0] = moverule[0]/7
                scaledmoverule[1] = moverule[1]/7
                checkend = False
                while (not checkend):
                    checkx += scaledmoverule[0]
                    checky += scaledmoverule[1]
                    if checkx < 0 or checkx > 7:
                        checkend = True
                    elif checky < 0 or checky > 7:
                        checkend = True
                    else:    
                        checkcolorpiece = board[checky][checkx]
                        if checkcolorpiece[0] == piececolor:
                            checkend = True
                        elif checkcolorpiece[0] == '0':
                            # blank space.  
                            if checkx == destx and checky == desty:
                                return True
                        else:
                            # on opponent piece
                            checkend = True
                            if checkx == destx and checky == desty:
                                return True
            else:
                # process a jumpmove
                checkx += moverule[0]
                checky += moverule[1]
                if checkx == destx and checky == desty:
                    checkcolorpiece = board[checky][checkx]
                    if checkcolorpiece[0] != piececolor:
                        return True
                        
            if colorpiece[1] == 'k':        # Need to check if this is a castle
               if abs(sourcex - destx) == 2 and notcheckchecking:
                   return self.checkifcastleislegal(sourcex, sourcey, destx, desty, board)
                   
        return False
        
    
    def getcomputermoveincremental(self,whoseturn):
        print "DAGWOOD30"
        scoredone = False
        if self.movecount < 3:  # need to select a predefined opening
            if self.movecount == 0: 
                self.currentopening = random.choice(self.openings)
                return self.currentopening[0]
            if self.movecount == 2:
                return self.currentopening[1]
            else:
                return random.choice(self.defenses)
        else:
           loopcontinue = True
           while (loopcontinue == True):
               print "DAGWOOD1"
               sourcecolorpiece = self.board[self.cpusourcey][self.cpusourcex]
               if sourcecolorpiece[0] == whoseturn:
                   loopcontinue = False
               elif self.cpusourcex == 7 and self.cpusourcey == 7:
                   loopcontinue = False
                   scoredone = True  # no more values.  We can return the score
               else:
                   self.cpusourcex += 1
                   if self.cpusourcex == 8:
                       self.cpusourcex = 0
                       self.cpusourcey += 1
           # we now have the piece we want to search, or are out of pieces.
           if not scoredone:
               level = 2
               print "DAGWOOD2 level = ", level
               score, move = self.findscoreforonepiece(self.board, self.cpusourcex, 
                                     self.cpusourcey, whoseturn, whoseturn, level)
               print "DAGWOOD3"
               if self.bestscore < score:
                   self.bestscore = score
                   self.bestmove = move
               elif self.bestscore == score:  # PBA bowling ladder randomization
                   if random.choice([True,False]):
                       self.bestscore = score
                       self.bestmove = move
               if self.cpusourcex == 7 and self.cpusourcey == 7:
                   scoredone = True
               else:
                   self.cpusourcex += 1
                   if self.cpusourcex == 8:
                       self.cpusourcex = 0
                       self.cpusourcey += 1
           # continue here.  return either false or the score.        
           if scoredone:
               self.bestscore = -30000
               move = self.bestmove
               if move == []: return "RESIGN"
               self.bestmove = []
               self.cpusourcex = 0
               self.cpusourcey = 0
               return move
           else:
               return False   
                    
        
    def calculatescore(self,board, whoseturninthegame):
        totalscore = 0
        for x in range(0,8):
            for y in range(0,8):
                colorpiece = board[y][x]
                score = self.piecescore[colorpiece]
                if score == 1 or score == -1:
                    if colorpiece[0] == 'W': score = self.whitepawnvaluebyrow[y]
                    else: score = self.blackpawnvaluebyrow[y]
                totalscore += score
        if whoseturninthegame == 'W':
            return totalscore 
        else:
            return -totalscore 
            
    def getcomputermove(self, whoseturn):
        if self.movecount < 3:  # need to select a predefined opening
            if self.movecount == 0: 
                self.currentopening = random.choice(self.openings)
                return self.currentopening[0]
            if self.movecount == 2:
                return self.currentopening[1]
            else:
                return random.choice(self.defenses)
        else:
            bestscore, bestmove = self.findbestscoremove(self.board,whoseturn, whoseturn,3)  
        return random.choice(bestmove)      
            
        
    def findscoreforonepiece(self, board, sourcex, sourcey, whoseturninthegame, whosemoveintheanalysis, level):
        # finds the best score for one piece
        # Doing this so we give the UI a chance to update.
        # whoseturninthegame is who will move when the chosen turn is returned
        # whosemoveintheanalysis is whose move it is when looking ahead.
        # level is how many levels of searching we have left
        if level == 0:  # we are at the bottom of the tree.  Just return the score
            return self.calculatescore(board,whoseturninthegame), []
        bestmove = []
        print "DAGWOOD20"
        if whoseturninthegame == whosemoveintheanalysis:
            bestscore = -30000  # set initial value in case we can't move
        else:                   # if you can't move, that is bad
            bestscore = 30000   # if your opponent can't move, that is very good.
        whosemovenext = 'W'  # switch whose move it is
        if whosemoveintheanalysis == 'W':
            whosemovenext = 'B'     
        print "DAGWOOD21"   
        sourcecolorpiece = board[sourcey][sourcex]
        if sourcecolorpiece[0] == whosemoveintheanalysis:
            for destx in range(0,8):
                for desty in range(0,8):
                    if self.checkifmoveispossibledest(sourcex,sourcey,
                            destx, desty, board, False): # ignore enpassant and castling to save time
                        if not self.wouldmoveexposecheck(sourcex,sourcey,destx,desty,board):
                            move = (sourcex, sourcey, destx, desty)
                            #print move, level
                            #pdb.set_trace()
                            newboard = self.fastcopy(board) 
                            self.updateboardinplace(sourcex,sourcey,
                                destx,desty,newboard)
                            score,nextmove = self.findbestscoremove(newboard,
                                    whoseturninthegame,whosemovenext,level-1)
                            print "DAGW score = ", score, "bestscore = ", bestscore
                            #pdb.set_trace()
                            if bestscore == score:
                                bestmove.append(move)
                            elif whoseturninthegame == whosemoveintheanalysis:
                                if score > bestscore:
                                    bestmove = [move]
                                    bestscore = score
                            else:
                                if score < bestscore:
                                    bestmove = [move]
                                    bestscore = score
        print "bestscore =", bestscore, "bestmove =", bestmove, "level =", level   
        if len(bestmove) > 1:
            bestmove = random.choice(bestmove)
        elif len(bestmove) == 1:
            bestmove = bestmove[0]                             
        return bestscore, bestmove  
             
        
        
    def findbestscoremove(self,board, whoseturninthegame, whosemoveintheanalysis, level):
        # whoseturninthegame is who will move when the chosen turn is returned
        # whosemoveintheanalysis is whose move it is when looking ahead.
        # level is how many levels of searching we have left
        if level == 0:  # we are at the bottom of the tree.  Just return the score
            return self.calculatescore(board,whoseturninthegame), []
        bestmove = []
        if whoseturninthegame == whosemoveintheanalysis:
            bestscore = -30000  # set initial value in case we can't move
        else:                   # if you can't move, that is bad
            bestscore = 30000   # if your opponent can't move, that is very good.
        whosemovenext = 'W'  # switch whose move it is
        if whosemoveintheanalysis == 'W':
            whosemovenext = 'B'        
        for sourcex in range(0,8):
            for sourcey in range(0,8):
                sourcecolorpiece = board[sourcey][sourcex]
                if sourcecolorpiece[0] == whosemoveintheanalysis:
                    for destx in range(0,8):
                        for desty in range(0,8):
                            if self.checkifmoveispossibledest(sourcex,sourcey,
                                   destx, desty, board, False): # ignore enpassant and castling to save time
                                if not self.wouldmoveexposecheck(sourcex,sourcey,destx,desty,board):
                                    move = (sourcex, sourcey, destx, desty)
                                    print move, level
                                    #pdb.set_trace()
                                    newboard = self.fastcopy(board) 
                                    self.updateboardinplace(sourcex,sourcey,
                                       destx,desty,newboard)
                                    score,nextmove = self.findbestscoremove(newboard,
                                           whoseturninthegame,whosemovenext,level-1)
                                    print "score = ", score, "bestscore = ", bestscore
                                    #pdb.set_trace()
                                    if bestscore == score:
                                        bestmove.append(move)
                                    elif whoseturninthegame == whosemoveintheanalysis:
                                        if score > bestscore:
                                            bestmove = [move]
                                            bestscore = score
                                    else:
                                        if score < bestscore:
                                            bestmove = [move]
                                            bestscore = score
        print "bestscore =", bestscore, "bestmove =", bestmove, "level =", level                                
        return bestscore, bestmove  
 
        
                         
if __name__ == '__main__':
    import time
    import cProfile
    cb = ChessEngine()  
    cb.printboard(cb.board)
    cb.makevalidmove(4,1,4,3)
    cb.makevalidmove(4,6,4,5)
    cb.makevalidmove(4,3,4,4)
    cb.makevalidmove(3,7,7,3)
    cb.makevalidmove(7,3,7,2)
    
    #pdb.set_trace()
    print cb.checkifmoveispossibledest(6,0,7,2,cb.board,True)
    print cb.checkifincheck('B',cb.board)
    
    cb.printboard(cb.board)
    """print "move the knight"
    cb.updateboardinplace(1,0,0,2,cb.board)
    cb.updateboardinplace(0,2,1,4,cb.board)
    cb.updateboardinplace(0,6,0,4,cb.board)
    cb.updateboardinplace(0,4,0,3,cb.board)
    cb.updateboardinplace(0,3,0,2,cb.board)"""
    
    cb.updateboardinplace(4,6,4,4,cb.board)
    cb.updateboardinplace(5,7,2,4,cb.board)
    cb.updateboardinplace(3,7,7,3,cb.board)


    for x in range(0,8):
        for y in range(0,8):
            cb.board[y][x] = '00'  # clear the board.
            
    # populate it with a pattern where the computer is being unaggressive
    
    cb.board[0][4]='WK'
    cb.board[3][6]='BN'
    cb.board[4][7]='BQ'
    cb.board[5][5]='BP'
    cb.board[5][4]='BP'
    cb.board[5][3]='BP'
    cb.board[6][3]='BB'
    cb.board[6][2]='BK'
    cb.board[6][1]='BP'
    cb.board[6][0]='BP'
    cb.board[7][1]='BR'
    cb.board[7][5]='BR'
    
    pdb.set_trace()


    """cb.printboard(cb.board)
    print cb.wouldmoveexposecheck(3,1,3,2,cb.board)
    cb.board[0][0] = '00'
    cb.printboard(cb.board)
    print cb.calculatescore(cb.board,'W')
    print cb.calculatescore(cb.board,'B')
    #pdb.set_trace()
    time1 = time.time()
    print cb.findbestscoremove(cb.board,'W','W',1)
    time2 = time.time()
    print "took ", time2-time1, "seconds"
    print cb.findbestscoremove(cb.board,'W','W',2)
    time3 = time.time()
    print "took ", time3-time2, "seconds"
    print cb.findbestscoremove(cb.board,'W','W',3)
    time4 = time.time()
    print "took ", time4-time3, "seconds"
    print cb.getcomputermove('W')"""
 

    #pdb.set_trace()
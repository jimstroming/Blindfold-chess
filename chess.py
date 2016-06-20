import pdb
from copy import deepcopy

class Chessboard(object):
    # white on bottom, black on top
   
    def __init__(self):
        firstrow = ['Wr','WN','WB','WQ','Wk','WB','WN','Wr'] # r is a R that hasn't moved
        wpawnrow = ['Wp','Wp','Wp','Wp','Wp','Wp','Wp','Wp'] # p is a P that hasn't moved
        blnkrow2 = ['00','00','00','00','00','00','00','00']
        blnkrow3 = ['00','00','00','00','00','00','00','00']
        blnkrow4 = ['00','00','00','00','00','00','00','00']
        blnkrow5 = ['00','00','00','00','00','00','00','00']
        bpawnrow = ['Bp','Bp','Bp','Bp','Bp','Bp','Bp','Bp']
        lastrow  = ['Br','BN','BB','BQ','Bk','BB','BN','Br'] # k is a K that hasn't moved
        self.board = [firstrow, wpawnrow, blnkrow2, blnkrow3,
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
                          'WPnocapture':[[0,1]],
                          'WPcapture':[[-1,1],[1,1]],
                          'Wpnocapture':[[0,1],[0,2]],
                          'Wpcapture' : [[-1,1],[1,1]],
                          'BPnocapture':[[0,-1]],
                          'BPcapture':[[-1,-1],[1,-1]],
                          'Bpnocapture':[[0,-1],[0,-2]],                          
                          'Bpcapture':[[-1,-1],[1,-1]]
                         }

    def printboard(self):
        for x in range(0,8):
            print self.board[7-x] 
           
    def checkifvalidmove(self, color, sourcex, sourcey, destx, desty):
        # if players piece not selected return False
        colorpiece = self.board[sourcey][sourcex]
        if colorpiece[0] != color:
            print 'wrong color'
            return False
        # if destination not in possible destinations return False
        return self.checkifmoveispossibledest(sourcex, sourcey, destx, desty, self.board)
        
    def makevalidmove(self,sourcex, sourcey, destx, desty):
        self.updateboardinplace(sourcex,sourcey,destx,desty,self.board)    
        
    def findonepiece(self, piece, board):
        for y in range(0,8):
            if piece in board[y]:
                return board[y].index(piece),y
        return False,False
        
    def checkifincheck(self, color, board):
        # find the king
        kingx,kingy = self.findonepiece(color+'K',board)
        print 'king at',kingx,kingy
        for y in range(0,7):
            for x in range(0,7):
                # see if opponent piece can move to king
                piecetocheck = self.board[y][x]
                if piecetocheck[0] != '0' and piecetocheck[0] != color:
                    if self.checkifmoveispossibledest(x,y,kingx,kingy,board):
                        return True
        return False    

    def updateboardinplace(self,sourcex,sourcey,destx,desty,board):
        piece = board[sourcey][sourcex]
        pdb.set_trace()
        if piece[1] == 'r': piece = piece[0]+'R'
        if piece[1] == 'k': piece = piece[0]+'K'
        if piece[1] == 'p': piece = piece[0]+'P'
        board[desty][destx] = piece
        board[sourcey][sourcex] = '00'


    def wouldmoveexposecheck(self,sourcex,sourcey,destx,desty,board):
        
        colorpiece = board[sourcey][sourcex]
        color = colorpiece[0]
        newboard = deepcopy(board)
        self.updateboardinplace(sourcex,sourcey,destx,desty,newboard)
        return self.checkifincheck(color, newboard)

    def checkifmoveispossibledest(self, sourcex, sourcey, destx, desty, board):
        # get the piece and color
        colorpiece = board[sourcey][sourcex]
        print colorpiece
        piececolor = colorpiece[0]
        piecetype  = colorpiece[1]
        print piececolor
        print piecetype
        if colorpiece[1] == 'P' or colorpiece[1] == 'p':  # handle the pawn separately
            # this is just a stub so we don't crash
            # a lot more work to do on pawns.
            # probably a completely different if-else
            potentialmoves = self.moverules[colorpiece[0]+'Pnocapture']
        else:
            potentialmoves = self.moverules[colorpiece]
        print potentialmoves
        for moverule in potentialmoves:
            checkx = sourcex
            checky = sourcey
            print moverule
            if abs(moverule[0]) == 7 or abs(moverule[1]) == 7:
                # process the range move
                # scale if down by 7
                moverule[0] = moverule[0]/7
                moverule[1] = moverule[1]/7
                print moverule
                checkend = False
                while (not checkend):
                    checkx += moverule[0]
                    checky += moverule[1]
                    print checkx, checky
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
                if checkx >= 0 and checkx <= 7:
                    if checky >= 0 and checky <= 7:
                        checkcolorpiece = board[checky][checkx]
                        if checkcolorpiece[0] != piececolor:
                            if checkx == destx and checky == desty:
                                return True
                                
            # Need extra processing if move is king.
            # Need to check if this is a castle
            # ADD HERE                    
        return False
                         
if __name__ == '__main__':
    print "hello"
    cb = Chessboard()  
    cb.printboard()
    pdb.set_trace()
    print cb.checkifmoveispossibledest(6,0,7,2,cb.board)
    print cb.findonepiece('BQ',cb.board)
    print cb.checkifincheck('B',cb.board)
    
    cb.printboard()
    print "move the knight"
    cb.updateboardinplace(1,0,0,2,cb.board)
    cb.printboard()
    print cb.wouldmoveexposecheck(3,1,3,2,cb.board)
    cb.printboard()
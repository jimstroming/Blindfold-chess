import pdb

class Chessboard(object):
   
    def __init__(self):
        firstrow = ['WR','WN','WB','WQ','WK','WB','WN','WR']
        wpawnrow = ['WP','WP','WP','WP','WP','WP','WP','WP']
        blankrow = ['00','00','00','00','00','00','00','00']
        bpawnrow = ['BP','BP','BP','BP','BP','BP','BP','BP']
        lastrow  = ['BR','BN','BB','BQ','BK','BB','BN','BR']
        self.board = [firstrow, wpawnrow, blankrow, blankrow,
                     blankrow, blankrow, bpawnrow, lastrow]
                     
        self.moverules = {'R':[[0,7],[0,-7],[7,0],[-7,0]],
                          'B':[[7,7],[7,-7],[-7,7],[-7,-7]],
                          'Q':[[0,7],[0,-7],[7,0],[-7,0],
                              [7,7],[7,-7],[-7,7],[-7,-7]],
                          'K':[[0,1],[0,-1],[1,0],[-1,0],
                              [1,1],[1,-1],[-1,1],[-1,-1]],
                          'N':[[2,1],[2,-1],[-2,1],[-2,-1],
                              [1,2],[1,-2],[-1,2],[-1,-2]],
                          'pawnnocapture':[[0,1]],
                          'pawncapture':[[-1,1],[1,1]],
                          'pawnfirstmove':[[0,1],[0,2]]
                         }

    def printboard(self):
        for x in range(0,8):
            print self.board[7-x] 
           
    def checkifvalidmove(self, color, sourcex, sourcey, destx, desty):
        # if players piece not selected return False
        # if destination not in possible destinations return False
        # if move would result in own king in check return False
        # if piece moving is king
            # if any intermediate move is in check return False
        return True

    def checkifmoveispossibledest(self, sourcex, sourcey, destx, desty):
        # get the piece and color
        colorpiece = self.board[sourcey][sourcex]
        print colorpiece
        piececolor = colorpiece[0]
        piecetype  = colorpiece[1]
        print piececolor
        print piecetype
        potentialmoves = self.moverules[piecetype]
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
                        checkcolorpiece = self.board[checky][checkx]   
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
                    if checky >= 0 and checkx <= 7:
                        checkcolorpiece = self.board[checky][checkx]
                        if checkcolorpiece[0] != piececolor:
                            if checkx == destx and checky == desty:
                                return True
        
        return False
                         
if __name__ == '__main__':
    print "hello"
    chessboard = Chessboard()  
    chessboard.printboard()
    print chessboard.checkifmoveispossibledest(6,0,7,2)
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

if __name__ == '__main__':
    print "hello"
    chessboard = Chessboard()
    chessboard.printboard()
    print chessboard.moverules['B']
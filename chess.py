import pdb

class Chessboard(object):
   
   def __init__(self):
       self.tangerine = "And now a thousand years between"
       firstrow = ['WR','WN','WB','WQ','WK','WB','WN','WR']
       lastrow  = ['BR','BN','BB','BQ','BK','BB','BN','BR']
       blankrow = ['00','00','00','00','00','00','00','00']
       self.board = [firstrow, blankrow, blankrow, blankrow,
                     blankrow, blankrow, blankrow, lastrow]
                     
   def printboard(self):
       for x in range(0,8):
           print self.board[7-x]                  

if __name__ == '__main__':
    print "hello"
    chessboard = Chessboard()
    print chessboard.tangerine
    chessboard.printboard()
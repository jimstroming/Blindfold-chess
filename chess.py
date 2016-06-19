import pdb

class Chessboard(object):
   
   def __init__(self):
       self.tangerine = "And now a thousand years between"
       firstrow = ['WR','WN','WB','WQ','WK','WB','WN','WR']
       wpawnrow = ['WP','WP','WP','WP','WP','WP','WP','WP']
       blankrow = ['00','00','00','00','00','00','00','00']       
       bpawnrow = ['BP','BP','BP','BP','BP','BP','BP','BP']
       lastrow  = ['BR','BN','BB','BQ','BK','BB','BN','BR']
       self.board = [firstrow, wpawnrow, blankrow, blankrow,
                     blankrow, blankrow, bpawnrow, lastrow]
                     
   def printboard(self):
       for x in range(0,8):
           print self.board[7-x]                  

if __name__ == '__main__':
    print "hello"
    chessboard = Chessboard()
    print chessboard.tangerine
    chessboard.printboard()
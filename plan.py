""" Outline the general strategy

Main routine{

Initialize the board
Initialize the timers

While neither player resigned and reset not pressed

   while no valid move
      Select the piece
      Select the destination
      Check if valid move
      If not, increment the wrong move count

   Stop the timer
   Make the move
   if opponent now in check
       announce the check
   Start the other player timer
}
   
-------

Check if valid move{
    if players piece not selected return False
    if destination not in possible destinations return False
    if move would result in own king in check return False
    if piece moving is king
        if any intermediate move is in check return False
    return True
}
   
------

Check if move in list of possible destinations{

    for each jumpmove in potential moves
        if move on board and own piece not in space
            check destination
    for each rangemove in potential moves
        initialize distance to 1
        while True
            if move not on board break
            if own piece in space break
            check destination
            if opponent piece in space break
            
    
    if king 
        if castle conditions are valid
            check castle destinations
    if piece is pawn
        if pawn has not moved add 2 distance destinations
        if opponent last move was neighboring pawn
           check en passant destination
            
}   

------------

Make the move{
    if there is an opponent at the destination
        remove the piece
    move the piece to new location
    if pawn
        if at end of board promote
    if king
        if moved 2 castle    
    
}
  

------------------------------------------------

Let's make a simple one player mode, for practice.
The computer player will have perfect vision.  It will remember where every piece is
and will not play blind.

But it will not be very strategic.  It will only look N moves ahead,
analyzing what the best outcome is at the end of those N moves,
and choose the best option.
While as a regular chess opponent, this would be very bad,
as a blind chess opponent, it should be passable.

It will use the values
pawn   = 1
knight = 3
bishop = 3
rook   = 5
queen  = 9 
king   = 1000

----------

I think what we need at the heart is a recursive routine

findbestscore(board, whoseturninthegame, whosemoveintheanalysis, level)
    # whose turninthegame is who will move when the chosen turn is returned
    if level == 0:
        return calculatescoreandmove(whoteturninthegame, board)
    else:
        bestmove = []
        bestscore = None
        newmoveintheanalysis = opposite(whosemoveintheanalysis)
        for moves in possiblemoves:
            if movelegal(): newboard = move(board)
            score, move = findbestscore(newboard, whoseturninthegame, newmoveintheanalysis,level-1)
            if bestscore == score:
                bestturn.append(move)
            elif whoseturninthegame == whosemoveintheanalysis:
                if bestscore == None or score > bestscore:
                    bestmove = [move]
                    bestscore = score
            else:
                if bestscore == None or score < bestscore:
                    bestmove = [move]
                    bestscore = score
        return bestscore, bestmove  
"""

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
   

"""

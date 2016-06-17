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
   Start the other player timer
}
   
-------

Check if valid move{
    if players piece not selected return False
    create list of possible destinations
    if destination not in possible destinations return False
    if move would result in own king in check return False
    if piece moving is king
        if any intermediate move is in check return False
    return True
}
   
------

Create list of possible destinations{

    
    if king 
        if castle conditions are valid
            add castle destinations
    if piece is pawn
        if pawn has not moved add 2 distance destinations
        if opponent last move was neighboring pawn
           add en passant destination
            
}   
   

"""

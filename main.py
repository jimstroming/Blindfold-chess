from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from chess import ChessEngine

class BlindChessRoot(BoxLayout):
    
    def initialsetup(self):  # called at the beginning of the game
        print "DAGWOOD BOOT"
        self.createchessengine()
        self.purewhite   = ( 1,   1,  1, 1)
        self.brightwhite = (0.9,0.9,0.9, 1)
        self.lightgray   = (0.6,0.6,0.6, 1)
        self.darkgray    = (0.4,0.4,0.4, 1)   
        self.darkblack   = (0.1,0.1,0.1, 1)     
        self.pureblack   = ( 0,   0,  0, 1)
        self.ids["messageW"].text = 'Your Move'
        self.ids["messageB"].text = 'Black Move'
        self.blind = 1    # 1 means blind.  0 means show the pieces       
        self.updateboardui()
        self.whosemove = 'W' # white moves first
        self.setwidgetbackgroundcolors()
        self.sourcex = -1  # set the source and destination to none
        self.sourcey = -1 
        self.destx = -1
        self.desty = -1
        self.state = "looking for source"
        self.ids['clockW'].text = "10:00"
        self.ids['clockB'].text = "10:00"
        self.ids['messageW'].font_size = '30dp'
        self.ids['messageB'].font_size = '30dp'
        self.cancelcount = 0 # pressing cancel 3 times in a row toggles self.blind
        print "DAGWOOD50"
        Clock.schedule_interval(self.updateclocks, 1)
         
    def createchessengine(self):
        self.chessengine = ChessEngine() 
        
    def updateboardui(self): # update the board to match the engine
        for x in range(0,8):
            for y in range(0,8):
                stringid = "but"+str(x)+str(y)
                colorpiece = self.chessengine.getpiece(x,y)
                buttonid = "but"+str(x)+str(y)
                if self.blind == 0 and colorpiece[0] != '0':
                    if colorpiece[0] == 'B':
                        self.ids[buttonid].color = self.pureblack
                    else:
                        self.ids[buttonid].color = self.purewhite
                    self.ids[buttonid].text = colorpiece[1]
                else:
                    self.ids[buttonid].text = ''
                    
    def setallfontsonecolor(self, color):
        self.ids['clockW'].color = color
        self.ids['clockB'].color = color
        self.ids['mistakecountW'].color = color                
        self.ids['mistakecountB'].color = color                
        self.ids['moveW'].color = color
        self.ids['moveB'].color = color
        self.ids['cancelW'].color = color
        self.ids['cancelB'].color = color
        
    def restoreallfonts(self):
        almostblack = (0.2,0.2,0.2,1)
        almostwhite = (0.8,0.8,0.8,1)
        self.ids['clockW'].color = almostwhite
        self.ids['clockB'].color = almostblack
        self.ids['mistakecountW'].color = almostwhite                
        self.ids['mistakecountB'].color = almostblack              
        self.ids['moveW'].color = self.darkgray
        self.ids['moveB'].color = self.lightgray
        self.ids['cancelW'].color = self.darkgray
        self.ids['cancelB'].color = self.lightgray
        
                   
    def getboardcolor(self,x,y):
        if (y%2 == 0 and x%2 == 0) or (y%2 == 1 and x%2 == 1):
            return self.darkgray
        else:
            return self.lightgray  
            
    def updateclocks(self,dt):
        if self.whosemove == 'W':
            timestring = self.ids['clockW'].text
        else:
            timestring = self.ids['clockB'].text
            
        if timestring != '00:00':
            if timestring[4] != '0':
                timestring = timestring[0:4]+str(int(timestring[4])-1)
            else:
                if timestring[3] != '0':
                    timestring = timestring[0:3]+str(int(timestring[3])-1)+'9'
                else:
                    if timestring[1] != '0':
                        timestring = timestring[0]+str(int(timestring[1])-1)+timestring[2]+'59'
                    else:
                        timestring = str(int(timestring[0])-1)+'9:59'
        if self.whosemove == 'W':
            self.ids['clockW'].text = timestring
        else:
            self.ids['clockB'].text = timestring            
            
    def setwidgetbackgroundcolors(self):
        if self.whosemove == 'W': 
            blackcolor = self.darkgray
            whitecolor = self.brightwhite
        else:
            blackcolor = self.darkblack
            whitecolor = self.lightgray
        self.ids["moveB"].background_color = blackcolor
        self.ids["cancelB"].background_color = blackcolor
        self.ids["moveW"].background_color = whitecolor
        self.ids["cancelW"].background_color = whitecolor
        
    def resetsquarebackground(self,x,y):
        buttonid = buttonid = "but"+str(x)+str(y)
        self.ids[buttonid].background_color = self.getboardcolor(x,y)
        
    def increasemistakecount(self,color):
        # read the mistake count and convert to a number
        labelid = "mistakecount"+color 
        mistakecount = int(self.ids[labelid].text) 
        mistakecount += 1 # increment
        self.ids[labelid].text = str(mistakecount) # convert to a string and update
        
    def updatebothmessages(self, message, colortodraw):
        colorvalue = self.purewhite
        if colortodraw == 'B' : colorvalue = self.pureblack
        self.ids['messageW'].text = message
        self.ids['messageB'].text = message
        self.ids['messageW'].color = colorvalue
        self.ids['messageB'].color = colorvalue
        
    def updatemessage(self,message,colortoupdate,colortodraw):
        labelid = "message"+colortoupdate 
        self.ids[labelid].text = message
        if colortodraw == 'W':
            self.ids[labelid].color = self.purewhite
        else:
            self.ids[labelid].color = self.pureblack
    
    def resetaftermove(self):
        # reset both the cursors ui
        if self.sourcex != -1:
            self.resetsquarebackground(self.sourcex,self.sourcey)
        if self.destx != -1:    
            self.resetsquarebackground(self.destx,self.desty)
        # reset the source and destination
        self.sourcex = -1
        self.sourcey = -1
        self.destx = -1
        self.desty = -1
        # redraw the board
        self.updateboardui()
        # reset the message colors
        self.restoreallfonts()
        # set the state
        self.state = "looking for source"
        
    def checkforpawnpromotion(self, color):
        # check if we need to do pawn promotion
        # we will start with Queen
        # The order we will present the promotion options is
        # Q, N, R, B, 
        x,y = self.chessengine.checkforpawnpromotion(color)
        if x == -1: return False
        self.promotex = x # save pawn promotion coordinates for later
        self.promotey = y 
        # redraw the board
        self.updateboardui()
        self.updatemessage('Promote Queen?',color,color)
        self.state = "Promote Queen?"
        return True
        
    def promoteprawn(self, color, piece):
        self.chessengine.promotepawn(color,piece,self.promotex,self.promotey)
        self.movestring += piece 
        oppcolor = 'B'
        if color == 'B': oppcolor = 'W'
        if self.chessengine.checkifincheck(oppcolor,self.chessengine.board): self.movestring += '+'
        self.updatebothmessages(self.movestring,self.whosemove)
        if self.whosemove == 'B': # switch the players turn
            self.whosemove = 'W'
        else:
            self.whosemove = 'B'
        self.setwidgetbackgroundcolors()
        self.resetaftermove()
    

    def buttonpress(self, x, y):
        message = self.ids["messageB"].text
        if message == 'Press a Button to Start':
            self.initialsetup()
            return 
        self.cancelcount = 0            
        if self.state == "looking for source":
            buttonid = "but"+str(x)+str(y)     
            self.sourcex = x
            self.sourcey = y
            if self.whosemove == 'W':
                self.ids[buttonid].background_color = self.brightwhite
            else:
                self.ids[buttonid].background_color = self.darkblack
            self.state = "looking for destination"
            return
            
        if self.state == "looking for destination":
            if x == self.sourcex and y == self.sourcey:
                return    # can't have source be same as destination
        
            # check if we need to erase the previous destination source
            if self.destx != -1:
                self.resetsquarebackground(self.destx,self.desty)
             
            buttonid = "but"+str(x)+str(y)     
            self.destx = x
            self.desty = y
            if self.whosemove == 'W':
                self.ids[buttonid].background_color = self.purewhite
            else:
                self.ids[buttonid].background_color = self.pureblack
            return
        

    def movebuttonpress(self, color):
        print "DAGWOOD11 - movebuttonpress"
        message = self.ids["messageB"].text
        if message == 'Press a Button to Start':
            self.initialsetup()
            return
        self.cancelcount = 0            
        if self.whosemove == color:
            if 'Promote' in self.state: # need to execute the pawn promotion.
                piece = self.state[8]
                if piece == 'K': piece = 'N'  # Knight not Night
                self.promoteprawn(self.whosemove,piece)
                return    
            if self.state == "looking for source": # need a destination
                return
            if self.state == "looking for destination" and self.destx != -1:
                # check if the move is legal
                validmove = self.chessengine.checkifvalidmove(self.whosemove, self.sourcex, 
                                    self.sourcey, self.destx, self.desty)
                if validmove:  
                    self.movestring = self.chessengine.getmovenotation(self.sourcex, self.sourcey, 
                                    self.destx, self.desty) # get the move notation
                    self.chessengine.makevalidmove(self.sourcex, self.sourcey, 
                                    self.destx, self.desty)
                    if not self.checkforpawnpromotion(self.whosemove):
                        self.updatebothmessages(self.movestring,self.whosemove)
                        if self.whosemove == 'B': # switch the players turn
                            self.whosemove = 'W'
                        else:
                            self.whosemove = 'B'
                        self.setwidgetbackgroundcolors()
                        self.resetaftermove()
                        if self.chessengine.checkifincheck(self.whosemove,self.chessengine.board):
                            self.setallfontsonecolor((0,0,1,1)) # turn the fonts blue if in check
                else:
                    self.increasemistakecount(self.whosemove)
                    self.resetaftermove()
                    self.setallfontsonecolor((1,0,0,1)) # turn the fonts red
                return
                
    def cancelbuttonpress(self, color):
        message = self.ids["messageB"].text
        if message == 'Press a Button to Start':
            self.initialsetup()
            return
        self.cancelcount += 1
        if self.cancelcount == 3:
            self.blind = 1-self.blind
            self.cancelcount = 0            
        if self.whosemove == color:            
            if 'Promote' in self.state: # rejected the pawn promotion piece
                     # need to cycle to the next one
                if self.state == 'Promote Queen?':
                    message = 'Promote Knight?'
                elif self.state == 'Promote Knight?':
                    message = 'Promote Rook?'
                elif self.state == 'Promote Rook?':
                    message = 'Promote Bishop?' 
                elif self.state == 'Promote Bishop?':
                    message = 'Promote Queen?'   
                self.updatemessage(message,color,color)
                self.state = message
                return    
            self.resetaftermove()


class BlindChessApp(App):
    pass


if __name__ == '__main__':
    BlindChessApp().run()

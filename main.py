from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from chess import ChessEngine

class BlindChessRoot(BoxLayout):
    
    def initialsetup(self):  # called at the beginning of the game
        print "DAGWOOD BOOT"
        self.createchessengine()
        self.ids["messageW"].text = 'Your Move'
        self.ids["messageB"].text = 'Black Move'
        self.blind = 0    # 1 means blind.  0 means show the pieces       
        self.updateboardui()
        self.whosemove = 'W' # white moves first
        self.sourcex = -1  # set the source and destination to none
        self.sourcey = -1 
        self.destx = -1
        self.desty = -1
        self.state = "looking for source"
         
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
                        self.ids[buttonid].color = (0,0,0,1)
                    else:
                        self.ids[buttonid].color = (1,1,1,1)
                    self.ids[buttonid].text = colorpiece[1]
                else:
                    self.ids[buttonid].text = ''
                    
    def getboardcolor(self,x,y):
        if (y%2 == 0 and x%2 == 0) or (y%2 == 1 and x%2 == 1):
            return (0.4,0.4,0.4,1)
        else:
            return (0.6,0.6,0.6,1)    
            
    def resetsquarebackground(self,x,y):
        buttonid = buttonid = "but"+str(x)+str(y)
        self.ids[buttonid].background_color = self.getboardcolor(x,y)
        
    def increasemistakecount(self,color):
        # read the mistake count and convert to a number
        print "DAGWOOD1"
        labelid = "mistakecount"+color 
        mistakecount = int(self.ids[labelid].text) 
        mistakecount += 1 # increment
        print "DAGWOOD4"
        self.ids[labelid].text = str(mistakecount) # convert to a string and update
                    
    def buttonpress(self, x, y):
        message = self.ids["messageB"].text
        if message == 'Press Any Button to Start':
            self.initialsetup()
            return 
            
        if self.state == "looking for source":
            buttonid = "but"+str(x)+str(y)     
            self.sourcex = x
            self.sourcey = y
            if self.whosemove == 'W':
                self.ids[buttonid].background_color = (.9,.9,.9,1)
            else:
                self.ids[buttonid].background_color = (.1,.1,.1,1)
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
                self.ids[buttonid].background_color = (1,1,1,1)
            else:
                self.ids[buttonid].background_color = (0,0,0,1)
            return
        

    def movebuttonpress(self, color):
        message = self.ids["messageB"].text
        if message == 'Press Any Button to Start':
            self.initialsetup()
            return
        if self.whosemove == color:
            if self.state == "looking for source": # need a destination
                return
            if self.state == "looking for destination" and self.destx != -1:
                # check if the move is legal
                validmove = self.chessengine.checkifvalidmove(self.whosemove, self.sourcex, 
                                    self.sourcey, self.destx, self.desty)
                if validmove:  
                    self.chessengine.makevalidmove(self.sourcex, self.sourcey, 
                                    self.destx, self.desty)
                    if self.whosemove == 'B': # switch the players turn
                        self.whosemove = 'W'
                    else:
                        self.whosemove = 'B'
                else:
                    self.increasemistakecount(self.whosemove)
                # reset both the cursors ui
                self.resetsquarebackground(self.sourcex,self.sourcey)
                self.resetsquarebackground(self.destx,self.desty)
                # reset the source and destination
                self.sourcex = -1
                self.sourcey = -1
                self.destx = -1
                self.desty = -1
                # redraw the board
                self.updateboardui()
                # set the state
                self.state = "looking for source"
                return
                
    def cancelbuttonpress(self, color):
        message = self.ids["messageB"].text
        if message == 'Press Any Button to Start':
            self.initialsetup()
            return
        pass  # (STILL NEED TO WRITE)


class BlindChessApp(App):
    pass


if __name__ == '__main__':
    BlindChessApp().run()

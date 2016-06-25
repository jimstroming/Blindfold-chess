from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from chess import ChessEngine


class LightGreyButton(BoxLayout):   
    def changetext(self):
        self.ids["greybut"].text = 'R'
        self.ids["greybut"].background_color = (.3,0,0,1)
        self.ids["greybut"].color = (1,1,1,1)

class DarkGreyButton(BoxLayout):   
    pass

class BlindChessRoot(BoxLayout):
    
    def initialsetup(self):  # called at the beginning of the game
        self.createchessengine()
        self.ids["messageW"].text = 'Your Move'
        self.ids["messageB"].text = 'Black Move'
        self.blind = 0    # 1 means blind.  0 means show the pieces       
        self.updateboardui()
        self.whosmove = 'W' # white moves first
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
                if self.blind == 0:
                    if colorpiece[0] != '0':
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
                    
    def printwookie(self, parameter0, parameter1, parameter2):
        print "WOOKIE", parameter0, parameter1, parameter2
    def buttonpress(self, x, y):
        message = self.ids["messageB"].text
        if message == 'Press Any Button to Start':
            self.initialsetup()
            return 
            
        if self.state == "looking for source":
            # check if we need to erase the previous selected source
            if self.sourcex != -1:
                buttonid = buttonid = "but"+str(self.sourcex)+str(self.sourcey)
                self.ids[buttonid].background_color = self.getboardcolor(self.sourcex,self.sourcey)
             
            buttonid = "but"+str(x)+str(y)     
            self.sourcex = x
            self.sourcey = y
            if self.whosmove == 'W':
                self.ids[buttonid].background_color = (.9,.9,.9,1)
            else:
                self.ids[buttonid].background_color = (.1,.1,.1,1)

    def movebuttonpress(self, color):
        message = self.ids["messageB"].text
        if message == 'Press Any Button to Start':
            self.initialsetup()
            return
        if self.whosmove == color:
            if self.state == "looking for source" and self.sourcex != -1:
                self.state = "looking for destination"
                return
                
    def cancelbuttonpress(self, color):
        message = self.ids["messageB"].text
        if message == 'Press Any Button to Start':
            self.initialsetup()
            return
        pass


class BlindChessApp(App):
    pass


if __name__ == '__main__':
    BlindChessApp().run()

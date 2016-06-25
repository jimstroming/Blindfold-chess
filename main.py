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
    gamesetup = NumericProperty(0)  # 0 means we need to setup the game
    
    
    def initialsetup(self):  # called at the beginning of the game
        createchessengine()
    def createchessengine(self):
        self.chessengine = ChessEngine()    
    def printwookie(self, parameter0, parameter1, parameter2):
        print "WOOKIE", parameter0, parameter1, parameter2
    def buttonpress(self, x, y):
        self.ids["but"+str(x)+str(y)].text = 'S'
        self.ids["but"+str(x)+str(y)].background_color = (0,.3,0,1)
        self.ids["but"+str(x)+str(y)].color = (1,1,1,1)
    def movebuttonpress(self, color):
        pass
    def cancelbuttonpress(self, color):
        pass


class BlindChessApp(App):
    pass


if __name__ == '__main__':
    BlindChessApp().run()

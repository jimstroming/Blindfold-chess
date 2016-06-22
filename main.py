from random import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Rectangle, Line, PushMatrix, PopMatrix
from kivy.graphics import Rotate
from kivy.core.window import Window
from chess import ChessEngine

class BlindChessWidget(Widget):

    def drawboard(self):
        color = (1,1,1)  # set color to white
        with self.canvas:
            Color(*color)
            PushMatrix()
            Rotate(angle=0)
            self.displaywidth = Window.size[0]
            self.bottomboard = self.displaywidth*2/7
            self.squarewidth = int(self.displaywidth/8)
            d = self.squarewidth
            component = 0.45;
            for y in range(0,8):
                for x in range(0,8):
                    color = (component, component, component)
                    Color(*color)
                    Rectangle(pos=(x*d, self.bottomboard+y*d), size=(d, d))
                    component = 1-component
                component = 1-component
            PopMatrix()

    def setchessengine(self, chessengine):
        self.chessengine = chessengine
    

    def drawpiece(self,colorpiece,x,y):
        colorchar = colorpiece[0]
        color = (0,0,0)
        if colorchar == 'W': color = (1,1,1)
        print "DAGWOOD2"
        with self.canvas:
            Color(*color)
            labx = x*self.squarewidth
            laby = self.bottomboard + y*self.squarewidth
            testlabel = Label(text='K',pos=(labx,laby))

             

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))


class BlindChessApp(App):

    def build(self):
        parent = Widget() 
        self.chessboard = BlindChessWidget()
        #startbtn = Button(text='Start')
        #startbtn.bind(on_release=self.draw_board)
        parent.add_widget(self.chessboard)
        #parent.add_widget(startbtn)    
        buttonwidth = Window.size[0]/7
        whitechoosepiece = Button(x=Window.size[0]*2/7,y=0,height=buttonwidth,width=buttonwidth)
        whitechoosepiece.bind(on_release=self.enter_piece)
        parent.add_widget(whitechoosepiece)
        blackchoosepiece = Button(x=Window.size[0]*2/7,y=Window.size[1]-buttonwidth,height=buttonwidth,width=buttonwidth)
        blackchoosepiece.bind(on_release=self.enter_piece)
        parent.add_widget(blackchoosepiece)
        self.numberlives = 0
        self.blindgame = False # False means show the pieces
                               # True means don't shoe the pieces
        self.chessboard.drawboard()
        self.chesseng = ChessEngine()
        self.chessboard.setchessengine(self.chesseng) # pass the chess engine to the widget
        return parent

    def clear_canvas(self, obj):
        self.chessboard.canvas.clear()
        
    def draw_board(self, obj):
        self.chessboard.drawboard()
        
    def enter_piece(self, obj):
        print "DAGWOOD"
        self.chessboard.drawpiece('WK',1,2)
        
    def enter_destination(self, obj):    
        return

if __name__ == '__main__':
    BlindChessApp().run()
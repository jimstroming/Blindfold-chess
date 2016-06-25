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
        color = (1,0,1)  # set color to white
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
        
    def createcursor(self,color):
        with self.canvas:
            Color(*color)
            print "HULK" , color
            toprect   = Rectangle(size=(self.squarewidth,self.squarewidth*.1))
            botrect   = Rectangle(size=(self.squarewidth,self.squarewidth*.1))
            leftrect  = Rectangle(size=(self.squarewidth*.1,self.squarewidth))
            rightrect = Rectangle(size=(self.squarewidth*.1,self.squarewidth))
            toprect.pos = (100,300)
            botrect.pos = (100,300)
            leftrect.pos = (100,300)
            rightrect.pos = (100,300)
            cursor = [toprect, botrect, leftrect, rightrect]
            print "AHULK"
            label = Label(text='A', pos=(100,300))
            print "AHULK done"
        return cursor,label

    def createlabel(self,color,x,y):
        with self.canvas:
            Color(*color)
            print "SHEHULK", color
            label = Label(text='S',pos=(x,y))
            print "SHEHULK DONE"

        return label    

    def drawpiece(self,colorpiece,x,y):
        colorchar = colorpiece[0]
        color = (0,0,0)
        #if colorchar == 'W': color = (1,1,1)
        print "DAGWOOD2"
        with self.canvas:
            Color(*color)
            labx = x*self.squarewidth
            laby = self.bottomboard + y*self.squarewidth
            black = (0,0,0)
            Color(*black)
            testlabel = self.createlabel((0,0,0),labx,laby)
            #testlabel.pos = (400,400) # changing label
            #testlabel.text = 'Q'
            # I will keep one label in each square
            # then we will update the squares to match the chessboard.
            # similarly, need rectangles for the square borders
            # to highlight the square when selected.
            botrect = Rectangle(size=(self.squarewidth,self.squarewidth*.1))
            botrect.pos = (self.squarewidth*x,self.bottomboard+self.squarewidth*y)
            toprect = Rectangle(size=(self.squarewidth,self.squarewidth*.1))
            toprect.pos = (self.squarewidth*x,self.bottomboard+self.squarewidth*(y+0.9))
            toprect.pos = (-100,100)



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
        self.chessboard.createcursor((0.4,0,0))
        self.chessboard.createlabel((0.8,0,0),400,400)
        self.chessboard.drawpiece('BR',3,4)
        
    def enter_destination(self, obj):    
        return

if __name__ == '__main__':
    BlindChessApp().run()
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Rectangle, Line, PushMatrix, PopMatrix
from kivy.graphics import Rotate
from kivy.core.window import Window

class BlindChessWidget(Widget):

    def drawboard(self):
        color = (1,1,1)  # set color to white
        with self.canvas:
            Color(*color)
            PushMatrix()
            Rotate(angle=0)
            displaywidth = Window.size[0]
            bottomboard = displaywidth*2/7
            squarewidth = int(displaywidth/8)
            d = squarewidth
            component = 0;
            for y in range(0,8):
                for x in range(0,8):
                    color = (component, component, component)
                    Color(*color)
                    Rectangle(pos=(x*d, bottomboard+y*d), size=(d, d))
                    component = 1-component
                component = 1-component
            PopMatrix()


    

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
        self.painter = BlindChessWidget()
        startbtn = Button(text='Start')
        startbtn.bind(on_release=self.draw_board)
        parent.add_widget(self.painter)
        parent.add_widget(startbtn)    
        buttonwidth = Window.size[0]/7
        whitechoosepiece = Button(x=Window.size[0]*2/7,y=0,height=buttonwidth,width=buttonwidth)
        whitechoosepiece.bind(on_release=self.enter_piece)
        whitemove = Button(x=Window.size[0]*4/7,y=0,height=buttonwidth,width=buttonwidth)
        whitemove.bind(on_release=self.enter_destination)
        parent.add_widget(whitechoosepiece)
        parent.add_widget(whitemove)
        blackchoosepiece = Button(x=Window.size[0]*2/7,y=Window.size[1]-buttonwidth,height=buttonwidth,width=buttonwidth)
        blackchoosepiece.bind(on_release=self.enter_piece)
        blackmove = Button(x=Window.size[0]*4/7,y=Window.size[1]-buttonwidth,height=buttonwidth,width=buttonwidth)
        blackmove.bind(on_release=self.enter_destination)
        parent.add_widget(blackchoosepiece)
        parent.add_widget(blackmove)

        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        
    def draw_board(self, obj):
        self.painter.drawboard()
        
    def enter_piece(self, obj):
        return
        
    def enter_destination(self, obj):    
        return

if __name__ == '__main__':
    BlindChessApp().run()
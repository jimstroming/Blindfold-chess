from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line


class BlindChessWidget(Widget):

    def drawboard(self):
        color = (1,1,1)  # set color to white
        with self.canvas:
            Color(*color, mode='hsv')
            displaywidth = 700
            bottomboard = 200
            squarewidth = int(displaywidth/8)
            d = squarewidth
            Ellipse(pos=(0,bottomboard), size=(d, d))

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class BlindChessApp(App):

    def build(self):
        parent = Widget()
        self.painter = BlindChessWidget()
        startbtn = Button(text='Start')
        startbtn.bind(on_release=self.draw_board)
        parent.add_widget(self.painter)
        parent.add_widget(startbtn)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        
    def draw_board(self, obj):
        self.painter.drawboard()


if __name__ == '__main__':
    BlindChessApp().run()
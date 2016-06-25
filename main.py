from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class LightGreyButton(BoxLayout):   
    def changetext(self):
        self.ids["greybut"].text = 'R'
        self.ids["greybut"].background_color = (.3,0,0,1)
        self.ids["greybut"].color = (1,1,1,1)

class DarkGreyButton(BoxLayout):   
    pass

class BlindChessRoot(BoxLayout):
    def printwookie(self, parameter0, parameter1, parameter2):
        print "WOOKIE", parameter0, parameter1, parameter2
    def buttonpress(self, x, y):
        self.ids["but"+str(x)+str(y)].text = 'S'
        self.ids["but"+str(x)+str(y)].background_color = (0,.3,0,1)
        self.ids["but"+str(x)+str(y)].color = (1,1,1,1)
    


class BlindChessApp(App):
    pass


if __name__ == '__main__':
    BlindChessApp().run()

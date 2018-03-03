from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import StringProperty

class TextWidget(Widget):
    pass

class TestApp(App):

    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'greeting'

    def build(self):
        return TextWidget()

if __name__ == '__main__':
    TestApp().run()

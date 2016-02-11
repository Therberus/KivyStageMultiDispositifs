__version__ = '1.0'

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty, NumericProperty,StringProperty
import pyjsonrpc
import random
import demjson as json

class Tablette(Widget):
    
    http_client = pyjsonrpc.HttpClient(
        url = "http://10.42.0.1:8080"
    )
    TrueColor = ListProperty([0,0,0])
    Status = StringProperty("Disconnected")
    
    def appairage(self):
        reponse = self.http_client.call("appairage","10.42.0.1","8080",self.Status)
        reponse_tab = json.decode(reponse)
        self.Status = reponse_tab["status"]
        if self.Status=="Connected":
            r = float(reponse_tab["color"]["r"])
            g = float(reponse_tab["color"]["g"])
            b = float(reponse_tab["color"]["b"])
            self.TrueColor = [r,g,b]

class TabletteclientApp(App):
    
    def build(self):
        tablette = Tablette()
        tablette.appairage()
        return tablette
        

if __name__ == '__main__':
    TabletteclientApp().run()
        

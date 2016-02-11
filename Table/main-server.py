from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty, NumericProperty,StringProperty
import pyjsonrpc
import threading
import random
    

class Joueur(Widget):
    
    TrueColor = ListProperty([1,1,1])
    Adresse = StringProperty("")
    Port = NumericProperty(0)
    ID = NumericProperty(0)

class TabletteApp(App):
    
    IpTable = "10.42.0.1"
    PortTable = "8080"
    tablette = ObjectProperty(None)
    nbClient = NumericProperty(0)

    def build(self):
        self.tablette = GridLayout(cols=3, rows=2)
        return self.tablette
        
    def appairage(self, ip, port, status):
        if status != "Connected":
            if self.nbClient < 6:
                self.nbClient += 1
                joueur = Joueur()
                r = random.random()
                g = random.random()
                b = random.random()
                joueur.TrueColor = [r,g,b]
                joueur.Adresse = ip
                joueur.Port = port
                joueur.ID = self.nbClient
                self.tablette.add_widget(joueur)
                print self.nbClient
                return '{"status":"Connected","color":{"r":"'+str(r)+'","g":"'+str(g)+'","b":"'+str(b)+'"}'+'}'
            else:
                return '{"status":"Refused","message":"too many clients"}'
        else: 
            return '{"status":"Connected","message":"alredy connected"}'
        
        
class RequestHandler(pyjsonrpc.HttpRequestHandler):
    
    app = TabletteApp()
    t1 = threading.Thread(target=app.run)
    t1.daemon = True
    t1.start()
    
    @pyjsonrpc.rpcmethod
    def appairage(self,ip,port,status):
        message = self.app.appairage(ip,port,status)
        return message
        
if __name__ == '__main__':
    http_server = pyjsonrpc.ThreadingHttpServer(
        server_address = ('10.42.0.1', 8080),
        RequestHandlerClass = RequestHandler
    )
    print "Starting HTTP server ..."
    print "URL: http://10.42.0.1:8080"
    http_server.serve_forever()
        

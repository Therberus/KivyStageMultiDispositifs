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
    
def randomColor():
    return [random.random(), random.random(), random.random()]

class Joueur(Widget):
    
    TrueColor = ListProperty([1,1,1])
    Adresse = StringProperty("")
    Port = StringProperty("")
    ID = NumericProperty(0)

    http_client = ObjectProperty(None)
    Status = ObjectProperty(None)

    def createHttpClient(self):
        print self.Adresse
        print self.Port
        self.http_client = pyjsonrpc.HttpClient(
            url = "http://"+self.Adresse.__str__()+":"+self.Port.__str__()
        )
        self.Status = StringProperty("Disconnected")

    def on_touch_up(self, touch):
        print("My address is : ", self.Adresse)
        self.TrueColor = randomColor()
        print(self.http_client.colorUpdate(self.TrueColor))


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
                joueur.TrueColor = randomColor()
                joueur.Adresse = "127.0.0.2"
                joueur.Port = port
                joueur.ID = self.nbClient
                joueur.createHttpClient()

                self.tablette.add_widget(joueur)
                #print self.nbClient
                return '{"status":"Connected","color":{"r":"'+str(joueur.TrueColor[0])+'","g":"'+str(joueur.TrueColor[1])+'","b":"'+str(joueur.TrueColor[2])+'"}'+'}'
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
    def appairage(self,port,status):
        message = self.app.appairage(self.client_address[0], port, status)
        return message
        
if __name__ == '__main__':
    http_server = pyjsonrpc.ThreadingHttpServer(
        server_address = ('localhost', 8080),
        RequestHandlerClass = RequestHandler
    )
    #print "Starting HTTP server ..."
    #print "URL: http://10.42.0.1:8080"
    http_server.serve_forever()
        

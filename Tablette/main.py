__version__ = '1.0'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty, NumericProperty,StringProperty

import random
import pyjsonrpc
import threading
import demjson as json
import socket

TableURL = "http://10.42.0.1:8080"

class Tablette(Widget):
    
    http_client = pyjsonrpc.HttpClient(
        url = TableURL
    )
    TrueColor = ListProperty([0,0,0])
    Status = StringProperty("Disconnected")
    
    def appairage(self, adresse):
        reponse = self.http_client.appairage(adresse)
        reponse_tab = json.decode(reponse)
        self.Status = reponse_tab["status"]
        if self.Status=="Connected":
            r = float(reponse_tab["color"]["r"])
            g = float(reponse_tab["color"]["g"])
            b = float(reponse_tab["color"]["b"])
            self.TrueColor = [r,g,b]

    def setColor(self, color):
        self.TrueColor = color

    def finish(self):
        self.http_client.goodbye()

class TabletteclientApp(App):
    tablette = None
    server = None
    adresse = None

    def build(self):
        self.tablette = Tablette()
        self.tablette.appairage(self.adresse)
        return self.tablette

    def on_start(self):
        hostName = socket.gethostname()
        ip = socket.gethostbyname_ex(hostName)
        self.adresse = ip[2][0]

        self.server = pyjsonrpc.ThreadingHttpServer(
                server_address = (self.adresse, 8080),
                RequestHandlerClass = RequestHandler
        )
        self.server.RequestHandlerClass.app = self
        t1 = threading.Thread(target=self.server.serve_forever)
        t1.daemon = True
        t1.start()

    def on_stop(self):
        print('Closing')
        self.tablette.finish()

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    app = None

    @pyjsonrpc.rpcmethod
    def ping(self):
        print "Ping"
        return "Pong"

    @pyjsonrpc.rpcmethod
    def colorUpdate(self, color):
        print("ColorUpdate")
        self.app.tablette.setColor(color)

if __name__ == '__main__':
    TabletteclientApp().run()

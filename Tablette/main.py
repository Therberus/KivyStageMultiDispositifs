__version__ = '1.0'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty, NumericProperty,StringProperty
import pyjsonrpc
import threading
import demjson as json

class Tablette(Widget):
    
    http_client = pyjsonrpc.HttpClient(
        url = "http://localhost:8080"
    )
    TrueColor = ListProperty([0,0,0])
    Status = StringProperty("Disconnected")
    
    def appairage(self):
        reponse = self.http_client.call("appairage","8080",self.Status)
        reponse_tab = json.decode(reponse)
        self.Status = reponse_tab["status"]
        if self.Status=="Connected":
            r = float(reponse_tab["color"]["r"])
            g = float(reponse_tab["color"]["g"])
            b = float(reponse_tab["color"]["b"])
            self.TrueColor = [r,g,b]

    def setColor(self, color):
        self.TrueColor = color

class TabletteclientApp(App):
    tablette = None

    def build(self):
        self.tablette = Tablette()
        self.tablette.appairage()
        return self.tablette

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    app = TabletteclientApp()
    t1 = threading.Thread(target=app.run)
    t1.daemon = True
    t1.start()

    @pyjsonrpc.rpcmethod
    def ping(self):
        print "Ping"
        return "Pong"

    @pyjsonrpc.rpcmethod
    def colorUpdate(self, color):
        self.app.tablette.setColor(color)

if __name__ == '__main__':
    http_server = pyjsonrpc.ThreadingHttpServer(
            server_address = ('127.0.0.2', 8080),
            RequestHandlerClass = RequestHandler
    )
    #print "Starting HTTP server ..."
    #print "URL: http://10.42.0.1:8080"
    http_server.serve_forever()


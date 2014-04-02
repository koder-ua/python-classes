import os
import cherrypy

class HelloWorld(object):

    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    def list(self):
        return os.listdir("C:\\")
    
h = HelloWorld()
cherrypy.quickstart(h)

# localhost:8080/list

h.index()

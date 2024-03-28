#qpy:webapp:Almacen de Carve
#qpy://127.0.0.1:8080/
"""
This is a sample for qpython webapp
"""
from bottle import Bottle
from BottleSessions import BottleSessions

from bottle.ext.websocket import GeventWebSocketServer

import pymvu_websocket

app = Bottle()

######### BUILT-IN ROUTERS ###############
@app.route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

pymvu_websocket.rutearModulo(app, '/sockets')

######### WEBAPP ROUTERS ###############

# app.route('/', method='GET')(home)
# app.route('/__exit', method=['GET','HEAD'])(__exit)
# app.route('/assets/<filepath:path>', method='GET')(server_static)

try:

    # Get the IP address of the hostname
    direccion_ip = "127.0.0.1"
    puerto = 8081

    backing_params = {
        'cache_type': 'SimpleCache', 
        #'host': direccion_ip,
        #'password': None
    }

    BottleSessions(app, session_backing = backing_params, session_secure = False, session_expire = 600 )
    app.run(host = direccion_ip, port = puerto, reloader=False, server = GeventWebSocketServer)
except Exception as ex:
    errs = "Exception: %s" % repr(ex)
    print(errs)




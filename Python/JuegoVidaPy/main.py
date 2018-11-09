#-*-coding:utf8;-*-
#qpy:3
#qpy:webapp:JuegoVida
#qpy:fullscreen
#qpy://localhost:8080/
"""
This is a sample for qpython webapp
"""
from bottle import route, run, static_file, response
import os
WEB_ROOT = os.path.dirname (os.path.abspath (__file__))
#("/storage/sdcard0/com.hipipal.qpyplus/projects3/JuegoVida")


@route('/')
def raiz():
    return static_file("index.html", root=WEB_ROOT)

@route('/js/<filepath:path>')
def server_static_js(filepath):
    response.set_header("Cache-control","no-cache")
    response.set_header("Expires","0")
    return static_file(filepath, root=WEB_ROOT+"/js")

run(host='localhost', port=8080)

from flask import Flask, redirect, url_for, request, Response, render_template
import reporte
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/construir_grafico',methods = ['POST'])
def construir_grafico():
    #print("Inicia proceso ")
    entrada = request.get_json()
    salida = reporte.construir_grafico(entrada)
    return Response( salida.getvalue(), mimetype = 'image/png' )

if __name__ == '__main__':
   app.run(port = 8003, debug = True)

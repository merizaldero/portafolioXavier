from __future__ import with_statement
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_xmlrpcre.xmlrpcre import XMLRPCHandler, Fault
import currency
import region_validator
import xpd_os_session

# configuration

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
HOST = '0.0.0.0'
PORT = 80

ENCABEZADOS_INTERES = ["X-Forwarded-For", "X-SecondLife-Shard", "X-SecondLife-Region", "X-SecondLife-Owner-Name",
    "X-SecondLife-Owner-Key", "X-SecondLife-Object-Name","X-SecondLife-Object-Key","X-SecondLife-Local-Velocity",
    "X-SecondLife-Local-Rotation","X-SecondLife-Local-Position"
    ]

# create our little application :)
app = Flask(__name__)
# app.secret_key = SECRET_KEY
app.debug = DEBUG

@app.errorhandler(404)
def error404(er):
    print("404\n"+ str(er))
    return "404 Recurso no existe", 404

@app.before_request
def before_request_callback():
    #print(request.get_data())
    pass

@app.route('/')
def index():
    if DEBUG == False:
        return {"cod":"0", "message":"Servidor Funcional"}
    else:
        stats = currency.obtener_stats()
        stats['cod'] = '0'
        stats['message'] = "Servidor Funcional"
        return stats

@app.route('/welcome')
def welcome():
   return render_template('welcome.html')

VIDEOS= [
    {'label':'Caballeros del Zodiaco', 'url':'https://www.youtube.com/embed/Lxkz8j_WqDM'},
    {'label':'Festival de los Robots', 'url':'https://www.youtube.com/embed/pGavB2qaajo'},
    {'label':'Pokemon', 'url':'https://www.youtube.com/embed/U8LlGHIXD14'},
    {'label':'de Mazinger a Mazinkaiser', 'url':'https://www.youtube.com/embed/O8YM8ByMvmA'},
    {'label':'Transformers: The Touch', 'url':'https://www.youtube.com/embed/1nktv5EprGg'},
    {'label':'Superman', 'url':'https://www.youtube.com/embed/ebXB0lBoaQ0'},
    {'label':'Batman', 'url':'https://www.youtube.com/embed/W2mD8nmA_Es'},
    {'label':'Flash', 'url':'https://www.youtube.com/embed/bYTM2Ws1f-Y'},
    {'label':'Evolucion de Canciones de Caricaturas', 'url':'https://www.youtube.com/embed/evJaa6xcr3Y'},
    {'label':'Caricaturas de los 80s', 'url':'https://www.youtube.com/embed/3J6iieVfw-w'},
]

@app.route('/whoiam')
def whoiam():
    return render_template('whoiam.html', encabezados_interes = ENCABEZADOS_INTERES,argumentos = request.args, encabezados = request.args, url = request.url, formulario = request.form, remote_addr = request.remote_addr, remote_user = request.remote_user, user_agent = request.user_agent.string)

@app.route('/requestSession',methods = ["POST",])
def request_session():
    return xpd_os_session.crear_sesion( request.form.get('request_id',''), request.form.get('userid',''), request.form.get('username','') )

@app.route('/home/<request_id>/<session_id>')
def home_user(request_id, session_id):
    try:
        sesion = xpd_os_session.validar_sesion(request_id, session_id)
        return render_template('home.html', sesion = sesion)
    except Exception as ex:
        return "No Autorizado", 401
    finally:
        pass


@app.route('/videos')
def lista_videos():
   return render_template('videos.html', videos = VIDEOS )

VIDEOS_EJERCICIO = [
    {'label':'Rutina Casera', 'url':'https://www.youtube.com/embed/Z8R5n1oG660'},
    {'label':'(1) Nado Mariposa en tierra', 'url':'https://www.youtube.com/embed/eI0NjCB_ATs'},
    {'label':'(2) Nado Pecho en tierra', 'url':'https://www.youtube.com/embed/wvUIg4YTV38'},
    {'label':'(3) Nado Dorso en casa', 'url':'https://www.youtube.com/embed/1THm9e3wcEY'},
    {'label':'(4) Nado CROL en casa', 'url':'https://www.youtube.com/embed/Gzjf5D4Yxpg'},
    {'label':'(5) Ejercicios nado CROL', 'url':'https://www.youtube.com/embed/lMU9NjKt8ac'},
    {'label':'(6) Ejercicios Pecho Simulacion', 'url':'https://www.youtube.com/embed/Ae8KiFa-dM0'},
    {'label':'(7) Ejercicios Nado dorso', 'url':'https://www.youtube.com/embed/JWLFgHfz-u8'},
    {'label':'(8) Ejercicios Nado mariposa', 'url':'https://www.youtube.com/embed/VJ3BUaV_te4'},
    {'label':'(9) Ejercicios CROL', 'url':'https://www.youtube.com/embed/uFoQ7yNBzFQ'},

]

@app.route('/videosejercicio')
def lista_videos_ejercicios():
   return render_template('videos.html', videos = VIDEOS_EJERCICIO )

api = XMLRPCHandler('economy')
api.connect(app, '/economy/currency.php')
#api.connect(app, '/currency.php')

@api.register_function
def getCurrencyQuote( parametros ):

    print('getCurrencyQuote ' + str(parametros))

    agentid   = parametros['agentId']
    sessionid = parametros['secureSessionId']
    amount    = parametros['currencyBuy']

    respuesta = {'success':False, 'errorMessage': __name__ + 'Servicio no disponible', 'errorURI':' '}

    confirmvalue = "123456789";
    estimated_cost = currency.get_costo_estimado(amount)
    user_id = region_validator.validar_session(agentid, sessionid)

    if user_id == agentid :
        respuesta = {'success':True,
                    'currency':{'estimatedCost' : estimated_cost, 'currencyBuy': amount },
                    'confirm': confirmvalue }
    else:
        respuesta = {'success':False, 'errorMessage': "Unable to Authenticate\n\nClick URL for more info. 002", 'errorURI':' '}
    print('getCurrencyQuote ' + str(respuesta))
    return respuesta

@api.register_function
def buyCurrency(parametros):
    print('buyCurrency ' + str(parametros))

    agentid   = parametros['agentId']
    #regionid  = parametros['RegionID']
    sessionid = parametros['secureSessionId']
    amount    = parametros['currencyBuy']
    ipAddress = request.remote_addr

    respuesta = {'success':False, 'errorMessage': __name__ + 'Servicio no disponible', 'errorURI':' '}

    user_id = region_validator.validar_session(agentid, sessionid)

    if user_id == agentid :
        #costo = currency.get_costo_estimado(amount)
        try:
            resultado = currency.comprar( agentid, amount, ipAddress )
            if DEBUG == True:
                print("COMPRA EXITOSA")
            #TODO notificar a usuario
            region_validator.actualizar_saldo_simulador(agentid)
            respuesta = { 'success':True }
        except Exception as ex:
            if DEBUG == True:
                print("ERROR EN COMPRA: " +str(ex))
            respuesta = { 'success':False, 'errorMessage': str(ex) , 'errorURI':' '}
    else:
        respuesta = { 'success':False, 'errorMessage': "Unable to Authenticate\n\nClick URL for more info. 003", 'errorURI':' '}
    print('buyCurrency ' + str(respuesta))
    return respuesta

@api.register_function
def simulatorUserBalanceRequest(parametros):
    print('simulatorUserBalanceRequest ' + str(parametros))

    agentid        = parametros['agentId']
    sessionid      = parametros['secureSessionId']
    regionid       = parametros['RegionID']
    secret         = parametros['secret']
    currencySecret = parametros['currencySecret']

    respuesta = {'success':False, 'errorMessage': __name__ + 'Servicio no disponible', 'errorURI':' '}

    region_id = regionid # region_validator.validar_region(regionid, secret)

    if region_id == regionid:
        user_id = agentid #region_validator.validar_session(agentid, sessionid, False, regionid)
        if user_id == agentid :
            try:
                resultado = currency.crear_cuenta_si_no_existe( agentid )
                respuesta = {   'success': True,
                                'agentId': agentid,
                                'funds': int (resultado['saldo'])
                            }
            except Exception as ex:
                respuesta = { 'success':False, 'errorMessage': str(ex) , 'errorURI':' '}
        else:
            respuesta = { 'success':False, 'errorMessage': "Unable to Authenticate\n\nClick URL for more info. 003", 'errorURI':' '}
    else:
        respuesta = { 'success':False, 'errorMessage': "This region is not authorized to check your balance. Money operations may be unavailable", 'errorURI':' '}

    print('simulatorUserBalanceRequest ' + str(respuesta))
    return respuesta

@api.register_function
def regionMoveMoney(req):
    print('regionMoveMoney ' + str(req))

    agentid                = req['agentId']
    sessionid              = req['secureSessionId']
    regionid               = req['regionId']
    secret                 = req['secret']
    currencySecret         = req['currencySecret']
    destid                 = req['destId']
    cash                   = req['cash']
    aggregatePermInventory = req['aggregatePermInventory']
    aggregatePermNextOwner = req['aggregatePermNextOwner']
    flags                  = req['flags']
    transactiontype        = req['transactionType']
    description            = req['description']
    ipAddress              = request.remote_addr

    respuesta = {'success':False, 'errorMessage': __name__ + 'Servicio no disponible', 'errorURI':' '}

    region_id = region_validator.validar_region(regionid, secret)
    if region_id == regionid :
        user_id = region_validator.validar_session(agentid, sessionid, False, regionid)
        if user_id == agentid :

            if destid == '00000000-0000-0000-0000-000000000000':
                destid = currency.get_minteador()

            if transactiontype == 1101:
                region_validator.user_alert(agentid, "00000000-0000-0000-0000-000000000000", "You paid L$" + cash + " to upload.")
                description="Asset upload fee"
            elif transactiontype in [ 5001, 5008, 2 ]:
                destName = region_validator.agent_name(destid)
                sourceName = region_validator.agent_name(agentid)
                region_validator.user_alert( agentid, "00000000-0000-0000-0000-000000000000", "You paid " + destName + " L$" + cash )
                region_validator.user_alert( destid, "00000000-0000-0000-0000-000000000000", sourceName + " paid you L$" + cash)
                if transactiontype == 5001:
                    description="Gift"
            elif transactiontype == 0:
                if destid == currency.get_minteador():
                    region_validator.user_alert( agentid, "00000000-0000-0000-0000-000000000000", "You paid L$" + cash + " for a parcel of land.");
                else:
                    destName = region_validator.agent_name(destid)
                    sourceName = region_validator.agent_name(agentid)
                    region_validator.user_alert( agentid, "00000000-0000-0000-0000-000000000000", "You paid " + destName + " L$" + cash +" for a parcel of land.")
                    region_validator.user_alert( destid, "00000000-0000-0000-0000-000000000000", sourceName + " paid you L$" + cash + " for a parcel of land")
                description="Land purchase"

            try:
                resultado = currency.transferir( agentid, destid, cash, ipAddress )
                cuenta1 = currency.obtener_cuenta(agentid)
                cuenta2 = currency.obtener_cuenta(destid)
                respuesta = { 'success':True,
                            'agentId': agentid ,
                            'funds': cuenta1['saldo'],
                            'funds2' : cuenta2['saldo'],
                            'currencySecret': ' '}
            except Exception as ex:
                respuesta = { 'success':False, 'errorMessage': str(ex) , 'errorURI':' '}

        else:
            respuesta = { 'success':False, 'errorMessage': "Unable to Authenticate\n\nClick URL for more info. 004", 'errorURI':' '}
    else:
        respuesta = { 'success':False, 'errorMessage': "This region is not authorized to manage your money. Money operations may be unavailable", 'errorURI':' '}

    print('regionMoveMoney ' + str(respuesta))
    return respuesta

@api.register_function
def simulatorClaimUserRequest(req):
    print('simulatorClaimUserRequest ' + str(req))

    agentid   = req['agentId']
    sessionid = req['secureSessionId']
    regionid  = req['RegionID']
    secret    = req['secret']

    respuesta = {'success':False, 'errorMessage': __name__ + 'Servicio no disponible', 'errorURI':' '}

    region_id = region_validator.validar_region(regionid, secret)
    if region_id == regionid :
        user_id = region_validator.validar_session(agentid, sessionid, False, regionid)
        if user_id == agentid :
            region_validator.actualizar_region(agentid, sessionid, regionid)
        else:
            respuesta = { 'success':False, 'errorMessage': "Unable to Authenticate\n\nClick URL for more info. 001", 'errorURI':' '}
    else:
        respuesta = { 'success':False, 'errorMessage': "This region is not authorized to manage your money. Money operations may be unavailable", 'errorURI':' '}
    print('simulatorClaimUserRequest ' + str(respuesta))
    return respuesta

if __name__ == '__main__':
   app.run(host = HOST, port = PORT, debug = True)

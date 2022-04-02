

def generarInitSequence(modelo):
    contenido = """
mkdir {0}
cd {0}
npx express-generator
npm install mysql --save
npm install sqlite3 --save
npm install mysql --save
npm install sequelize --save
npm install
    """.format(modelo['nombre'].lower())
    return contenido

def generarManifiestJson(modelo):
    contenido = """
{
  "name": "{0}",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "start": "node ./bin/www"
  },
  "dependencies": {
    "cookie-parser": "~1.4.4",
    "debug": "~2.6.9",
    "express": "~4.16.1",
    "http-errors": "~1.6.3",
    "jade": "~1.11.0",
    "morgan": "~1.9.1",
    "mysql": "^2.18.1",
    "sqlite3": "^5.0.2"
  }
}
    """.format(modelo['nombre'].lower())
    return contenido

def generarRoutes(modelo):
    nombreProyecto = modelo['nombre'].lower()
    entidades = modelo['__listas']['Entidades']
    rutas_entidades = []
    for entidad in entidades:
        campos = entidad['__listas']['Campos']
        lista_campos = [ campo['nombre'] for campo in campos if 'pk' not in campo['__atributos'] or campo['__atributos']['pk'] != '1' ]
    rutas_entidades = [ """
router.route('/{0}/:id')
.get(async (req, res, next)=>{
    let resultado = await persistencia.obtener_{0}(req.params.id);
    if(resultado.length == 0){
        res.status(404).send('No encontrado');
    }else{
        res.send(resultado[0]);
    }
})
.post( async (req, res, next)=>{
    let lista_campos = [{1}];
    var values = {};
    lista_campos.forEach( (item)=>{
        if req.body.hasOwnProperty( item ){
            values[item] = req.body[item];
        }
    } );
    let resultado = await persistencia.actualizar_{0}( req.params.id , values );
    res.send( resultado );
})
.delete( async (req, res, next)=>{
    let resultado = await persistencia.eliminar_{0}( req.params.id , values);
    res.send( resultado );
});

router.route('/{0}')
.get( async (req, res, next)=>{
    let resultado = await persistencia.obtener_{0}s();
    if(resultado.length == 0){
        res.status(404).send('No encontrado');
    }else{
        res.send(resultado);
    }
})
.post( async (req, res, next)=>{
    let lista_campos = [{1}];
    var values = {};
    lista_campos.forEach( (item)=>{
        if req.body.hasOwnProperty( item ){
            values[item] = req.body[item];
        }
    } );
    let resultado = await persistencia.registrar_{0}( values );
    res.send(resultado)
});
    """.format( entidad['nombre'].lower(), " ".join(lista_campos) ) for entidad in entidades ]
    contenido = """
var express = require('express');
var persistencia = require('./persistencia/{0}')
var router = express.Router();

{1}

module.exports = router;
    """, format(nombreModelo, "\n".join(rutas_entidades) );
    return contenido

def generarModelo(modelo):

    nombreProyecto = modelo['nombre'].lower()

    resultado = { 'archivos' : [ { 'path':'Secuencia init',     'contenido': generarInitSequence(modelo) },
                                 { 'path': nombreProyecto + '/manifiest.json','contenido': generarManifiestJson(modelo) },
                                 { 'path': nombreProyecto + '/routes/' + nombreProyecto + '.js','contenido': generarRoutes(modelo) },
                                 #{ 'path':'app/models.py',      'contenido': generarModelsPy(modelo) },
                                 #{ 'path':'app/admin.py',       'contenido': generarAdminViewsPy(modelo) },
                                 #{ 'path':'app/serializers.py', 'contenido': generarSerializersPy(modelo) },
                                 #{ 'path':'app/forms.py',       'contenido': generarFormsPy(modelo) },
                                 #{ 'path':'app/views.py',       'contenido': generarViewsPy(modelo) },
                                 #{ 'path':'project/urls.py',    'contenido': generarPryUrlsPy(modelo) },
                                 #{ 'path':'app/urls.py',        'contenido': generarAppUrlsPy(modelo) },
                                 ]}
    return resultado

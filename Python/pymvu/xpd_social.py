import xpd_orm as orm
from os.path import abspath , dirname, exists

from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle

import xpd_usr

from hashlib import sha256

from uuid import uuid4

PATH_BDD = dirname(abspath(__file__)) + "/data/base.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/init_pymvu.sql"

RUTA_BASE = ""

Seguimientos = orm.Entidad()
Seguimientos.setMetamodelo({
    "nombreTabla":"SEGUIMIENTO",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"id_usuario_seguidor",
            "nombreCampo":"ID_USUARIO_SEGUIDOR",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_usuario_seguido",
            "nombreCampo":"ID_USUARIO_SEGUIDO",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"activo",
            "nombreCampo":"ACTIVO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findBySeguidor",
            "whereClause":["id_usuario_seguidor", "activo"]
            },
        {
            "nombre":"findBySeguido",
            "whereClause":["id_usuario_seguido", "activo"]
            },
        {
            "nombre":"findBySeguidorSeguido",
            "whereClause":["id_usuario_seguidor", "id_usuario_seguido"]
            },
        ]
    })

Amistades = orm.Entidad()
Amistades.setMetamodelo({
    "nombreTabla":"AMISTAD",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"activo",
            "nombreCampo":"ACTIVO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findAll",
            "whereClause":["activo"]
            },
        ]
    })

UsuariosAmistad = orm.Entidad()
UsuariosAmistad.setMetamodelo({
    "nombreTabla":"USUARIOS_AMISTAD",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"id_amistad",
            "nombreCampo":"ID_AMISTAD",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_usuario",
            "nombreCampo":"ID_USUARIO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByAmistad",
            "whereClause":["id_amistad"]
            },
        ]
    })

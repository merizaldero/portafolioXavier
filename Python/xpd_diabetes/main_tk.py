import tkinter as tk
from tkinter import messagebox
import xpd_health
import xpd_orm as orm
from xpd_tk import FormularioEdicionTki, VisorListadoTki, VisorImagenTki
import datetime
from os.path import join, dirname
import sys

FORMULARIOS = {
    "sujeto_show_form" : None,
    "sujeto_show_grafico" : None,
    "glucosa_edit_form" : None,
    "insulina_edit_form" : None,
}

def show_sujeto(id_sujeto):
    conexion = orm.Conexion(xpd_health.PATH_BDD)
    sujeto = xpd_health.Sujetos.getNamedQuery(conexion, "findById", {"id":id_sujeto} )
    conexion.close()
    if len(sujeto) == 0 :
        messagebox.showerror("Error","Sujeto no encontrado")
        return       
    sujeto = sujeto[0]
    FORMULARIOS["sujeto_show_form"].setData(sujeto)
    FORMULARIOS["sujeto_show_form"].mostrar()
    path_imagen = xpd_health.generar_imagen_sujeto(id_sujeto)
    print("imagen generada")
    FORMULARIOS["sujeto_show_grafico"].setPath(path_imagen)
    FORMULARIOS["sujeto_show_grafico"].mostrar()


def show_ingresar_glucosa( sujeto ):
    nuevo_glucosa = xpd_health.LecturaGlucosas.nuevoDiccionario()
    nuevo_glucosa["id_sujeto"] = sujeto["id"]
    nuevo_glucosa["fecha_hora"] = datetime.datetime.now().isoformat()
    nuevo_glucosa["valor"] = 0
    nuevo_glucosa["observacion"] = ""
    FORMULARIOS["glucosa_edit_form"].setData(nuevo_glucosa)
    FORMULARIOS["sujeto_show_form"].esconder()
    FORMULARIOS["sujeto_show_grafico"].esconder()
    FORMULARIOS["glucosa_edit_form"].mostrar()

def salir_app(sujeto):
    sys.exit(0)

def guardar_glucosa(lecturaGlucosa):
    try:
        xpd_health.transaccionar(xpd_health.LecturaGlucosas.insertar, lecturaGlucosa)
        messagebox.showinfo("Exito","Guardado Exitoso")
        cancelar_ingreso(lecturaGlucosa)
    except Exception as ex:
        messagebox.showerror("Error","Error de Guardado")

def show_ingresar_dosis_insulina( sujeto ):
    nuevo_insulina = xpd_health.DosisInsulinas.nuevoDiccionario()
    nuevo_insulina["id_sujeto"] = sujeto["id"]
    nuevo_insulina["fecha_hora"] = datetime.datetime.now().isoformat()
    nuevo_insulina["unidades_aplicadas"] = 30
    nuevo_insulina["observacion"] = "()h"
    FORMULARIOS["insulina_edit_form"].setData(nuevo_insulina)
    FORMULARIOS["sujeto_show_form"].esconder()
    FORMULARIOS["sujeto_show_grafico"].esconder()
    FORMULARIOS["insulina_edit_form"].mostrar()


def cancelar_ingreso(objeto):
    FORMULARIOS["glucosa_edit_form"].esconder()
    FORMULARIOS["insulina_edit_form"].esconder()
    show_sujeto(objeto["id_sujeto"])

def guardar_insulina(dosisInsulina):
    try:
        xpd_health.transaccionar(xpd_health.DosisInsulinas.insertar, dosisInsulina)
        messagebox.showinfo("Exito","Guardado Exitoso")
        cancelar_ingreso(dosisInsulina)
    except Exception as ex:
        messagebox.showerror("Error","Error de Guardado")

SUJETO_SHOW_CAMPOS = [
    {
        "nombre" : "nombre",
        "etiqueta" : "Nombre",
        "tipo": "STRING",
        "editable": False ,
        "nullable": False ,
        "valor_defecto": "Nombre Aqui",
        "tamano": 24 ,
        "precision" : 0 
    }
]

SUJETO_SHOW_COMANDOS = [
    { 
        "etiqueta" : "Registrar Glucosa",
        "color_fondo" : "PRIMARY",
        "callback": show_ingresar_glucosa
    },
    { 
        "etiqueta" : "Registrar Insulina",
        "color_fondo" : "PRIMARY",
        "callback": show_ingresar_dosis_insulina
    },
    { 
        "etiqueta" : "Salir",
        "color_fondo" : "DANGER",
        "callback": salir_app
    },
]

GLUCOSA_EDIT_CAMPOS = [
    {
        "nombre" : "fecha_hora",
        "etiqueta" : "Fecha / Hora",
        "tipo": "DATETIME",
        "editable": True ,
        "nullable": False ,
        "valor_defecto": datetime.datetime.now().isoformat(),
        "tamano": 25 ,
        "precision" : 0 
    },
    {
        "nombre" : "valor",
        "etiqueta" : "Valor",
        "tipo": "INTEGER",
        "editable": True ,
        "nullable": False ,
        "valor_defecto": 0,
        "tamano": 4 ,
        "precision" : 0 
    },
    {
        "nombre" : "observacion",
        "etiqueta" : "Observacion",
        "tipo": "STRING",
        "editable": True ,
        "nullable": True ,
        "valor_defecto": "",
        "tamano": 25 ,
        "precision" : 0 
    },
]

GLUCOSA_EDIT_COMANDOS = [
    { 
        "etiqueta" : "Cancelar",
        "color_fondo" : "DANGER",
        "callback": cancelar_ingreso
    },
    { 
        "etiqueta" : "Guardar",
        "color_fondo" : "SUCCESS",
        "callback": guardar_glucosa
    },
]

INSULINA_EDIT_CAMPOS = [
    {
        "nombre" : "fecha_hora",
        "etiqueta" : "Fecha / Hora",
        "tipo": "DATETIME",
        "editable": True ,
        "nullable": False ,
        "valor_defecto": datetime.datetime.now().isoformat(),
        "tamano": 25 ,
        "precision" : 0 
    },
    {
        "nombre" : "unidades_aplicadas",
        "etiqueta" : "Unidades Aplicadas",
        "tipo": "INTEGER",
        "editable": True ,
        "nullable": False ,
        "valor_defecto": 0,
        "tamano": 4 ,
        "precision" : 0 
    },
    {
        "nombre" : "observacion",
        "etiqueta" : "Observacion",
        "tipo": "STRING",
        "editable": True ,
        "nullable": True ,
        "valor_defecto": "",
        "tamano": 25 ,
        "precision" : 0 
    },

]
INSULINA_EDIT_COMANDOS = [
    { 
        "etiqueta" : "Cancelar",
        "color_fondo" : "DANGER",
        "callback": cancelar_ingreso
    },
    { 
        "etiqueta" : "Guardar",
        "color_fondo" : "SUCCESS",
        "callback": guardar_insulina
    },
]

if __name__ == "__main__":
    ventana = tk.Tk()    
    FORMULARIOS['sujeto_show_form'] = FormularioEdicionTki(ventana, SUJETO_SHOW_CAMPOS, SUJETO_SHOW_COMANDOS)
    FORMULARIOS['sujeto_show_grafico'] = VisorImagenTki(ventana, join( dirname(__file__) , "static", "img", "resumen_1.png") )
    FORMULARIOS["glucosa_edit_form"] = FormularioEdicionTki(ventana, GLUCOSA_EDIT_CAMPOS, GLUCOSA_EDIT_COMANDOS)
    FORMULARIOS["insulina_edit_form"] = FormularioEdicionTki(ventana, INSULINA_EDIT_CAMPOS, INSULINA_EDIT_COMANDOS)
    show_sujeto(1)
    ventana.mainloop()
    print("Termina mainloop")
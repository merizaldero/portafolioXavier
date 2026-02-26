import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import copy

class FormularioEdicionTki:
    def __init__(self, parent_control, lista_campos, lista_comandos=[]):
        self.parent = parent_control
        self.__lista_campos = copy.deepcopy(lista_campos)
        self.__lista_comandos = lista_comandos
        self.__datos = {}
        self.__dic_controles = {}
        
        # Frame principal del formulario (inicialmente oculto)
        self.frame_container = tk.Frame(self.parent)
        
        # Colores para los comandos
        self.__colores = {
            "PRIMARY": "#007bff",
            "SECONDARY": "#6c757d",
            "SUCCESS": "#28a745",
            "DANGER": "#dc3545"
        }

        self.__inicializar_datos_y_controles()
        self.__crear_interfaz()

    def __inicializar_datos_y_controles(self):
        """Configura los valores iniciales y valida la estructura de campos."""
        for campo in self.__lista_campos:
            nombre = campo["nombre"]
            tipo = campo["tipo"]
            
            # Valores por defecto para llaves opcionales
            campo["etiqueta"] = campo.get("etiqueta", nombre.replace("_", " ").capitalize())
            campo["editable"] = campo.get("editable", True)
            campo["nullable"] = campo.get("nullable", False)
            
            # Inicializar self.__datos
            val_defecto = campo.get("valor_defecto")
            if val_defecto is None:
                if tipo in ["INTEGER", "REAL"]: val_defecto = 0
                elif tipo == "BOOLEAN": val_defecto = False
                else: val_defecto = ""
            
            self.__datos[nombre] = val_defecto

    def __crear_interfaz(self):
        """Genera los widgets en el frame_container."""
        # Grid para los campos
        for i, campo in enumerate(self.__lista_campos):
            nombre = campo["nombre"]
            
            # Etiqueta
            lbl = tk.Label(self.frame_container, text=campo["etiqueta"] + ":")
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            
            # Control de edición
            estado = "normal" if campo["editable"] else "disabled"
            
            if campo["tipo"] == "BOOLEAN":
                var = tk.BooleanVar(value=self.__datos[nombre])
                ctrl = tk.Checkbutton(self.frame_container, variable=var, state=estado)
                self.__dic_controles[nombre] = var # Almacenamos la variable
            elif campo["tipo"] == "LONGSTRING":
                ctrl = tk.Text(self.frame_container, height=4, width=30, state=estado)
                ctrl.insert("1.0", str(self.__datos[nombre]))
                self.__dic_controles[nombre] = ctrl
            else:
                # Caso general: Entry (STRING, INTEGER, REAL, DATE, DATETIME, BARCODE)
                var = tk.StringVar(value=str(self.__datos[nombre]))
                ctrl = tk.Entry(self.frame_container, textvariable=var, state=estado)
                if campo["tipo"] in ["STRING", "REAL"]:
                    ctrl.config(width=campo.get("tamano", 20))
                self.__dic_controles[nombre] = var # Almacenamos la variable para fácil Sync

            ctrl.grid(row=i, column=1, sticky="w", padx=5, pady=2)

        # Barra de botones
        frame_botones = tk.Frame(self.frame_container)
        frame_botones.grid(row=len(self.__lista_campos), column=0, columnspan=2, pady=10)

        for comando in self.__lista_comandos:
            color = comando["color_fondo"]
            bg_color = color if color.startswith("#") else self.__colores.get(color, "SystemButtonFace")
            fg_color = "white" if bg_color != "SystemButtonFace" else "black"
            
            btn = tk.Button(
                frame_botones, 
                text=comando["etiqueta"],
                bg=bg_color,
                fg=fg_color,
                command=lambda cmd=comando: self.__ejecutar_callback(cmd["callback"])
            )
            btn.pack(side="left", padx=5)

    def __ejecutar_callback(self, callback_func):
        """Sincroniza controles a self.__datos y ejecuta el callback."""
        for campo in self.__lista_campos:
            nombre = campo["nombre"]
            ctrl = self.__dic_controles[nombre]
            
            # Obtener valor según el tipo de widget/variable almacenada
            if isinstance(ctrl, tk.BooleanVar):
                val = ctrl.get()
            elif isinstance(ctrl, tk.Text):
                val = ctrl.get("1.0", "end-1c")
            else: # StringVar
                val = ctrl.get()
            
            # Casting básico según tipo
            try:
                if campo["tipo"] == "INTEGER": val = int(val) if val else 0
                elif campo["tipo"] == "REAL": val = float(val) if val else 0.0
                elif campo["tipo"] == "BOOLEAN": val = bool(val)
            except ValueError:
                pass # Se mantiene como string si falla la conversión
                
            self.__datos[nombre] = val
            
        callback_func(self.__datos)

    def mostrar(self):
        self.frame_container.pack(fill="both", expand=True, padx=10, pady=10)

    def esconder(self):
        self.frame_container.pack_forget()

    def setData(self, diccionario):
        """Actualiza el diccionario interno y los controles visuales."""
        self.__datos = copy.deepcopy(diccionario)
        for nombre, valor in self.__datos.items():
            if nombre in self.__dic_controles:
                ctrl = self.__dic_controles[nombre]
                if isinstance(ctrl, (tk.StringVar, tk.BooleanVar)):
                    ctrl.set(valor)
                elif isinstance(ctrl, tk.Text):
                    ctrl.delete("1.0", tk.END)
                    ctrl.insert("1.0", str(valor))

class VisorListadoTki:
    def __init__(self, parent_control, lista_campos, lista_comandos=[]):
        self.parent = parent_control
        self.__lista_campos = copy.deepcopy(lista_campos)
        self.__lista_comandos = lista_comandos
        self.__datos = []
        self.__seleccionados = {} # Diccionario para rastrear Checkboxes por ID de fila

        # Contenedor principal (oculto por defecto)
        self.container = tk.Frame(self.parent)
        
        # Diccionario de colores para botones
        self.__colores_map = {
            "PRIMARY": "#007bff",
            "SECONDARY": "#343a40",
            "SUCCESS": "#28a745",
            "DANGER": "#dc3545"
        }

        self.__preparar_campos()
        self.__crear_interfaz()
        
        # Inicialización con datos vacíos o por defecto
        self.setData([])

    def __preparar_campos(self):
        """Procesa etiquetas faltantes en la configuración de campos."""
        for campo in self.__lista_campos:
            if "etiqueta" not in campo:
                campo["etiqueta"] = campo["nombre"].replace("_", " ").capitalize()

    def __crear_interfaz(self):
        """Genera la barra de herramientas y el Grid."""
        # 1. Barra de comandos (Botones arriba)
        self.barra_herramientas = tk.Frame(self.container)
        self.barra_herramientas.pack(side="top", fill="x", pady=5)

        for cmd in self.__lista_comandos:
            color_fondo = cmd["color_fondo"]
            bg = color_fondo if color_fondo.startswith("#") else self.__colores_map.get(color_fondo, "#f0f0f0")
            fg = "white" if bg != "#f0f0f0" else "black"

            btn = tk.Button(
                self.barra_herramientas,
                text=cmd["etiqueta"],
                bg=bg,
                fg=fg,
                command=lambda c=cmd: self.__ejecutar_callback(c["callback"])
            )
            btn.pack(side="left", padx=2)

        # 2. Grid (Treeview)
        # Definimos las columnas (incluyendo una para el checkbox visual)
        columnas_id = ["#select"] + [c["nombre"] for c in self.__lista_campos]
        
        self.tree = ttk.Treeview(self.container, columns=columnas_id, show="headings", selectmode="none")
        
        # Configurar columna de selección (Checkbox visual)
        self.tree.heading("#select", text="[X]")
        self.tree.column("#select", width=40, anchor="center")
        
        # Configurar columnas de datos
        for campo in self.__lista_campos:
            self.tree.heading(campo["nombre"], text=campo["etiqueta"])
            # Calcular ancho basado en porcentaje si existe, si no usar tamaño
            ancho = campo.get("porcentaje_ancho", 10) * 5 
            self.tree.column(campo["nombre"], width=ancho, anchor="w")

        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Evento de clic para simular checkbox
        self.tree.bind("<Button-1>", self.__al_hacer_clic)

    def __al_hacer_clic(self, event):
        """Maneja la selección lógica al hacer clic en una fila."""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            # Alternar estado de selección
            esta_seleccionado = self.__seleccionados.get(item_id, False)
            self.__seleccionados[item_id] = not esta_seleccionado
            
            # Actualizar visualmente (usando tags para simular el check)
            nuevo_texto = "☑" if self.__seleccionados[item_id] else "☐"
            valores = list(self.tree.item(item_id, "values"))
            valores[0] = nuevo_texto
            self.tree.item(item_id, values=valores)

    def __ejecutar_callback(self, callback_func):
        """Filtra los datos seleccionados y ejecuta el callback."""
        items_seleccionados = []
        for i, item_id in enumerate(self.tree.get_children()):
            if self.__seleccionados.get(item_id, False):
                items_seleccionados.append(self.__datos[i])
        
        callback_func(items_seleccionados)

    def setData(self, listado):
        """Limpia el grid y carga los nuevos datos."""
        self.__datos = copy.deepcopy(listado)
        self.__seleccionados = {}
        
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insertar filas
        for idx, fila in enumerate(self.__datos):
            valores = ["☐"] # Icono de no seleccionado inicial
            for campo in self.__lista_campos:
                val = fila.get(campo["nombre"], "")
                
                # Formateo básico de precisión para REAL
                if campo["tipo"] == "REAL" and "precision" in campo:
                    try:
                        val = f"{float(val):.{campo['precision']}f}"
                    except: pass
                
                valores.append(val)
            
            item_id = self.tree.insert("", "end", values=valores)
            self.__seleccionados[item_id] = False

    def mostrar(self):
        """Hace visible el componente completo."""
        self.container.pack(fill="both", expand=True, padx=5, pady=5)

    def esconder(self):
        """Oculta el componente completo."""
        self.container.pack_forget()
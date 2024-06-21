% include('xpd_minearch/encabezado.tpl', titulo="Información Edificio", usuario = usuario, estilo ="")

% if lvl != "" :
<div class="alert alert-{{lvl}}">
{{mensaje}}
</div>
% end

<form method="POST" id="frmSolicitud">
<div class="card mt-3">  
  <div class="card-body bg-light">
    <div class="form-group">
        <div class="mb-3">
            <label for="nombre" class="form-label">Nombre:</label>
            <input type="text" class="form-control" id="nombre" placeholder="Nombre" name="nombre" maxlength="16" value="{{edificio['nombre']}}">
        </div>
        <div class="mb-3 mt-3">
            <label for="descripcion" class="form-label">Descripci&oacute;n:</label>
            <input type="text" class="form-control" id="descripcion" placeholder="Descripci&oacute;n" name="descripcion" maxlength="128" value="{{edificio['descripcion']}}">
        </div>
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" id="es_publico" name="es_publico" value="1"
% if edificio['es_publico'] == 1 :
            checked
% end           
          >
          <label class="form-check-label" for="es_publico">Visible P&uacute;blico</label>
        </div>
    </div>
  </div>
</div>

<div class="mt-3 w-100 d-flex flex-row justify-content-around">      
    <a class="btn btn-secondary" href="/xpd_minearch/edificios">Cancelar</a>
    <input type="submit" class="btn btn-primary" value="Guardar">
</div>

</form>

% include('xpd_minearch/pie.tpl', usuario = usuario)
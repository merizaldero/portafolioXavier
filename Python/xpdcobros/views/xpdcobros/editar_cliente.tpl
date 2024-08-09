% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Solicitar Item de Cobro", usuario = usuario, estilo ="")

% if lvl != "" :
<div class="alert alert-{{lvl}}">
{{mensaje}}
</div>
% end

<form method="POST">
<div class="card mt-3">  
  <div class="card-body bg-light">
    <div class="form-group">
        <div class="mb-3">
            <label for="nombre" class="form-label">Nombre:</label>
            <input type="text" class="form-control" placeholder="Nombre Cliente" name="nombre" maxlength="32" value="{{cliente['nombre']}}" locked>
        </div>
        <div class="mb-3 mt-3">
            <label for="email" class="form-label">Email:</label>
            <input type="email" class="form-control" placeholder="E-Mail" name="email" maxlength="64" value="{{cliente['email']}}" locked>
        </div>
    </div>
  </div>
</div>

<div class="mt-3 w-100 d-flex flex-row justify-content-around">
    <a class="btn btn-secondary" href="/xpdcobros/usuarios/organizacion/{{organizacion['id']}}">Cancelar</a>
    <input type="submit" class="btn btn-primary" value="Guardar">
</div>

</form>

% include('xpdcobros/pie.tpl', usuario = usuario)
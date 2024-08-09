% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Configuracion", usuario = usuario, estilo ="")
<div class="container">
% if lvl != '':
    <div class="alert alert-{{lvl}}">
        {{mensaje}}
    </div>
% end
<form id="frm_cobrador" method="POST">
    <input type="hidden" name="accion" value="post_editar_cobrador">    

    <div class="card mt-3">
        <div class="card-body">
            <div class="container">
                <div class="row">
                    <div class="col strong">Empresa / Servicio :</div>
                    <div class="col">
                        <input class= "form-control" type="text" name="nombre" value="{{ cobrador['nombre'] }}" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col strong">E-mail :</div>
                    <div class="col">
                        <input class= "form-control" type="email" name="email" value="{{ cobrador['email'] }}" required>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-footer d-flex justify-content-between">
            <a class="btn btn-secondary" href="/xpdcobros/usuarios/organizacion/{{cobrador['id']}}">Cancelar</a>
            <input type="submit" class="btn btn-primary" value="Aceptar">
        </div>
    </div>

</form>
</div>

% include('xpdcobros/pie.tpl', usuario = usuario)
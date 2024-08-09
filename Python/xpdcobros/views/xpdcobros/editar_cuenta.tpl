% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Configuracion", usuario = usuario, estilo ="")
<div class="container">
% if lvl != '':
    <div class="alert alert-{{lvl}}">
        {{mensaje}}
    </div>
% end
<h1> Informaci&oacute;n de cuenta </h1>
<form id="frm_cuenta" method="POST">
    <div class="card mt-3">
        <div class="card-body">
            <div class="container">
                <div class="row">
                    <div class="col strong">Nombre Banco :</div>
                    <div class="col">
                        <input class= "form-control" type="text" name="nombre_banco" value="{{ cuenta['nombre_banco'] }}" maxlength="16" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col strong">Tipo Cuenta ( AHORROS | CORRIENTE ) : </div>
                    <div class="col">
                        <input class= "form-control" type="text" name="tipo_cuenta" value="{{ cuenta['tipo_cuenta'] }}" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col strong">N&uacute;mero Cuenta : </div>
                    <div class="col">
                        <input class= "form-control" type="text" name="numero_cuenta" value="{{ cuenta['numero_cuenta'] }}" required>
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
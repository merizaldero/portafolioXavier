% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Solicitar Item de Cobro", usuario = usuario, estilo ="")

% if msg_tipo != "" :
<div class="alert alert-{{msg_tipo}}">
{{msg}}
</div>
% end

<form method="POST" id="frmSolicitud">
<input type="hidden" name="hid_accion" id="hid_accion">
<div class="card mt-3">  
  <div class="card-body bg-light">
    <div class="form-group">
        <div class="mb-3">
            <label for="nombre" class="form-label">Nombre:</label>
            <input type="text" class="form-control" id="txt_nombre" placeholder="Nombre de Item de Cobro" name="txt_nombre" maxlength="32" value="{{solicitud['nombre']}}" locked>
        </div>
        <div class="mb-3 mt-3">
            <label for="email" class="form-label">Email:</label>
            <input type="email" class="form-control" id="txt_email" placeholder="E-Mail" name="txt_email" maxlength="64" value="{{solicitud['email']}}" locked>
        </div>
    </div>
  </div>
</div>

<div class="card mt-3">  
  <div class="card-body bg-light">
    La presente Solicitud tiene un costo de <b>USD {{costo}}</b>.
    <br>
    La creaci&oacute;n del Item de Cobro se realizar&aacute; al momento que el pago correspondiente sea aprobado.
  </div>
</div>

<div class="mt-3 w-100 d-flex flex-row justify-content-around">      
% if acciones == 'registrar':
    <a class="btn btn-secondary" href="/">Cancelar</a>
    <button class="btn btn-primary" onclick="enviar_accion('validar')">Continuar &gt;</button>
% elif acciones == 'validar':
    <a class="btn btn-secondary" href="/">Cancelar</a>
    <button class="btn btn-secondary" onclick="enviar_accion('registrar')">&lt; Regresar</button>
    <button class="btn btn-primary" onclick="enviar_accion('completar')">Completar &gt;</button>
% elif acciones == 'completado':
    <a class="btn btn-secondary" href="/">Inicio</a>
    <a class="btn btn-primary" href="/xpdcobros/usuarios/pagos_pendientes">Ver Pagos</a>
    <a class="btn btn-success" href="/xpdcobros/ordenes_pago/{{solicitud['id_orden_pago']}}">Pagar</a>
% end

</div>

</form>
<script language="javascript">
function enviar_accion(accion){
    const frmSolicitud = document.getElementById("frmSolicitud");
    frmSolicitud.hid_accion.value = accion;
    frmSolicitud.submit();
}

% if acciones == 'registrar':
const txt_nombre = document.getElementById("txt_nombre");
const txt_email = document.getElementById("txt_email");
txt_nombre.locked = false;
txt_email.locked = false;
% end

</script>
% include('xpdcobros/pie.tpl', usuario = usuario)
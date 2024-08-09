% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Inicio", usuario = usuario, estilo ="")
<div class="card">
  <div class="card-header d-flex flex-row justify-content-between">
    <span>Escoger Organizaci&oacute;n</span>
    <div>
      <a class="btn btn-primary" href="/xpdcobros/usuarios/solicitudcobrador/crear">+ Solicitar Cobrador</a>    
    </div>  
  </div>
  <div class="card-body">
    <div class="d-flex flex-column">
% for cobrador in organizaciones:
      <div class="mt-3 card">
        <div class="card-header text-bg-primary">{{cobrador['nombre']}}</div>
        <div class="card-body pl-5">
          {{cobrador['email']}}
        </div>
        <div class="card-footer d-flex flex-row justify-content-end">
          <a class="btn btn-success" href="/xpdcobros/usuarios/organizacion/{{cobrador['id_organizacion']}}">Gestionar</a>          
        </div>
      </div>
% end
% if len(organizaciones) == 0:
      <div class="alert-warning">
      <p>
      Al momento no tiene cobradores registrados.
      </p>
      <p>
      Solicite el registro de una nueva Organizaci&oacute;n <a class="card text-decoration-none" href="/xpdcobros/usuarios/solicitudcobrador/crear">aqu&iacute;</a> 
      </p>
      </div>      
% end
    </div>
  </div>
</div>
</script>
% include('xpdcobros/pie.tpl', usuario = usuario)
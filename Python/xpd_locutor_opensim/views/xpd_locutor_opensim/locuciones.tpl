% include('xpd_locutor_opensim/encabezado.tpl', titulo="Gestionar Locuciones", usuario = usuario, estilo ="")
<div class="card">
  <div class="card-header d-flex flex-row justify-content-between">
    <span>Locuciones</span>
  </div>
  <div class="card-body">
% if lvl != '':
    <div class="alert alert-{{lvl}}">
    {{mensaje}}
    </div>
% end
    <form method="POST">
    <input class="btn btn-secondary" type="submit" name="accion" value="Eliminar">
    <table class="table table-striped">
    <thead>
    <tr>
      <th></th>
      <th>Texto</th>
      <th>Duraci&oacute;n (seg)</th>
      <th>F. Creaci&oacute;n</th>
      <th>F. Lectura</th>
      <th></th>
      <th></th>
    </tr>
    </thead>
    <tbody>
% for locucion in locuciones:
      <tr>
        <td><input type="checkbox" name="id_locucion" value="{{locucion['id']}}"></td>
        <td>{{locucion['texto']}}</td>
        <td>{{locucion['duracion']}}</td>
        <td>{{locucion['fecha_creacion'][:10]}}</td>
        <td>{{locucion['fecha_lectura']}}</td>
        <td><a target="_blank" href="/xpd_locutor_opensim/locucion/{{locucion['id']}}">Reproducir</a></td>
        <td><a href="/xpd_locutor_opensim/locucion/{{locucion['id']}}/edit">Editar</a></td>
      </tr>
% end
% if len(locuciones) == 0:
      <tr>
      <td>
      Al momento no existe locuciones registradasa.
      </td>
      </tr>      
% end
    </tbody>
    </table>
    </form>
  </div>
</div>
</script>
% include('xpd_locutor_opensim/pie.tpl', usuario = usuario)
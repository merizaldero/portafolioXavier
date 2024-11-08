% include('novelas/encabezado.tpl', titulo="Cuadros Sinopticos")
<div class="d-flex flex-row justify-content-around">

  <div class="card ml-3">
    <div class="card-header">
      <span>Novelas Graficas</span>
    </div>
    <div class="card-body">
      <div class="list-group">
% for item in lista:
        <div class="item list-group-item">
          <a href="/static/novelas/{{item}}/index.html">{{item}}</a>
        </div>
% end
% if len(lista) == 0:
        <div class="alert-warning">
        <p>
        Al momento no hay cuadros sinópticos disponibles
        </p>
        </div>      
% end
      </div>
    </div>
  </div>

</div>

% include('novelas/pie.tpl')
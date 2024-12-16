% include('xpd_sistema_puntos/encabezado.tpl', titulo="titulo", usuario = usuario, estilo = "")
<ul class="list-group">
% for entidad in entidades:
<li class="list-group-item">
<a href="{{entidad['path']}}">{{entidad["nombre"]}}</a>
</li>
% end
</ul>
% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
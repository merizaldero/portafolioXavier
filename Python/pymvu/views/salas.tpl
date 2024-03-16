% include('encabezado.tpl', titulo="Salas", usuario = usuario)
<h1>Salas de Chat</h1>
% for sala in salas :
<div class="card mb-2">
    <div class="card-header">
        {{sala['nombre']}}
    </div>
    <div class="card-body">
    <ul class="small">
            <li>
                {{sala['descripcion']}}
            </li>
% if sala['privado'] == 1 :
            <li>
                SALA PRIVADA
            </li>        
% end
% if sala['username_propietario'] is not None :
            <li>
                Propietario: {{sala['username_propietario']}}
            </li>        
% end
        </ul>        
    </div>
    <div class="card-footer justify-content-end">
        <a class="btn btn-primary btn-sm" href ="/pymvu/chat/{{sala['id']}}">Ingresar &gt;&gt;</a>
    </div>
</div>
% end
% include('pie.tpl', usuario = usuario)
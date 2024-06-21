% include('xpd_minearch/encabezado.tpl', titulo="XPD Minetest Architech", usuario = usuario, estilo ="")
<div class="d-flex flex-row justify-content-around">

  <div class="card ml-3">
    <div class="card-header">
      <span>Creaciones de la Comunidad</span>
    </div>
    <div class="card-body">
      <div>
% for edificio in edificios_publicos:
        <div class="mt-3 card text-decoration-none">
          <div class="card-header">{{edificio['nombre']}}</div>
          <div class="card-body pl-5">
            {{edificio['descripcion']}}
          </div>
          <div class="card-footer d-flex flex-row justify-content-end">          
% if edificio['id_usuario'] == usuario['id']:
            <a class="btn btn-primary" href="/xpd_minearch/edificio/{{edificio['id']}}">Editar</a>
            <a class="btn btn-primary" href="/xpd_minearch/edificio/{{edificio['id']}}/editarbloques">Editar Bloques</a>
% else:
            <a class="btn btn-primary" href="/xpd_minearch/edificio/{{edificio['id']}}/editarbloques">Ver</a>
% end
            <button class="btn btn-primary btn-copiar-enlace" data-id_edificio="{{edificio['id']}}">Copiar URL</button>
          </div>
        </div>
% end
% if len(edificios_publicos) == 0:
        <div class="alert-warning">
        <p>
        Al momento no se ha compartido Creaciones en la Plataforma.
        </p>
        </div>      
% end
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-header d-flex flex-row justify-content-between">
      <span>Mis Creaciones</span>
      <div>
        <a class="btn btn-primary" href="/xpd_minearch/edificio/crear">+ Crear Nuevo</a>    
      </div>  
    </div>
    <div class="card-body">
      <div>
  % for edificio in edificios_usuario:
        <div class="mt-3 card text-decoration-none">
          <div class="card-header">{{edificio['nombre']}}</div>
          <div class="card-body pl-5">
            {{edificio['descripcion']}}
          </div>
          <div class="card-footer d-flex flex-row justify-content-end">          
            <a class="btn btn-primary" href="/xpd_minearch/edificio/{{edificio['id']}}">Editar</a>
            <a class="btn btn-primary" href="/xpd_minearch/edificio/{{edificio['id']}}/editarbloques">Editar Bloques</a>
            <button class="btn btn-primary btn-copiar-enlace" data-id_edificio="{{edificio['id']}}">Copiar URL</button>
          </div>
        </div>
  % end
  % if len(edificios_usuario) == 0:
        <div class="alert-warning">
        <p>
        Al momento no has creado Edificios.
        </p>
        <p>
        Realiza tu primera Creaci&oacute;n <a class="btn btn-primary" href="/xpd_minearch/edificio/crear">aqu&iacute;</a> 
        </p>
        </div>      
  % end
      </div>
    </div>
  </div>

</div>

<script>

function copiar_enlace(event){
  const id_edificio = event.target.dataset.id_edificio;
  const partes_path = document.location.href.split('/');
  const url = `${partes_path[0]}//${partes_path[2]}/xpd_minearch/edificio/${id_edificio}/bloques`;
  navigator.clipboard.writeText(url);
  alert(`URL Copiada: ${url}`);
}

window.addEventListener('load', async (event)=>{
  const botones_enlace = document.getElementsByClassName('btn-copiar-enlace');
  for(let indice = 0; indice < botones_enlace.length; indice++){
    const boton = botones_enlace[indice];
    boton.addEventListener('click', copiar_enlace);
  }
});

</script>

% include('xpd_minearch/pie.tpl', usuario = usuario)
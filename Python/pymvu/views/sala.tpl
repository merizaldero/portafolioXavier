% include('encabezado.tpl', titulo = 'Pymvu - Salas - ' + sala['nombre'], usuario = usuario)

<div id="div_canvas" class="p-0 w-100 h-100">
</div>

<div id="div_sidebar" class="collapse float-end w-25 ml-auto p-2 align-end d-flex flex-column" style="position:absolute; top:45px;bottom:45px; background-color:rgba(0,0,0, 0.3); color:#ffffff">
  <h4>Chat</h4>
  <div id="div_chat" class="flex-grow-1 p-1 overflow-auto d-flex flex-column" style="background-color:rgba(1.0,1.0,1.0, 0.3)"></div>
  <div class="input-group input-group-sm">
    <input id="txt_mensaje" type="text" class="form-control" placeholder="Escribir mensaje ...">
    <button id="btn_enviar_mensaje" class="btn btn-success" type="submit">Enviar</button>
  </div>
</div>

<script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@v0.161.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@v0.161.0/examples/jsm/"
      } 
    }
</script>

<script type="module">

import {SalaModule} from '/static/js/sala.js?2';

window.addEventListener("load", async (event)=>{
    SalaModule( {{ sala['id'] }} , '{{sala['url']}}' , {{ usuario['id'] }}, '{{ usuario['username'] }}' , 'div_canvas' );
});

</script>

% include('pie.tpl', usuario = usuario)
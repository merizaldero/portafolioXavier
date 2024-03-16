% include('encabezado.tpl', titulo="Principal", usuario = usuario)

<div id="div_canvas" class="w-100 h-100">
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

import {SalaModule} from '/static/js/sala.js';

window.addEventListener("load", async (event)=>{
    SalaModule( {{ sala['id'] }} , '{{sala['url']}}' , {{ usuario['id'] }}, '{{ usuario['username'] }}' , 'div_canvas' );
});

</script>

% include('pie.tpl', usuario = usuario)
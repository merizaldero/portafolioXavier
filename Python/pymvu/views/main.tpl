% include('encabezado.tpl', titulo="Pymvu - Inicio", usuario = usuario)
<div id="div_canvas" class="w-100 h-100 d-flex justify-content-center"></div>
<script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@v0.161.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@v0.161.0/examples/jsm/"
      }
    }
</script>

<script type="module" src="/static/js/main.js">
</script>
% include('pie.tpl', usuario = usuario)
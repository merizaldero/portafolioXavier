% include('encabezado.tpl', titulo="Principal", usuario = usuario)

<ul class="nav mb-4" id="ul_apariencias">
</ul>

<div class="row">
    <div class="col-md-6 h-sm-25 h-25-sm bg-light justify-content-center" id="div_canvas"></div>
    <div class="col-md-6">

        <div class="mb-1 mt-3 small">
            <label for="nombre" class="form-label form-label-sm">Nombre:</label>
            <input type="text" class="form-control form-control-sm" id="txt_nombre" placeholder="Ingrese Nombre" name="nombre">
            
            <label for="descripcion" class="form-label form-label-sm">Descripci&oacute;n:</label>
            <textarea class="form-control form-control-sm" rows="2" id="txt_descripcion" name="descripcion"></textarea>
            
            <div id="div_tipos_avatar" class="d-flex flex-row flex-wrap justify-content-around">
            </div>
            <input type="hidden" id="hid_id_tipo_avatar" name="hid_id_tipo_avatar">
            
            <div class="form-check form-switch">
                <label class="form-check-label form-check-label-sm" for="chk_activo">Activo </label>
                <input class="form-check-input form-check-input-sm" type="checkbox" id="chk_activo" name="chk_activo" value="1">
            </div>

            <div id="div_no_es_default" class="alert alert-warning justify-content-aroud">
                <span>Esta NO es la Apariencia Por Defecto</span>
                <button id="btn_si_default" class="btn btn-secondary">Definir por Defecto</button>
            </div>            
            <div id="div_es_default" class="alert alert-success">Esta es la Apariencia Por Defecto</div>

        </div>
        <ul class="nav nav-pills border-bottom border-top" id="ul_tipos_prenda">
        </ul>
        <div id="div_lista_prendas" class="w-100 p-1 d-flex flex-row flex-wrap">
        </div>


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

<script type="module" src="/static/js/apariencia.js?2">
</script>

% include('pie.tpl', usuario = usuario)
% include('sinopticos/encabezado.tpl', titulo="Información Edificio")
<h1>{{nombre_modelo}}</h1>
% for item in lista:
<div id="div_{{item['idObjeto']}}" class="item d-flex flex-row border-bottom mb-2 py-2" data-idObjetoPadre="{{item['idObjetoPadre']}}">
  <div class="d-flex flex-column">
    <span><b>{{item['nombre']}}</b></span>
% if item['descripcion'] is not None and item['descripcion'] not in ['null','None']:
    <span>{{item['descripcion']}}</span>
% end
  </div>
  <div id="div_{{item['idObjeto']}}_hijos" class="d-flex flex-column border-primary border-2 border-start rounded-start ms-2 ps-2">
  </div>
</div>
% end

<script>

const lista_items = document.getElementsByClassName('item');

for(let indice = 0; indice < lista_items.length; indice ++){
  const item = lista_items[indice];
  const idObjetoPadre = item.dataset.idobjetopadre;
  if( idObjetoPadre != null && idObjetoPadre != 'null' && idObjetoPadre != 'None'){
    const id_div_padre = `div_${idObjetoPadre}_hijos`;
    const div_padre = document.getElementById(id_div_padre);
    if(div_padre){
      div_padre.appendChild(item);
    }
  }
}

</script>

% include('sinopticos/pie.tpl')
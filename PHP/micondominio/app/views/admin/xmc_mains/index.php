<h2>Mi Condominio EC</h2>

<div class="card" style="display:flex; flex-direction: row; align-items: center ; justify-content: space-between;align-content:flex-start"  >
	<h3>Flujos de Estados</h3>
	<a href="<?php echo MvcRouter::admin_url(array('controller' => 'flujoestados', 'action' => 'index')); ?>">Detalles</a>
</div>
<div class="card" style="display:flex; flex-direction: row; align-items: center ; justify-content: space-between;align-content:flex-start"  >
    <h3>Tipos de Construcci&oacute;n</h3>
    <a href="<?php echo MvcRouter::admin_url(array('controller' => 'tipoconstruccions', 'action' => 'index')); ?>">Detalles</a>
</div>
<div class="card" style="display:flex; flex-direction: row; align-items: center ; justify-content: space-between;align-content:flex-start"  >
    <h3>Condominios</h3>
    <a href="<?php echo MvcRouter::admin_url(array('controller' => 'condominios', 'action' => 'index')); ?>">Detalles</a>
</div>

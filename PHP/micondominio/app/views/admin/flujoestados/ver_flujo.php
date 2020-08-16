
<h2>Flujo - <?php echo $object->__name; ?></h2>
<h3 class="card-header">Estados ( <?php echo count($estados) ;?> ) <button onclick="agregar_estado()">Agregar</button></h3>
<form id="frm_estado" enctype="application/x-www-form-urlencoded" action="<?php echo mvc_admin_url([ 'controller' => 'flujoestados' , 'action' => 'crear_editar_estado', 'id' => $object->id ]); ?>" method="post">
<input type="hidden" name="data[Estado][id]" value="">
<input type="hidden" name="data[Estado][flujoestado_id]" value="<?php echo $object->id; ?>">
<input type="hidden" name="data[Estado][nombre]" value="">
<input type="hidden" name="data[Estado][estado_inicial]" value="">
<input type="hidden" name="data[Estado][estado_final]" value="">
</form>
	<table class="widefat post fixed striped" cellspacing="0">
    <thead>
        <tr><th scope="col" class="manage-column">Nombre</th><th scope="col" class="manage-column">Estado Inicial</th><th scope="col" class="manage-column">Estado Final</th><th scope="col" class="manage-column"></th></tr>    
    </thead>
    <tbody>  
	<?php
	foreach($estados as $estado){
	    echo '<tr><td>';
	    //echo $estado->nombre;
	    echo MvcFormTagsHelper::text_input('nombre_'.$estado->id ,['id' => 'nombre_'.$estado->id ,'value'=> $estado->nombre , 'onkeyup' => 'habilitar_submit_estado( '.$estado->id.' )']) ;  
	    echo '</td><td>';
	    echo MvcFormTagsHelper::checkbox_input( 'estado_inicial_'.$estado->id ,[ 'id'=> 'estado_inicial_'.$estado->id ,'value'=> '1', 'checked'=> ($estado->estado_inicial == '1'), 'onchange' => 'habilitar_submit_estado( '.$estado->id.' )' ]) ;
	    echo '</td><td>';
	    echo MvcFormTagsHelper::checkbox_input( 'estado_final_'.$estado->id ,  [ 'id'=> 'estado_final_'.$estado->id   ,'value'=> '1', 'checked'=> ($estado->estado_final == '1'),   'onchange' => 'habilitar_submit_estado( '.$estado->id.' )' ]) ;
	    echo '</td><td>';
	    echo '<span id="submit_estado_'.$estado->id.'" style="display:none;visibility:hidden">';
	    echo '<button onclick="submit_estado( '. $estado->id .' )">Guardar</button>';
	    echo '<button onclick="cancelar_edicion()">Cancelar</button>';
	    echo '</span>';
        echo '</td></tr>';
	}
	
	//Fila Extra para Nuevo
	
	echo '<tr id="nuevo_estado" style="display:none;visibility:hidden"><td>';
	//echo $estado->nombre;
	echo MvcFormTagsHelper::text_input('nombre_' ,['id' => 'nombre_' ] ) ;
	echo '</td><td>';
	echo MvcFormTagsHelper::checkbox_input( 'estado_inicial_' ,[ 'id'=> 'estado_inicial_' ,'value'=> '1' ]) ;
	echo '</td><td>';
	echo MvcFormTagsHelper::checkbox_input( 'estado_final_' ,  [ 'id'=> 'estado_final_'   ,'value'=> '1' ]) ;
	echo '</td><td>';
	echo '<button onclick="submit_estado( \'\' )">Guardar</button>';
	echo '<button onclick="cancelar_nuevo_estado()">Cancelar</button>';
	echo '</td></tr>';
	
	?>
	</tbody>
	</table>

<h3 class="card-header">Transiciones ( <?php echo count($transiciones) ;?> ) <button onclick="agregar_transicion()">Agregar</button></h3>
<form id="frm_transicion" enctype="application/x-www-form-urlencoded" action="<?php echo mvc_admin_url([ 'controller' => 'flujoestados' , 'action' => 'crear_editar_transicion', 'id' => $object->id ]); ?>" method="post">
<input type="hidden" name="data[Transicionestado][id]" value="">
<input type="hidden" name="data[Transicionestado][flujoestado_id]" value="<?php echo $object->id; ?>">
<input type="hidden" name="data[Transicionestado][descripcion]" value="">
<input type="hidden" name="data[Transicionestado][estado_origen_id]" value="">
<input type="hidden" name="data[Transicionestado][estado_destino_id]" value="">
<input type="hidden" name="data[Transicionestado][habilitado]" value="">
</form>	
	<table class="widefat post fixed striped" cellspacing="0">
    <thead>
        <tr><th scope="col" class="manage-column">Descripci&oacute;n</th><th scope="col" class="manage-column">Estado Origen</th><th scope="col" class="manage-column">Estado Destino</th><th scope="col" class="manage-column">Habilitado</th><th scope="col" class="manage-column"></th></tr>    
    </thead>
    <tbody>
	<?php
	foreach($transiciones as $transicion){
	    echo '<tr><td>';
	    //echo $estado->descripcion;
	    echo MvcFormTagsHelper::text_input('descripcion_'.$transicion->id ,['id' => 'descripcion_'.$transicion->id ,'value'=> $transicion->descripcion , 'onkeyup' => 'habilitar_submit_transicion( '.$transicion->id.' )']) ;
	    echo '</td><td>';
	    echo MvcFormTagsHelper::select_input( 'estado_origen_id_'.$transicion->id ,[ 'id'=> 'estado_origen_id_'.$transicion->id ,'value' => $transicion->estado_origen_id , 'options' => $estados,  'onchange' => 'habilitar_submit_transicion( '.$transicion->id.' )' ]) ;
	    echo '</td><td>';
	    echo MvcFormTagsHelper::select_input( 'estado_destino_id_'.$transicion->id ,[ 'id'=> 'estado_destino_id_'.$transicion->id ,'value' => $transicion->estado_destino_id , 'options' => $estados,  'onchange' => 'habilitar_submit_transicion( '.$transicion->id.' )' ]) ;
	    echo '</td><td>';
	    echo MvcFormTagsHelper::checkbox_input( 'habilitado_'.$transicion->id ,  [ 'id'=> 'habilitado_'.$transicion->id   ,'value'=> '1', 'checked'=> ($transicion->habilitado == '1'),   'onchange' => 'habilitar_submit_transicion( '.$transicion->id.' )' ]) ;   
	    echo '</td><td>';
	    echo '<span id="submit_transicion_'.$transicion->id.'" style="display:none;visibility:hidden">';
	    echo '<button onclick="submit_transicion( '. $transicion->id .' )">Guardar</button>';
	    echo '<button onclick="cancelar_edicion()">Cancelar</button>';
	    echo '</span>';
	    echo '</td></tr>';
	}
	echo '<tr id="nueva_transicion" style="display:none;visibility:hidden"><td>';
	//echo $estado->descripcion;
	echo MvcFormTagsHelper::text_input('descripcion_' ,['id' => 'descripcion_' ,'value'=> '' , 'onkeyup' => 'habilitar_submit_transicion( "" )']) ;
	echo '</td><td>';
	echo MvcFormTagsHelper::select_input( 'estado_origen_id_' ,[ 'id'=> 'estado_origen_id_' ,'value' => '' , 'options' => $estados,  'onchange' => 'habilitar_submit_transicion( "" )' ]) ;
	echo '</td><td>';
	echo MvcFormTagsHelper::select_input( 'estado_destino_id_' ,[ 'id'=> 'estado_destino_id_' ,'value' => '' , 'options' => $estados,  'onchange' => 'habilitar_submit_transicion( "" )' ]) ;
	echo '</td><td>';
	echo MvcFormTagsHelper::checkbox_input( 'habilitado_' ,  [ 'id'=> 'habilitado_'  ,'value'=> '1',  'onchange' => 'habilitar_submit_transicion( "" )' ]) ;
	echo '</td><td>';
	echo '<button onclick="submit_transicion( \'\' )">Guardar</button>';
	echo '<button onclick="cancelar_nueva_transicion()">Cancelar</button>';
	echo '</td></tr>';	
	?>

	</tbody>
	</table>

<script language="javascript">
	function agregar_estado(){
		var divNuevo = document.getElementById('nuevo_estado');
		divNuevo.style.display = "block";
		divNuevo.style.visibility = "visible";
	}
	function agregar_transicion(){
		var divNuevo = document.getElementById('nueva_transicion');
		divNuevo.style.display = "block";
		divNuevo.style.visibility = "visible";
	}
	function habilitar_submit_estado( idEstado ){
		var divSubmit = document.getElementById('submit_estado_' + idEstado);
		divSubmit.style.display = "inline";
		divSubmit.style.visibility = "visible";
	}
	function habilitar_submit_transicion( idTransicion ){
		var divSubmit = document.getElementById('submit_transicion_' + idTransicion);
		divSubmit.style.display = "inline";
		divSubmit.style.visibility = "visible";
	}
	
	function submit_estado( idEstado ){
		var txtNombre = document.getElementById('nombre_' + idEstado);
		var chkEstadoInicial = document.getElementById('estado_inicial_' + idEstado);
		var chkEstadoFinal = document.getElementById('estado_final_' + idEstado);
		var frmEstado = document.forms['frm_estado'];
		frmEstado['data[Estado][id]'].value = idEstado;
		frmEstado['data[Estado][nombre]'].value = txtNombre.value;
		frmEstado['data[Estado][estado_inicial]'].value = chkEstadoInicial.checked ? '1' : '0';
		frmEstado['data[Estado][estado_final]'].value = chkEstadoFinal.checked ? '1' : '0';
		frmEstado.submit();
	}
	
	function submit_transicion( idTransicion ){
		var txtDescripcion = document.getElementById('descripcion_' + idTransicion);
		var selEstadoOrigen = document.getElementById('estado_origen_id_' + idTransicion);
		var selEstadoDestino = document.getElementById('estado_destino_id_' + idTransicion);
		var chkHabilitado = document.getElementById('habilitado_' + idTransicion);
		var frmTransicion = document.forms['frm_transicion'];
		frmTransicion['data[Transicionestado][id]'].value = idTransicion;
		frmTransicion['data[Transicionestado][descripcion]'].value = txtDescripcion.value;
		frmTransicion['data[Transicionestado][estado_origen_id]'].value = selEstadoOrigen.value;
		frmTransicion['data[Transicionestado][estado_destino_id]'].value = selEstadoDestino.value;
		frmTransicion['data[Transicionestado][habilitado]'].value = chkHabilitado.checked ? '1' : '0';
		frmTransicion.submit();
	}

	function cancelar_nuevo_estado(){
		var divNuevo = document.getElementById('nuevo_estado');
		divNuevo.style.display = "none";
		divNuevo.style.visibility = "hidden";
	}

	function cancelar_nueva_transicion(){
		var divNuevo = document.getElementById('nueva_transicion');
		divNuevo.style.display = "none";
		divNuevo.style.visibility = "hidden";
	}

	function cancelar_edicion(){
		document.location.href = "<?php echo mvc_admin_url([ 'controller' => 'flujoestados' , 'action' => 'ver_flujo', 'id' => $object->id ]); ?>";
	}

</script>


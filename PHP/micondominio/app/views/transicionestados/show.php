<h2><?php echo $object->descripcion; ?></h2>

<?php
if(!empty($object->flujoestado_id)){
    echo '<div><span>flujoestado_id</span><span>' . $object->flujoestado_id . '</span></div>';
} 
?>
<?php
if(!empty($object->estado_origen_id)){
    echo '<div><span>estado_origen_id</span><span>' . $object->estado_origen_id . '</span></div>';
} 
?>
<?php
if(!empty($object->estado_destino_id)){
    echo '<div><span>estado_destino_id</span><span>' . $object->estado_destino_id . '</span></div>';
} 
?>
<?php
if(!empty($object->habilitado)){
    echo '<div><span>habilitado</span><span>' . $object->habilitado . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Transicionestados', array('controller' => 'transicionestados')); ?>
</p>


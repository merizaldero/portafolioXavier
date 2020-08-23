<h2><?php echo $object->nombre; ?></h2>

<?php
if(!empty($object->flujoestado_id)){
    echo '<div><span>flujoestado_id</span><span>' . $object->flujoestado_id . '</span></div>';
} 
?>

<?php
if(!empty($object->activo_negocio)){
    echo '<div><span>activo_negocio</span><span>' . $object->activo_negocio . '</span></div>';
} 
?>
<?php
if(!empty($object->estado_inicial)){
    echo '<div><span>estadoInicial</span><span>' . $object->estado_inicial . '</span></div>';
} 
?>
<?php
if(!empty($object->estado_final)){
    echo '<div><span>estadoFinal</span><span>' . $object->estado_final . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Estados', array('controller' => 'estados')); ?>
</p>


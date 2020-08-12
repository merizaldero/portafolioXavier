<h2><?php echo $object->descripcion; ?></h2>

<$php
if(!empty($object->condominio_id)){
    echo '<div><span>condominio_id</span><span>' . $object->condominio_id . '</span></div>';
} 
?>
<$php
if(!empty($object->fecha)){
    echo '<div><span>fecha</span><span>' . $object->fecha . '</span></div>';
} 
?>
<$php
if(!empty($object->monto)){
    echo '<div><span>monto</span><span>' . $object->monto . '</span></div>';
} 
?>
<$php
if(!empty($object->habitante_abono_id)){
    echo '<div><span>habitante_abono_id</span><span>' . $object->habitante_abono_id . '</span></div>';
} 
?>
<$php
if(!empty($object->estado_id)){
    echo '<div><span>estado_id</span><span>' . $object->estado_id . '</span></div>';
} 
?>
<$php
if(!empty($object->transaccion_id)){
    echo '<div><span>transaccion_id</span><span>' . $object->transaccion_id . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Gastos', array('controller' => 'gastos')); ?>
</p>

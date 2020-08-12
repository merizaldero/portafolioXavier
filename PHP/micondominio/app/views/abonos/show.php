<h2>Abono</h2>

<$php
if(!empty($object->habitante_id)){
    echo '<div><span>habitante_id</span><span>' . $object->habitante_id . '</span></div>';
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
if(!empty($object->saldo)){
    echo '<div><span>saldo</span><span>' . $object->saldo . '</span></div>';
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
<$php
if(!empty($object->usuario_registro_id)){
    echo '<div><span>usuario_registro_id</span><span>' . $object->usuario_registro_id . '</span></div>';
} 
?>
<$php
if(!empty($object->fecharegistro)){
    echo '<div><span>fecharegistro</span><span>' . $object->fecharegistro . '</span></div>';
} 
?>
<$php
if(!empty($object->usuario_modificacion_id)){
    echo '<div><span>usuario_modificacion_id</span><span>' . $object->usuario_modificacion_id . '</span></div>';
} 
?>
<$php
if(!empty($object->fechamodificacion)){
    echo '<div><span>fechamodificacion</span><span>' . $object->fechamodificacion . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Abonos', array('controller' => 'abonos')); ?>
</p>


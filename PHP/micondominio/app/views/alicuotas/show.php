<h2>Alicuota</h2>

<?php
if(!empty($object->habitante_id)){
    echo '<div><span>habitante_id</span><span>' . $object->habitante_id . '</span></div>';
} 
?>
<?php
if(!empty($object->fecha)){
    echo '<div><span>fecha</span><span>' . $object->fecha . '</span></div>';
} 
?>
<?php
if(!empty($object->monto)){
    echo '<div><span>monto</span><span>' . $object->monto . '</span></div>';
} 
?>
<?php
if(!empty($object->saldo)){
    echo '<div><span>saldo</span><span>' . $object->saldo . '</span></div>';
} 
?>
<?php
if(!empty($object->user_creacion_id)){
    echo '<div><span>user_creacion_id</span><span>' . $object->user_creacion_id . '</span></div>';
} 
?>
<?php
if(!empty($object->fecharegistro)){
    echo '<div><span>fecharegistro</span><span>' . $object->fecharegistro . '</span></div>';
} 
?>
<?php
if(!empty($object->user_modificacion_id)){
    echo '<div><span>user_modificacion_id</span><span>' . $object->user_modificacion_id . '</span></div>';
} 
?>
<?php
if(!empty($object->fechamodificacion)){
    echo '<div><span>fechamodificacion</span><span>' . $object->fechamodificacion . '</span></div>';
} 
?>
<?php
if(!empty($object->estado_id)){
    echo '<div><span>estado_id</span><span>' . $object->estado_id . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Alicuotas', array('controller' => 'alicuotas')); ?>
</p>

<h2><?php echo $object->descripcion; ?></h2>

<?php
if(!empty($object->condominio_id)){
    echo '<div><span>condominio_id</span><span>' . $object->condominio_id . '</span></div>';
} 
?>
<?php
if(!empty($object->fecha_hora)){
    echo '<div><span>fechahora</span><span>' . $object->fecha_hora . '</span></div>';
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
if(!empty($object->user_registro_id)){
    echo '<div><span>user_registro_id</span><span>' . $object->user_registro_id . '</span></div>';
} 
?>
<?php
if(!empty($object->estado_id)){
    echo '<div><span>estado_id</span><span>' . $object->estado_id . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Transaccions', array('controller' => 'transaccions')); ?>
</p>

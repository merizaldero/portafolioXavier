<h2><?php echo $object->nombre; ?></h2>

<$php
if(!empty($object->user_id)){
    echo '<div><span>user_id</span><span>' . $object->user_id . '</span></div>';
} 
?>
<$php
if(!empty($object->condominio_id)){
    echo '<div><span>condominio_id</span><span>' . $object->condominio_id . '</span></div>';
} 
?>
<$php
if(!empty($object->direccion)){
    echo '<div><span>direccioninterna</span><span>' . $object->direccion . '</span></div>';
} 
?>
<$php
if(!empty($object->estado_id)){
    echo '<div><span>estado_id</span><span>' . $object->estado_id . '</span></div>';
} 
?>
<$php
if(!empty($object->saldo_pagar)){
    echo '<div><span>saldoPorPagar</span><span>' . $object->saldo_pagar . '</span></div>';
} 
?>
<$php
if(!empty($object->fecha_saldo)){
    echo '<div><span>fechasaldo</span><span>' . $object->fecha_saldo . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Habitantes', array('controller' => 'habitantes')); ?>
</p>

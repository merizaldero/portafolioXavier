<h2><?php echo $object->nombre; ?></h2>

<?php
if(!empty($object->provincia)){
    echo '<div><span>provincia</span><span>' . $object->provincia . '</span></div>';
} 
?>
<?php
if(!empty($object->ciudad)){
    echo '<div><span>ciudad</span><span>' . $object->ciudad . '</span></div>';
} 
?>
<?php
if(!empty($object->direccion)){
    echo '<div><span>direccion</span><span>' . $object->direccion . '</span></div>';
} 
?>
<?php
if(!empty($object->tipoconstruccion_id)){
    echo '<div><span>tipoconstruccion_id</span><span>' . $object->tipoconstruccion_id . '</span></div>';
} 
?>
<?php
if(!empty($object->creador_id)){
    echo '<div><span>creador_id</span><span>' . $object->creador_id . '</span></div>';
} 
?>
<?php
if(!empty($object->administrador_id)){
    echo '<div><span>administrador_id</span><span>' . $object->administrador_id . '</span></div>';
} 
?>
<?php
if(!empty($object->saldo)){
    echo '<div><span>saldo</span><span>' . $object->saldo . '</span></div>';
} 
?>
<?php
if(!empty($object->fecha_saldo)){
    echo '<div><span>fechasaldo</span><span>' . $object->fecha_saldo . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Condominios', array('controller' => 'condominios')); ?>
</p>

<h2><?php echo $object->nombre; ?></h2>

<$php
if(!empty($object->habilitado)){
    echo '<div><span>habilitado</span><span>' . $object->habilitado . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Tipoconstruccions', array('controller' => 'tipoconstruccions')); ?>
</p>

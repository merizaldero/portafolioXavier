<h2><?php echo $object->descripcion; ?></h2>

<?php
if(!empty($object->path)){
    echo '<div><span>path</span><span>' . $object->path . '</span></div>';
} 
?>

<p>
  <?php echo $this->html->link('Todos los Documentosoportes', array('controller' => 'documentosoportes')); ?>
</p>

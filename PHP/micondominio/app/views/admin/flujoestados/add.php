<h2>Nuevo Flujo de Estados</h2>
<?php echo get_class($this->form).'XXX'; ?>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php 
echo $this->form->open_admin_table(); 
?>

<?php 
echo $this->form->input('nombre', ['label' => 'nombre']); 
//echo MvcFormTagsHelper::input('nombre', ['label' => 'Nombre'] );
?>
<?php 
echo $this->form->input('habilitado', ['type'=>'checkbox', 'label' => 'Habilitado', 'value'=>'1']);
//echo MvcFormTagsHelper::input('habilitado', ['type'=>'checkbox', 'label' => 'Habilitado']); 
?>

<?php 
echo $this->form->close_admin_table(); 
?>
<?php echo $this->form->end('Guardar'); ?>


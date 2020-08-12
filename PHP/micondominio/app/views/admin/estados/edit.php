<h2>Editar Estado</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->belongs_to_dropdown('flujoestado', $flujoestados, ['label' => 'Flujoestado_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->input('nombre', ['label' => 'Nombre']); ?>
<?php echo $this->form->input('estado_inicial', ['label' => 'Estadoinicial', 'type' => 'checkbox', 'value' => '1']); ?>
<?php echo $this->form->input('estado_final', ['label' => 'Estadofinal', 'type' => 'checkbox', 'value' => '1']); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>


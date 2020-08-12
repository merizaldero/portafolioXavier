<h2>Editar Transicionestado</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->belongs_to_dropdown('flujoestado', $flujoestados, ['label' => 'Flujoestado_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->input('descripcion', ['label' => 'Descripcion']); ?>
<?php echo $this->form->belongs_to_dropdown('estado_origen', $estados, ['label' => 'Estado_origen_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->belongs_to_dropdown('estado_destino', $estados, ['label' => 'Estado_destino_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->input('habilitado', ['label' => 'Habilitado', 'type' => 'checkbox', 'value' => '1']); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>


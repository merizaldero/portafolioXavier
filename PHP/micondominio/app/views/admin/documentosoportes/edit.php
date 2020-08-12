<h2>Editar Documentosoporte</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->input('descripcion', ['label' => 'Descripcion']); ?>
<?php echo $this->form->input('path', ['label' => 'Path']); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>


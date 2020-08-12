<h2>Nuevo Tipoconstruccion</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->input('nombre', ['label' => 'Nombre']); ?>
<?php echo $this->form->input('habilitado', ['label' => 'Habilitado', 'type' => 'checkbox', 'value' => '1']); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Guardar'); ?>


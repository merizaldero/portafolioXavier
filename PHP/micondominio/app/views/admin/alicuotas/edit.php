<h2>Editar Alicuota</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->belongs_to_dropdown('habitante', $habitantes, ['label' => 'Habitante_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->input('fecha', ['label' => 'Fecha']); ?>
<?php echo $this->form->input('monto', ['label' => 'Monto']); ?>
<?php echo $this->form->input('saldo', ['label' => 'Saldo']); ?>
<?php echo $this->form->input('user_creacion_id', ['label' => 'User_creacion_id']); ?>
<?php echo $this->form->input('fecharegistro', ['label' => 'Fecharegistro']); ?>
<?php echo $this->form->input('user_modificacion_id', ['label' => 'User_modificacion_id']); ?>
<?php echo $this->form->input('fechamodificacion', ['label' => 'Fechamodificacion']); ?>
<?php echo $this->form->belongs_to_dropdown('estado', $estados, ['label' => 'Estado_id', 'type' => 'checkbox', 'empty' => true ]); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>


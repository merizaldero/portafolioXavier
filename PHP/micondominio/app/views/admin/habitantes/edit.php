<h2>Editar Habitante</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->input('user_id', ['label' => 'User_id']); ?>
<?php echo $this->form->belongs_to_dropdown('condominio', $condominios, ['label' => 'Condominio_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->input('nombre', ['label' => 'Nombre']); ?>
<?php echo $this->form->input('direccion', ['label' => 'Direccioninterna']); ?>
<?php echo $this->form->input('estado_id', ['label' => 'Estado_id']); ?>
<?php echo $this->form->input('saldo_pagar', ['label' => 'Saldoporpagar']); ?>
<?php echo $this->form->input('fecha_saldo', ['label' => 'Fechasaldo']); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>


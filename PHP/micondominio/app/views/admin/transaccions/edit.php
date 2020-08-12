<h2>Editar Transaccion</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->belongs_to_dropdown('condominio', $condominios, ['label' => 'Condominio_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->input('fecha_hora', ['label' => 'Fechahora']); ?>
<?php echo $this->form->input('descripcion', ['label' => 'Descripcion']); ?>
<?php echo $this->form->input('monto', ['label' => 'Monto']); ?>
<?php echo $this->form->input('saldo', ['label' => 'Saldo']); ?>
<?php echo $this->form->input('user_registro_id', ['label' => 'User_registro_id']); ?>
<?php echo $this->form->belongs_to_dropdown('estado', $estados, ['label' => 'Estado_id', 'type' => 'checkbox', 'empty' => true ]); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>


<h2>Editar Gasto</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->belongs_to_dropdown('condominio', $condominios, ['label' => 'Condominio_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->input('fecha', ['label' => 'Fecha']); ?>
<?php echo $this->form->input('descripcion', ['label' => 'Descripcion']); ?>
<?php echo $this->form->input('monto', ['label' => 'Monto']); ?>
<?php echo $this->form->belongs_to_dropdown('habitante_abono', $habitantes, ['label' => 'Habitante_abono_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->belongs_to_dropdown('estado', $estados, ['label' => 'Estado_id', 'type' => 'checkbox', 'empty' => true ]); ?>
<?php echo $this->form->belongs_to_dropdown('transaccion', $transaccions, ['label' => 'Transaccion_id', 'type' => 'checkbox', 'empty' => true ]); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>


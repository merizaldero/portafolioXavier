<h2>Nuevo Condominio</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->input('nombre', ['label' => 'Nombre']); ?>
<?php echo $this->form->input('provincia', ['label' => 'Provincia']); ?>
<?php echo $this->form->input('ciudad', ['label' => 'Ciudad']); ?>
<?php echo $this->form->input('direccion', ['label' => 'Direccion']); ?>
<?php echo $this->form->input('tipoconstruccion_id', ['label' => 'Tipoconstruccion_id']); ?>
<?php echo $this->form->input('creador_id', ['label' => 'Creador_id']); ?>
<?php echo $this->form->input('administrador_id', ['label' => 'Administrador_id']); ?>
<?php echo $this->form->input('saldo', ['label' => 'Saldo']); ?>
<?php echo $this->form->input('fecha_saldo', ['label' => 'Fechasaldo']); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Guardar'); ?>


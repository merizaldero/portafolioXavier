<h2>Nuevo Condominio</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

<?php echo $this->form->input('nombre', ['label' => 'Nombre']); ?>
<?php echo $this->form->input('provincia', ['label' => 'Provincia']); ?>
<?php echo $this->form->input('ciudad', ['label' => 'Ciudad']); ?>
<?php echo $this->form->input('direccion', ['label' => 'Direccion']); ?>
<?php echo $this->form->belongs_to_dropdown('tipoconstruccion', $tipoconstruccions, ['label' => 'Tipo Construcci&oacute;n', 'empty' => true ]); ?>
<?php 
//echo $this->form->input('creador_id', ['label' => 'Creador_id']); 
echo $this->form->belongs_to_dropdown('creador', $usuarios, ['label' => 'Creador', 'empty' => true ]);
?>
<?php 
//echo $this->form->input('administrador_id', ['label' => 'Administrador_id']);
echo $this->form->belongs_to_dropdown('administrador', $usuarios, ['label' => 'Administrador', 'empty' => true ]);
?>
<?php echo $this->form->input('saldo', ['label' => 'Saldo']); ?>
<?php echo $this->form->input('fecha_saldo', ['label' => 'Fechasaldo']); ?>

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Guardar'); ?>


<h2>Condominios</h2>
<div>
<a class="button button-primary" href="<?php echo mvc_admin_url([ 'controller' => 'condominios', 'action' => 'add' ]) ?>">Agregar</a>
</div>
<table class="widefat post fixed striped" cellspacing="0">
    <thead>
        <?php 
        echo $this->html->admin_header_cells($this);
        ?>
    </thead>
    <tfoot>
        <?php 
        echo $this->html->admin_header_cells($this);
        ?>
    </tfoot>
    <tbody>
        <?php 
        echo $this->html->admin_table_cells($this, $objects, []);
        ?>
    </tbody>
    <?php // echo $this->pagination(); ?>
    
</table>
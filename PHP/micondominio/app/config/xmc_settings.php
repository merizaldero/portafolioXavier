<?php 

// app/settings/documentation_settings.php
class MiCondominioSettings extends MvcSettings {
    var $settings = array(
        'xmc_flujo_condominio_id' => array(
            'type' => 'select',
            'label' => 'Flujo Condominios',
            'options_method' => 'obtenerFlujos',
            'default' => 1
        ),
        'xmc_flujo_habitante_id' => array(
            'type' => 'select',
            'label' => 'Flujo Habitantes',
            'options_method' => 'obtenerFlujos',
            'default' => 1
        ),
        'xmc_flujo_alicuota_id' => array(
            'type' => 'select',
            'label' => 'Flujo Alicuotas',
            'options_method' => 'obtenerFlujos',
            'default' => 1
        ),
        'xmc_flujo_abono_id' => array(
            'type' => 'select',
            'label' => 'Flujo Abonos',
            'options_method' => 'obtenerFlujos',
            'default' => 1
        ),
        'xmc_flujo_gasto_id' => array(
            'type' => 'select',
            'label' => 'Flujo Gastos',
            'options_method' => 'obtenerFlujos',
            'default' => 1
        ),
    );
    public function obtenerFlujos() {
        $modelo = mvc_model('Flujoestado');
        $flujos = $modelo->find();
        $lista = array();
        foreach ($flujos as $flujo) {
            $lista[$flujo->id] = $flujo->nombre;
        }
        return $lista;
    }
}

?>
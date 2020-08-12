<?php

class TransicionestadosController extends MvcPublicController {

    var $default_columns = [
        'id' => [
            'label'=>'id',
            'value_method'=>'print_id'
        ],
        'flujoestado_id' => [
            'label'=>'flujoestado_id',
            'value_method'=>'print_flujoestado_id'
        ],
        'estado_origen_id' => [
            'label'=>'estado_origen_id',
            'value_method'=>'print_estado_origen_id'
        ],
        'estado_destino_id' => [
            'label'=>'estado_destino_id',
            'value_method'=>'print_estado_destino_id'
        ],
        'habilitado' => [
            'label'=>'habilitado',
            'value_method'=>'print_habilitado'
        ]
    ];

    public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_flujoestado_id ($object) {
        return empty($object->flujoestado_id) ? null : $object->flujoestado_id ; 
    }

        public function print_estado_origen_id ($object) {
        return empty($object->estado_origen_id) ? null : $object->estado_origen_id ; 
    }

        public function print_estado_destino_id ($object) {
        return empty($object->estado_destino_id) ? null : $object->estado_destino_id ; 
    }

        public function print_habilitado ($object) {
        return empty($object->habilitado) ? null : $object->habilitado ; 
    }

private function set_flujoestados() {
        $this->load_model('Flujoestado');
        $flujoestados = $this->Flujoestado->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('flujoestados', $flujoestados );
    }

private function set_estados() {
        $this->load_model('Estado');
        $estados = $this->Estado->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('estados', $estados );
    }

}

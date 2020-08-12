<?php
class AdminTransicionestadosController extends MvcAdminController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'flujoestado_id' => [
            'label'=>'Flujoestado_id',
            'value_method'=>'print_flujoestado_id'
        ],
        'descripcion' => [
            'label'=>'Descripcion',
            'value_method'=>'print_descripcion'
        ],
        'estado_origen_id' => [
            'label'=>'Estado_origen_id',
            'value_method'=>'print_estado_origen_id'
        ],
        'estado_destino_id' => [
            'label'=>'Estado_destino_id',
            'value_method'=>'print_estado_destino_id'
        ],
        'habilitado' => [
            'label'=>'Habilitado',
            'value_method'=>'print_habilitado'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_flujoestado_id ($object) {
        return empty($object->flujoestado_id) ? null : $object->flujoestado_id ; 
    }

        public function print_descripcion ($object) {
        return empty($object->descripcion) ? null : $object->descripcion ; 
    }

        public function print_estado_origen_id ($object) {
        return empty($object->estado_origen_id) ? null : $object->estado_origen_id ; 
    }

        public function print_estado_destino_id ($object) {
        return empty($object->estado_destino_id) ? null : $object->estado_destino_id ; 
    }

        public function print_habilitado ($object) {
        return ($object->habilitado == '1') ? 'SI' : 'NO' ; 
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


    public function add(){
        $this->set_flujoestados();
$this->set_estados();
//$this->set_estados();
        parent::add();
    }
    
    public function edit(){
        $this->set_flujoestados();
$this->set_estados();
//$this->set_estados();
        parent::edit();
    }
}
?>

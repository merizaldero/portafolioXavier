<?php
class EstadosController extends MvcPublicController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'flujoestado_id' => [
            'label'=>'Flujoestado_id',
            'value_method'=>'print_flujoestado_id'
        ],
        'nombre' => [
            'label'=>'Nombre',
            'value_method'=>'print_nombre'
        ],
        'activo_negocio' => [
            'label'=>'Activo_negocio',
            'value_method'=>'print_activo_negocio'
        ],
        'estado_inicial' => [
            'label'=>'Estadoinicial',
            'value_method'=>'print_estadoInicial'
        ],
        'estado_final' => [
            'label'=>'Estadofinal',
            'value_method'=>'print_estadoFinal'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_flujoestado_id ($object) {
        return empty($object->flujoestado_id) ? null : $object->flujoestado_id ; 
    }

        public function print_nombre ($object) {
        return empty($object->nombre) ? null : $object->nombre ; 
    }

    public function print_activo_negocio ($object) {
        return ($object->activo_negocio == '1') ? 'SI' : 'NO' ;
    }
        public function print_estadoInicial ($object) {
        return ($object->estado_inicial == '1') ? 'SI' : 'NO' ; 
    }

        public function print_estadoFinal ($object) {
        return ($object->estado_final == '1') ? 'SI' : 'NO' ; 
    }

private function set_flujoestados() {
        $this->loadModel('Flujoestado');
        $flujoestados = $this->Flujoestado->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('flujoestados', $flujoestados );
    }
   
}
?>

<?php
class AbonosController extends MvcPublicController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'habitante_id' => [
            'label'=>'Habitante_id',
            'value_method'=>'print_habitante_id'
        ],
        'fecha' => [
            'label'=>'Fecha',
            'value_method'=>'print_fecha'
        ],
        'monto' => [
            'label'=>'Monto',
            'value_method'=>'print_monto'
        ],
        'saldo' => [
            'label'=>'Saldo',
            'value_method'=>'print_saldo'
        ],
        'estado_id' => [
            'label'=>'Estado_id',
            'value_method'=>'print_estado_id'
        ],
        'transaccion_id' => [
            'label'=>'Transaccion_id',
            'value_method'=>'print_transaccion_id'
        ],
        'usuario_registro_id' => [
            'label'=>'Usuario_registro_id',
            'value_method'=>'print_usuario_registro_id'
        ],
        'fecharegistro' => [
            'label'=>'Fecharegistro',
            'value_method'=>'print_fecharegistro'
        ],
        'usuario_modificacion_id' => [
            'label'=>'Usuario_modificacion_id',
            'value_method'=>'print_usuario_modificacion_id'
        ],
        'fechamodificacion' => [
            'label'=>'Fechamodificacion',
            'value_method'=>'print_fechamodificacion'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_habitante_id ($object) {
        return empty($object->habitante_id) ? null : $object->habitante_id ; 
    }

        public function print_fecha ($object) {
        return empty($object->fecha) ? null : $object->fecha ; 
    }

        public function print_monto ($object) {
        return empty($object->monto) ? null : $object->monto ; 
    }

        public function print_saldo ($object) {
        return empty($object->saldo) ? null : $object->saldo ; 
    }

        public function print_estado_id ($object) {
        return empty($object->estado_id) ? null : $object->estado_id ; 
    }

        public function print_transaccion_id ($object) {
        return empty($object->transaccion_id) ? null : $object->transaccion_id ; 
    }

        public function print_usuario_registro_id ($object) {
        return empty($object->usuario_registro_id) ? null : $object->usuario_registro_id ; 
    }

        public function print_fecharegistro ($object) {
        return empty($object->fecharegistro) ? null : $object->fecharegistro ; 
    }

        public function print_usuario_modificacion_id ($object) {
        return empty($object->usuario_modificacion_id) ? null : $object->usuario_modificacion_id ; 
    }

        public function print_fechamodificacion ($object) {
        return empty($object->fechamodificacion) ? null : $object->fechamodificacion ; 
    }

private function set_habitantes() {
        $this->load_model('Habitante');
        $habitantes = $this->Habitante->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('habitantes', $habitantes );
    }

private function set_estados() {
        $this->load_model('Estado');
        $estados = $this->Estado->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('estados', $estados );
    }

private function set_transaccions() {
        $this->load_model('Transaccion');
        $transaccions = $this->Transaccion->find( ['selects' => ['id', 'descripcion'] ] );
        $this->set('transaccions', $transaccions );
    }
   
}
?>


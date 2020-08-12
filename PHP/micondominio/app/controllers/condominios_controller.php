<?php
class CondominiosController extends MvcPublicController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'nombre' => [
            'label'=>'Nombre',
            'value_method'=>'print_nombre'
        ],
        'provincia' => [
            'label'=>'Provincia',
            'value_method'=>'print_provincia'
        ],
        'ciudad' => [
            'label'=>'Ciudad',
            'value_method'=>'print_ciudad'
        ],
        'direccion' => [
            'label'=>'Direccion',
            'value_method'=>'print_direccion'
        ],
        'tipoconstruccion_id' => [
            'label'=>'Tipoconstruccion_id',
            'value_method'=>'print_tipoconstruccion_id'
        ],
        'creador_id' => [
            'label'=>'Creador_id',
            'value_method'=>'print_creador_id'
        ],
        'administrador_id' => [
            'label'=>'Administrador_id',
            'value_method'=>'print_administrador_id'
        ],
        'saldo' => [
            'label'=>'Saldo',
            'value_method'=>'print_saldo'
        ],
        'fecha_saldo' => [
            'label'=>'Fechasaldo',
            'value_method'=>'print_fechasaldo'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_nombre ($object) {
        return empty($object->nombre) ? null : $object->nombre ; 
    }

        public function print_provincia ($object) {
        return empty($object->provincia) ? null : $object->provincia ; 
    }

        public function print_ciudad ($object) {
        return empty($object->ciudad) ? null : $object->ciudad ; 
    }

        public function print_direccion ($object) {
        return empty($object->direccion) ? null : $object->direccion ; 
    }

        public function print_tipoconstruccion_id ($object) {
        return empty($object->tipoconstruccion_id) ? null : $object->tipoconstruccion_id ; 
    }

        public function print_creador_id ($object) {
        return empty($object->creador_id) ? null : $object->creador_id ; 
    }

        public function print_administrador_id ($object) {
        return empty($object->administrador_id) ? null : $object->administrador_id ; 
    }

        public function print_saldo ($object) {
        return empty($object->saldo) ? null : $object->saldo ; 
    }

        public function print_fechasaldo ($object) {
        return empty($object->fecha_saldo) ? null : $object->fecha_saldo ; 
    }

   
}
?>


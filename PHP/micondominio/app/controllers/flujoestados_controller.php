<?php

class FlujoestadosController extends MvcPublicController {

    var $default_columns = [
        'id' => [
            'label'=>'id',
            'value_method'=>'print_id'
        ],
        'nombre' => [
            'label'=>'nombre',
            'value_method'=>'print_nombre'
        ],
        'habilitado' => [
            'label'=>'habilitado',
            'value_method'=>'print_habilitado'
        ]
    ];
    
    public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

    public function print_nombre ($object) {
        return empty($object->nombre) ? null : $object->nombre ; 
    }

    public function print_habilitado ($object) {
        return empty($object->habilitado) ? null : $object->habilitado ; 
    }

}

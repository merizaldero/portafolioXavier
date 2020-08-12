<?php
class DocumentosoportesController extends MvcPublicController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'descripcion' => [
            'label'=>'Descripcion',
            'value_method'=>'print_descripcion'
        ],
        'path' => [
            'label'=>'Path',
            'value_method'=>'print_path'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_descripcion ($object) {
        return empty($object->descripcion) ? null : $object->descripcion ; 
    }

        public function print_path ($object) {
        return empty($object->path) ? null : $object->path ; 
    }

   
}
?>

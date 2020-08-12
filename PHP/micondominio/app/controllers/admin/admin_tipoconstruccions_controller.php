<?php
class AdminTipoconstruccionsController extends MvcAdminController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'nombre' => [
            'label'=>'Nombre',
            'value_method'=>'print_nombre'
        ],
        'habilitado' => [
            'label'=>'Habilitado',
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
        return ($object->habilitado == '1') ? 'SI' : 'NO' ; 
    }



    public function add(){
        
        parent::add();
    }
    
    public function edit(){
        
        parent::edit();
    }
}
?>


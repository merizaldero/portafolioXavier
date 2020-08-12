<?php

class AdminFlujoestadosController extends MvcAdminController {

    var $default_columns = array(
        'id' => array(
            'label'=>'Id',
            'value_method'=>'print_id'
        ),
        'nombre' => array(
            'label'=>'Nombre',
            'value_method'=>'print_nombre'
        ),
        'habilitado'  => array(
            'label'=>'Estado',
            'value_method'=>'print_habilitado'
        )
    );
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_nombre ($object) {
        return empty($object->nombre) ? null : $object->nombre ; 
    }

        public function print_habilitado ($object) {
        return ($object->habilitado == '1') ? 'Habilitado' : 'Deshabilitado' ; 
    }


/*
    public function add(){
        $object = ['id'=>null , 'nombre'=>'Flujo1', 'habilitado'=>'1'];
        $this->set('object', $object);
        //$this->set_object();
	//$this->create();
    }
    
//    public function edit(){
        
        //$this->verify_id_param();
        //$this->set_object();
        //$this->create_or_save();
//    }
*/

}

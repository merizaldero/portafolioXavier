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
        ),
        'ver_flujo'  => array(
            'label'=>'Flujo',
            'value_method'=>'print_link_ver_flujo'
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

    public function print_link_ver_flujo($object){
        return '<a href="' . mvc_admin_url( ['controller' => 'flujoestados','action' => 'ver_flujo', 'id' => $object->id ]) . '">Ver Flujo</a>';
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
        
    public function ver_flujo(){

        $this->set_object();        
        $objeto = $this->object;        
        
        $this->load_model('Estado');
        $this->load_model('Transicionestado');
        
        $transiciones = $this->Transicionestado->find(['conditions' => [ 'flujoestado_id' => $objeto->id ] ]);
        //$transiciones = $this->Transicionestado->find();
        $estados = $this->Estado->find(['conditions' => [ 'flujoestado_id' => $objeto->id ] ]);
        //$estados = $this->Estado->find();
        $this->set('estados', $estados);
        $this->set('transiciones', $transiciones);
        
    }
    
    private function crear_editar_hijo($model){
        
        $flujoestado = $this->object;
        
        if (!empty($this->params['data'][ $model->name ])) {
            $object = $this->params['data'][ $model->name ];
            $object->flujoestado_id = $flujoestado->id;
            // params['data'][ $model->name ]->flujoestado_id = $flujoestado->id;
            if (empty($object['id'])) {
                if($model->create($this->params['data'])) {
                    $id = $model->insert_id;
                    //$url = MvcRouter::admin_url(array('controller' => $this->name, 'action' => 'edit', 'id' => $id));
                    $this->flash('notice', __('Successfully created!', 'wpmvc'));
                    //$this->redirect($url);
                } else {
                    $this->flash('error', $model->validation_error_html);
                    //$this->set_object();
                }
            } else {
                if ($model->save($this->params['data'])) {
                    $this->flash('notice', __('Successfully saved!', 'wpvmc'));
                    //$this->refresh();
                } else {
                    $this->flash('error', $model->validation_error_html);
                }
            }
        }
        $url = MvcRouter::admin_url(array('controller' => $this->name, 'action' => 'ver_flujo', 'id' => $flujoestado->id ));
        $this->redirect($url);
    }
    
    public function crear_editar_estado(){
        $this->set_object();
        $this->load_model("Estado");
        $this->crear_editar_hijo( $this->Estado );
        
    }
    
    public function crear_editar_transicion(){
        $this->set_object();
        $this->load_model("Transicionestado");
        $this->crear_editar_hijo( $this->Transicionestado );
    }

}

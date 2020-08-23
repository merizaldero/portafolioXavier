<?php
class AdminCondominiosController extends MvcAdminController {
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
            'label'=>'Tipo Construccion',
            'value_method'=>'print_tipoconstruccion_id'
        ],
        'creador_id' => [
            'label'=>'Creador',
            'value_method'=>'print_creador_id'
        ],
        'administrador_id' => [
            'label'=>'Administrador',
            'value_method'=>'print_administrador_id'
        ],
        'saldo' => [
            'label'=>'Saldo',
            'value_method'=>'print_saldo'
        ],
        'fecha_saldo' => [
            'label'=>'Fecha Saldo',
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

    public function buscar_tipo_construccion($tipoconstruccion_id){
        foreach ($this->tipoconstruccions as $tipo){
            if ($tipo->id == $tipoconstruccion_id){
                return $tipo;
            }
        }
        return null;
    }
    
    public function print_tipoconstruccion_id ($object) {
        $tipo = $this->buscar_tipo_construccion($object->tipoconstruccion_id);
        return is_null($tipo) ? null : $tipo->nombre ;
    }
    
    public function buscar_usuario($user_id){
        foreach ($this->usuarios as $usuario){
            if ($usuario->id == $user_id){
                return $usuario;
            }
        }
        return null;
    }
    
    public function print_creador_id ($object) {
        $usuario = $this->buscar_usuario($object->creador_id);
        return is_null($usuario) ? null : $usuario->name ;
    }
    
    public function print_administrador_id ($object) {
        $usuario = $this->buscar_usuario($object->administrador_id);
        return is_null($usuario) ? null : $usuario->name ;
    }
    
    public function print_saldo ($object) {
        return empty($object->saldo) ? null : $object->saldo ;
    }
    
    public function print_fechasaldo ($object) {
        return empty($object->fecha_saldo) ? null : $object->fecha_saldo ;
    }
    
    var $before = array('cargar_usuarios');
    
    public function cargar_usuarios(){
        //$this->load_model('MvcUser');
        $user_model = mvc_model('MvcUser');
        //$usuarios = $this->MvcUser->find();
        $usuarios = $user_model->find();
        $this->set('usuarios', $usuarios);
        $this->load_model('Tipoconstruccion');
        $tiposConstruccion = $this->Tipoconstruccion->find();
        $this->set('tipoconstruccions', $tiposConstruccion);
    }



    public function add(){
        
        parent::add();
    }
    
    public function edit(){
        
        parent::edit();
    }
}
?>


<?php
class AdminTransaccionsController extends MvcAdminController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'condominio_id' => [
            'label'=>'Condominio_id',
            'value_method'=>'print_condominio_id'
        ],
        'fecha_hora' => [
            'label'=>'Fechahora',
            'value_method'=>'print_fechahora'
        ],
        'descripcion' => [
            'label'=>'Descripcion',
            'value_method'=>'print_descripcion'
        ],
        'monto' => [
            'label'=>'Monto',
            'value_method'=>'print_monto'
        ],
        'saldo' => [
            'label'=>'Saldo',
            'value_method'=>'print_saldo'
        ],
        'user_registro_id' => [
            'label'=>'User_registro_id',
            'value_method'=>'print_user_registro_id'
        ],
        'estado_id' => [
            'label'=>'Estado_id',
            'value_method'=>'print_estado_id'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_condominio_id ($object) {
        return empty($object->condominio_id) ? null : $object->condominio_id ; 
    }

        public function print_fechahora ($object) {
        return empty($object->fecha_hora) ? null : $object->fecha_hora ; 
    }

        public function print_descripcion ($object) {
        return empty($object->descripcion) ? null : $object->descripcion ; 
    }

        public function print_monto ($object) {
        return empty($object->monto) ? null : $object->monto ; 
    }

        public function print_saldo ($object) {
        return empty($object->saldo) ? null : $object->saldo ; 
    }

        public function print_user_registro_id ($object) {
        return empty($object->user_registro_id) ? null : $object->user_registro_id ; 
    }

        public function print_estado_id ($object) {
        return empty($object->estado_id) ? null : $object->estado_id ; 
    }

private function set_condominios() {
        $this->load_model('Condominio');
        $condominios = $this->Condominio->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('condominios', $condominios );
    }

private function set_estados() {
        $this->load_model('Estado');
        $estados = $this->Estado->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('estados', $estados );
    }


    public function add(){
        $this->set_condominios();
$this->set_estados();
        parent::add();
    }
    
    public function edit(){
        $this->set_condominios();
$this->set_estados();
        parent::edit();
    }
}
?>


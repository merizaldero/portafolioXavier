<?php
class AdminHabitantesController extends MvcAdminController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'user_id' => [
            'label'=>'User_id',
            'value_method'=>'print_user_id'
        ],
        'condominio_id' => [
            'label'=>'Condominio_id',
            'value_method'=>'print_condominio_id'
        ],
        'nombre' => [
            'label'=>'Nombre',
            'value_method'=>'print_nombre'
        ],
        'direccion' => [
            'label'=>'Direccioninterna',
            'value_method'=>'print_direccioninterna'
        ],
        'estado_id' => [
            'label'=>'Estado_id',
            'value_method'=>'print_estado_id'
        ],
        'saldo_pagar' => [
            'label'=>'Saldoporpagar',
            'value_method'=>'print_saldoPorPagar'
        ],
        'fecha_saldo' => [
            'label'=>'Fechasaldo',
            'value_method'=>'print_fechasaldo'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_user_id ($object) {
        return empty($object->user_id) ? null : $object->user_id ; 
    }

        public function print_condominio_id ($object) {
        return empty($object->condominio_id) ? null : $object->condominio_id ; 
    }

        public function print_nombre ($object) {
        return empty($object->nombre) ? null : $object->nombre ; 
    }

        public function print_direccioninterna ($object) {
        return empty($object->direccion) ? null : $object->direccion ; 
    }

        public function print_estado_id ($object) {
        return empty($object->estado_id) ? null : $object->estado_id ; 
    }

        public function print_saldoPorPagar ($object) {
        return empty($object->saldo_pagar) ? null : $object->saldo_pagar ; 
    }

        public function print_fechasaldo ($object) {
        return empty($object->fecha_saldo) ? null : $object->fecha_saldo ; 
    }

private function set_condominios() {
        $this->load_model('Condominio');
        $condominios = $this->Condominio->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('condominios', $condominios );
    }


    public function add(){
        $this->set_condominios();
        parent::add();
    }
    
    public function edit(){
        $this->set_condominios();
        parent::edit();
    }
}
?>


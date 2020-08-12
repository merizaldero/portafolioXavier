<?php
class AdminGastosController extends MvcAdminController {
    var $default_columns = [
        'id' => [
            'label'=>'Id',
            'value_method'=>'print_id'
        ],
        'condominio_id' => [
            'label'=>'Condominio_id',
            'value_method'=>'print_condominio_id'
        ],
        'fecha' => [
            'label'=>'Fecha',
            'value_method'=>'print_fecha'
        ],
        'descripcion' => [
            'label'=>'Descripcion',
            'value_method'=>'print_descripcion'
        ],
        'monto' => [
            'label'=>'Monto',
            'value_method'=>'print_monto'
        ],
        'habitante_abono_id' => [
            'label'=>'Habitante_abono_id',
            'value_method'=>'print_habitante_abono_id'
        ],
        'estado_id' => [
            'label'=>'Estado_id',
            'value_method'=>'print_estado_id'
        ],
        'transaccion_id' => [
            'label'=>'Transaccion_id',
            'value_method'=>'print_transaccion_id'
        ]
    ];
public function print_id ($object) {
        return empty($object->id) ? null : $object->id ; 
    }

        public function print_condominio_id ($object) {
        return empty($object->condominio_id) ? null : $object->condominio_id ; 
    }

        public function print_fecha ($object) {
        return empty($object->fecha) ? null : $object->fecha ; 
    }

        public function print_descripcion ($object) {
        return empty($object->descripcion) ? null : $object->descripcion ; 
    }

        public function print_monto ($object) {
        return empty($object->monto) ? null : $object->monto ; 
    }

        public function print_habitante_abono_id ($object) {
        return empty($object->habitante_abono_id) ? null : $object->habitante_abono_id ; 
    }

        public function print_estado_id ($object) {
        return empty($object->estado_id) ? null : $object->estado_id ; 
    }

        public function print_transaccion_id ($object) {
        return empty($object->transaccion_id) ? null : $object->transaccion_id ; 
    }

private function set_condominios() {
        $this->load_model('Condominio');
        $condominios = $this->Condominio->find( ['selects' => ['id', 'nombre'] ] );
        $this->set('condominios', $condominios );
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


    public function add(){
        $this->set_condominios();
$this->set_habitantes();
$this->set_estados();
$this->set_transaccions();
        parent::add();
    }
    
    public function edit(){
        $this->set_condominios();
$this->set_habitantes();
$this->set_estados();
$this->set_transaccions();
        parent::edit();
    }
}
?>


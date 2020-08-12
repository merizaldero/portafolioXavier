<?php

class Gasto extends MvcModel {

    var $display_field = 'descripcion';
    var $table = '{prefix}xmc_GST';    
    var $primary_key = 'id';
    var $selects = ['id', 'condominio_id', 'fecha', 'descripcion', 'monto', 'habitante_abono_id', 'estado_id', 'transaccion_id'];
    var $validate = [
        'condominio_id' => [
            'message' => 'condominio_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'fecha' => [
            'message' => 'fecha no v&aacute;lido',
            'required' => true,
            'pattern' => '/^([1-9][0-9]{3})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])?$/'
        ],
        'descripcion' => [
            'message' => 'descripcion no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'monto' => [
            'message' => 'monto no v&aacute;lido',
            'required' => true,
            'rule' => 'numeric'
        ],
        'habitante_abono_id' => [
            'message' => 'habitante_abono_id no v&aacute;lido',
            'required' => false,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'estado_id' => [
            'message' => 'estado_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'transaccion_id' => [
            'message' => 'transaccion_id no v&aacute;lido',
            'required' => false,
            'pattern' => '/^(\+|-)?\d+$/'
        ]
    ];
    var $per_page = 7;
    var $belongs_to = [
        'Condominio' => [ 'foreign_key' => 'condominio_id' ],
        'Habitante' => [ 'foreign_key' => 'habitante_abono_id' ],
        'Estado' => [ 'foreign_key' => 'estado_id' ],
        'Transaccion' => [ 'foreign_key' => 'transaccion_id' ]
    ];
}

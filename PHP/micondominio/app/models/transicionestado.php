<?php

class Transicionestado extends MvcModel {

    var $display_field = 'descripcion';
    var $table = '{prefix}xmc_TRNSCNSTD';    
    var $primary_key = 'id';
    var $selects = ['id', 'flujoestado_id', 'estado_origen_id', 'estado_destino_id', 'habilitado'];
    var $validate = [
        'flujoestado_id' => [
            'message' => 'flujoestado_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'descripcion' => [
            'message' => 'descripcion no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'estado_origen_id' => [
            'message' => 'estado_origen_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'estado_destino_id' => [
            'message' => 'estado_destino_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'habilitado' => [
            'message' => 'habilitado no v&aacute;lido',
            'required' => true,
            'pattern' => '/^1|0$/'
        ]
    ];
    var $per_page = 7;
    var $belongs_to = [
        'Flujoestado' => [ 'foreign_key' => 'flujoestado_id' ],
        //'Estado' => [ 'foreign_key' => 'estado_origen_id' ],
        'Estado' => [ 'foreign_key' => 'estado_destino_id' ]
    ];
}

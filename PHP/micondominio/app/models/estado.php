<?php

class Estado extends MvcModel {

    var $table = '{prefix}xmc_ESTD';    
    var $primary_key = 'id';
    var $selects = ['id', 'flujoestado_id', 'nombre', 'estado_inicial', 'estado_final'];
    var $validate = [
        'flujoestado_id' => [
            'message' => 'flujoestado_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'nombre' => [
            'message' => 'nombre no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'estado_inicial' => [
            'message' => 'estadoInicial no v&aacute;lido',
            'required' => true,
            'pattern' => '/^1|0$/'
        ],
        'estado_final' => [
            'message' => 'estadoFinal no v&aacute;lido',
            'required' => true,
            'pattern' => '/^1|0$/'
        ]
    ];
    var $belongs_to = [
        'Flujoestado' => [ 'foreign_key' => 'flujoestado_id' ]
    ];
    var $per_page = 7;
    var $display_field = 'nombre';

}

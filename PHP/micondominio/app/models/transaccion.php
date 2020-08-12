<?php

class Transaccion extends MvcModel {

    var $display_field = 'descripcion';
    var $table = '{prefix}xmc_TRNSCCN';    
    var $primary_key = 'id';
    var $selects = ['id', 'condominio_id', 'fecha_hora', 'descripcion', 'monto', 'saldo', 'user_registro_id', 'estado_id'];
    var $validate = [
        'condominio_id' => [
            'message' => 'condominio_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'fecha_hora' => [
            'message' => 'fechahora no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(?:[\+-]?\d{4}(?!\d{2}\b))(?:(-?)(?:(?:0[1-9]|1[0-2])(?:\1(?:[12]\d|0[1-9]|3[01]))?|W(?:[0-4]\d|5[0-2])(?:-?[1-7])?|(?:00[1-9]|0[1-9]\d|[12]\d{2}|3(?:[0-5]\d|6[1-6])))(?:[T\s](?:(?:(?:[01]\d|2[0-3])(?:(:?)[0-5]\d)?|24\:?00)(?:[\.,]\d+(?!:))?)?(?:\2[0-5]\d(?:[\.,]\d+)?)?(?:[zZ]|(?:[\+-])(?:[01]\d|2[0-3]):?(?:[0-5]\d)?)?)?)?$/'
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
        'saldo' => [
            'message' => 'saldo no v&aacute;lido',
            'required' => true,
            'rule' => 'numeric'
        ],
        'user_registro_id' => [
            'message' => 'user_registro_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'estado_id' => [
            'message' => 'estado_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ]
    ];
    var $per_page = 7;
    var $belongs_to = [
        'Condominio' => [ 'foreign_key' => 'condominio_id' ],
        'Estado' => [ 'foreign_key' => 'estado_id' ]
    ];

}

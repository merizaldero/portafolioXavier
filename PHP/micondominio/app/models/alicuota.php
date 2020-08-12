<?php

class Alicuota extends MvcModel {

    var $display_field = 'fecha';
    var $table = '{prefix}xmc_ALCT';    
    var $primary_key = 'id';
    var $selects = ['id', 'habitante_id', 'fecha', 'monto', 'saldo', 'user_creacion_id', 'fecharegistro', 'user_modificacion_id', 'fechamodificacion', 'estado_id'];
    var $validate = [
        'habitante_id' => [
            'message' => 'habitante_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'fecha' => [
            'message' => 'fecha no v&aacute;lido',
            'required' => true,
            'pattern' => '/^([1-9][0-9]{3})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])?$/'
        ],
        'monto' => [
            'message' => 'monto no v&aacute;lido',
            'required' => true,
            'rule' => 'numeric'
        ],
        'saldo' => [
            'message' => 'saldo no v&aacute;lido',
            'required' => false,
            'rule' => 'alphanumeric'
        ],
        'user_creacion_id' => [
            'message' => 'user_creacion_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'fecharegistro' => [
            'message' => 'fecharegistro no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(?:[\+-]?\d{4}(?!\d{2}\b))(?:(-?)(?:(?:0[1-9]|1[0-2])(?:\1(?:[12]\d|0[1-9]|3[01]))?|W(?:[0-4]\d|5[0-2])(?:-?[1-7])?|(?:00[1-9]|0[1-9]\d|[12]\d{2}|3(?:[0-5]\d|6[1-6])))(?:[T\s](?:(?:(?:[01]\d|2[0-3])(?:(:?)[0-5]\d)?|24\:?00)(?:[\.,]\d+(?!:))?)?(?:\2[0-5]\d(?:[\.,]\d+)?)?(?:[zZ]|(?:[\+-])(?:[01]\d|2[0-3]):?(?:[0-5]\d)?)?)?)?$/'
        ],
        'user_modificacion_id' => [
            'message' => 'user_modificacion_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'fechamodificacion' => [
            'message' => 'fechamodificacion no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(?:[\+-]?\d{4}(?!\d{2}\b))(?:(-?)(?:(?:0[1-9]|1[0-2])(?:\1(?:[12]\d|0[1-9]|3[01]))?|W(?:[0-4]\d|5[0-2])(?:-?[1-7])?|(?:00[1-9]|0[1-9]\d|[12]\d{2}|3(?:[0-5]\d|6[1-6])))(?:[T\s](?:(?:(?:[01]\d|2[0-3])(?:(:?)[0-5]\d)?|24\:?00)(?:[\.,]\d+(?!:))?)?(?:\2[0-5]\d(?:[\.,]\d+)?)?(?:[zZ]|(?:[\+-])(?:[01]\d|2[0-3]):?(?:[0-5]\d)?)?)?)?$/'
        ],
        'estado_id' => [
            'message' => 'estado_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ]
    ];
    var $per_page = 7;
    var $belongs_to = [
        'Habitante' => [ 'foreign_key' => 'habitante_id' ],
        'Estado' => [ 'foreign_key' => 'estado_id' ]
    ];
}

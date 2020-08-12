<?php

class Condominio extends MvcModel {

    var $display_field = 'nombre';
    var $table = '{prefix}xmc_CNDMN';    
    var $primary_key = 'id';
    var $selects = ['id', 'nombre', 'provincia', 'ciudad', 'direccion', 'tipoconstruccion_id', 'creador_id', 'administrador_id', 'saldo', 'fecha_saldo'];
    var $validate = [
        'nombre' => [
            'message' => 'nombre no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'provincia' => [
            'message' => 'provincia no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'ciudad' => [
            'message' => 'ciudad no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'direccion' => [
            'message' => 'direccion no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'tipoconstruccion_id' => [
            'message' => 'tipoconstruccion_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'creador_id' => [
            'message' => 'creador_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'administrador_id' => [
            'message' => 'administrador_id no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(\+|-)?\d+$/'
        ],
        'saldo' => [
            'message' => 'saldo no v&aacute;lido',
            'required' => true,
            'rule' => 'numeric'
        ],
        'fecha_saldo' => [
            'message' => 'fechasaldo no v&aacute;lido',
            'required' => true,
            'pattern' => '/^(?:[\+-]?\d{4}(?!\d{2}\b))(?:(-?)(?:(?:0[1-9]|1[0-2])(?:\1(?:[12]\d|0[1-9]|3[01]))?|W(?:[0-4]\d|5[0-2])(?:-?[1-7])?|(?:00[1-9]|0[1-9]\d|[12]\d{2}|3(?:[0-5]\d|6[1-6])))(?:[T\s](?:(?:(?:[01]\d|2[0-3])(?:(:?)[0-5]\d)?|24\:?00)(?:[\.,]\d+(?!:))?)?(?:\2[0-5]\d(?:[\.,]\d+)?)?(?:[zZ]|(?:[\+-])(?:[01]\d|2[0-3]):?(?:[0-5]\d)?)?)?)?$/'
        ]
    ];
    var $per_page = 7;
}

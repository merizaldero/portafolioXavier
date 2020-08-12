<?php

class Documentosoporte extends MvcModel {

    var $display_field = 'descripcion';
    var $table = '{prefix}xmc_DCMNTSPRT';    
    var $primary_key = 'id';
    var $selects = ['id', 'descripcion', 'path'];
    var $validate = [
        'descripcion' => [
            'message' => 'descripcion no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'path' => [
            'message' => 'path no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ]
    ];
    var $per_page = 7;

}

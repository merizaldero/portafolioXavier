<?php

MvcConfiguration::set(array(
    'Debug' => false
));

MvcConfiguration::append(array(
    'AdminPages' => array(
        'xmc_mains' => [ 'label' => 'Mi Condominio EC' ,
            'ver_flujoestados' => ['label' => 'Flujos de Estados'],
            'ver_tipoconstruccions' => ['label' => 'Tipos de Construccion'],
            'ver_condominios' => ['label' => 'Condominios'],
            'ver_habitantes' => ['label' => 'Habitantes', 'in_menu' => false ]
        ],
        
        'flujoestados' => [ 'label'=>'Flujos de Estados' ,'order' => 1, 'parent_slug' => 'admin.php?page=mvc_xmc_mains'
            ,'add' => [ 'label' => 'Agregar' ,'order' => 1 ]
            ,'edit' => [ 'label' => 'Editar' , 'in_menu' => false ]
            ,'delete' => [ 'label' => 'Eliminar' , 'in_menu' => false ]
            ,'ver_flujo' => [ 'label' => 'Ver Flujo' , 'in_menu' => false ]
            ,'crear_editar_estado' => [ 'label' => 'Editar Estado' , 'in_menu' => false ]
            ,'crear_editar_transicion' => [ 'label' => 'Editar Transicion' , 'in_menu' => false ]
        ],
        'transicionestados' => [ 'label' => 'Transiciones de Estados', 'in_menu'=>false , 'parent_slug' => 'admin.php?page=mvc_flujoestados'],
        'estados' => [ 'in_menu'=>false , 'parent_slug' => 'admin.php?page=mvc_flujoestados'],
        
        'documentosoportes' => [ 'label' => 'Documentoss de Soporte', 'order' => 2 , 'parent_slug' => 'admin.php?page=mvc_xmc_mains'],

        'tipoconstruccions' => [ 'label' => 'Tipos de Construccion', 'order' => 3 , 'parent_slug' => 'admin.php?page=mvc_xmc_mains'
            ,'add' => [ 'label' => 'Agregar' ,'order' => 1 ]
            ,'edit' => [ 'label' => 'Editar' , 'in_menu' => false ]
            ,'delete' => [ 'label' => 'Eliminar' , 'in_menu' => false ]
        ],        
        
        'condominios' => [ 'in_menu'=>false , 'order' => 4 , 'parent_slug' => 'admin.php?page=mvc_xmc_mains'
            ,'add' => [ 'label' => 'Agregar' ,'order' => 1 ]
            ,'edit' => [ 'label' => 'Editar' , 'in_menu' => false ]
            ,'delete' => [ 'label' => 'Eliminar' , 'in_menu' => false ]
        ],
        'gastos' => [ 'in_menu'=>false , 'parent_slug' => 'admin.php?page=mvc_condominios' ],
        'transaccions' => [ 'label' => 'Transacciones', 'in_menu'=>false , 'parent_slug' => 'admin.php?page=mvc_condominios' ],
        
        'habitantes' => [ 'in_menu'=>false , 'parent_slug' => 'admin.php?page=mvc_condominios' , 'parent_slug' => 'admin.php?page=mvc_xmc_mains'],
        'alicuotas' => [ 'in_menu'=>false , 'parent_slug' => 'admin.php?page=mvc_habitantes' ],
        'abonos' => [ 'in_menu'=>false , 'parent_slug' => 'admin.php?page=mvc_habitantes' ],
        
        
        
    )
));


?>
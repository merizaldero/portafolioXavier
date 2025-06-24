<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{titulo}}</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <script src="/static/js/bootstrap.bundle.min.js"></script>
% if estilo != "" :
    <style>
        {{estilo}}
    </style>
% end
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand fixed-top border-bottom justify-content-between w-100 p-0" style="background-color:#8888FF">
        <a class="navbar-brand ml-5" href="/">{{titulo}}</a>
        <div class="collapse navbar-collapse justify-content-end" id="collapsibleNavbar">
% if usuario:
            <ul class="navbar-nav w-25">
                <li class="nav-item">
                    <a class="nav-link" href="/xpd_alicuotas/condominios">
                        Condominios
                    </a>    
                </li>

% if usuario and 'roles' in usuario.keys() and 'Administrador' in usuario['roles']:
                <li class="nav-item">
                    <a class="nav-link" href="/xpd_alicuotas/admin">
                         |Administrar|
                    </a>
                </li>
% end
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        {{usuario['username']}}
                    </a>
                    <ul class="dropdown-menu" id="user_menu">
                        <li><a class="dropdown-item" href="/cambiar_clave">Cambiar Clave</a></li>
                        <li><a class="dropdown-item" href="/logout">Cerrar Sesion</a></li>
                    </ul>
                </li>
            </ul>
% end            
        </div>
    </nav>
    <div class="container">
        <div class="mt-3 mb-4">&nbsp;</div>

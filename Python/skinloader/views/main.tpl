<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Mis Avatares</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <script src="/static/js/bootstrap.bundle.min.js"></script>
    <style>
        body{
            background-color: #88cccc;
        }
    </style>
  </head>
  <body> 
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Skins Minetest</a>
        <span class="navbar-text">
          <select id="selGrupo" name="selGrupo" class="form-select">            
          </select>
        </span>        
      </div>
    </nav>

    <div class="container">

%if tipo_mensaje != '':
<div class="alert alert-{{tipo_mensaje}} alert-dismissible">
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  {{mensaje}}
</div>
%end

      <div id="divAvatares" class="mt-3 list-group">
        <div id="btnNuevo" class="list-group-item nuevo-avatar">+ Nuevo Avatar</div>
      </div>
   </div>

    <script src="/js/skinloader.js"></script>
  </body>
</html>

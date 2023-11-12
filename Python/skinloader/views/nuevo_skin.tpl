<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Avatar</title>
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
        <a class="navbar-brand" href="/">&#8678;</a>        
      </div>
    </nav>

<div class="container">

%if tipo_mensaje != '':
<div class="alert alert-{{tipo_mensaje}} alert-dismissible">
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  {{mensaje}}
</div>
%end

<h1>Nuevo Skin</h1>
<form method="POST" id="form_avatar" action="/nuevo_skin" enctype="multipart/form-data">
  <div class="row">
    <div class="col-md-12 input-group mb-3">
      <label for="txt_grupo" class="input-group-text">Grupo: </label>
      <input type="text" class="form-control" name="txt_grupo" id="txt_grupo" maxlength="32" readonly value="{{grupo}}">
    </div>
  </div>

  <div class="row">
    <div class="col-md-12 input-group mb-3">
      <label for="txt_nombre" class="input-group-text">Nombre: </label>
      <input type="text" class="form-control" name="txt_nombre" id="txt_nombre" maxlength="32" value="{{nombre}}">
    </div>
  </div>

  <div class="row">
    <div class="col-md-12 input-group mb-3">
      <label for="txt_archivo" class="input-group-text">Archivo: </label>
      <input type="file" class="form-control" name ="archivo" id="archivo">
    </div>
  </div>

  <div class="row">
    <div class="col-md-12 btn-group mb-3">
      <input type="submit" class="btn btn-primary" name ="submit" value="Enviar">
      <a class="btn btn-secondary" href="/">Cancelar</a>
    </div>
  </div>

</form>

</div>
<script src="/static/js/nuevo_skin.js"></script>
</body>
</html>
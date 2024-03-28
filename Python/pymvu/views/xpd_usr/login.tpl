<!DOCTYPE html>
<html lang="es" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <style>

.card {
    margin-top: 20px;
}

    </style>
</head>
<body>
    <div class="container">

% if lvl != "":
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        Iniciar Sesi&oacute;n
                    </div>
                    <div class="card-body">
                        <form action="/login" method="post">
                            <div class="form-group">
                                <label for="username">Usuario</label>

<input type="text" class="form-control" id="username" name="username" value="{{username}}" placeholder="Nombre de Usuario">

                            </div>
                            <div class="form-group">
                                <label for="password">Contrase&ntilde;a</label>
                                <input type="password" class="form-control" id="password" name="password" placeholder="Ingrese su contraseña">
                            </div>
                            <button type="submit" class="mt-3 btn btn-primary">Iniciar Sesi&oacute;n</button>
                        </form>
                        <a href="/registrar_usuario" class="mt-3">¿No tienes una cuenta? Reg&iacute;strate aqu&iacute;</a>
                        <br>
                        <a href="/solicitar_recuperar_clave" class="mt-3">¿Olvidaste tu contrase&nacute;a?</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>

<!DOCTYPE html>
<html lang="es" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
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
                        Registro de Usuario
                    </div>
                    <div class="card-body">
                        <form action="/registrar_usuario" method="post">
                            <div class="form-group">
                                <label for="username">Nombre de usuario</label>
                                <input type="text" class="form-control" id="username" name="username" placeholder="Ingrese su nombre de usuario" value="{{usuario['username']}}" required>
                            </div>
                            <div class="form-group">
                                <label for="email">Correo electr&oacute;nico</label>
                                <input type="email" class="form-control" id="email" name="email" placeholder="Ingrese su correo electrónico" value="{{usuario['email']}}" required>
                            </div>
                            <div class="form-group">
                                <label for="password">Contrase&nacute;a</label>
                                <input type="password" class="form-control" id="password" name="password" placeholder="Ingrese su contraseña" value="{{usuario['password']}}" required>
                            </div>
                            <div class="form-group">
                                <label for="password1">Confirmar contrase&nacute;a</label>
                                <input type="password" class="form-control" id="password1" name="password1" placeholder="Confirme su contraseña" value="{{usuario['password1']}}" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Registrarse</button>
                            <a href="/" class="btn btn-secondary">Cancelar</a>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>

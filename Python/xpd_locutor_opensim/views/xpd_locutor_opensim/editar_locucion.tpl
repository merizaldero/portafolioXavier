% include('xpd_locutor_opensim/encabezado.tpl', titulo="Editar Locución", usuario = usuario, estilo ="")

<h1>Editar Locución</h1>

% if lvl != '':
    <div class="alert alert-{{lvl}}">
    {{mensaje}}
    </div>
% end

<form method="POST" enctype="multipart/form-data">
    <div class="card">
        <div class="card-body container">
            <div class="row">
                <span class="col">
                    Texto:
                </span>
                <span class="col">
                    {{locucion['texto']}}
                </span>
            </div>
            <div class="row">
                <span class="col">
                    Archivo:
                </div>
                <span class="col">
                    <input class="form-control" type="file" name="archivo">
                </span>
            </div>            
        </div>
        <div class="card-footer">
            <input class="btn btn-primary" type="submit" name="accion" value="Actualizar">
        </div>
    </div>
</form>

% include('xpd_locutor_opensim/pie.tpl', usuario = usuario)
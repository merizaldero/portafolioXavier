% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Configuracion", usuario = usuario, estilo =".card-header{font-weight:bold;color:#ffffff;background-color:#880088;} .card-footer{background-color:#ff00ff;}")
<div class="container">
    <div class="row">
    <div class="col-8">

        <div class="card mt-3">
            <div class="card-header">
                Organizaci&oacute;n
            </div>
            <div class="card-body">
                <div class="list-group-item d-flex flex-row justify-content-between align-content-center">
                    <div class="container">
                        <div class="row">
                            <div class="col-3">ID :</div>
                            <div class="col">{{ cobrador['uuid'] }} &#x2750;</div>                    
                        </div>
                        <div class="row">
                            <div class="col-3">Empresa / Servicio :</div>
                            <div class="col">{{ cobrador['nombre'] }}</div>                    
                        </div>
                        <div class="row">
                            <div class="col-3">E-mail :</div>
                            <div class="col">{{ cobrador['email'] }}</div>                    
                        </div>
                        <div class="row">                    
                            <div class="col strong">Fecha Saldo :</div>
                            <div class="col">{{ cobrador['fecha_saldo'][:10] }}</div>
                            <div class="col strong">Saldo :</div>
                            <div class="col">{{ cobrador['saldo'] }}</div>
                        </div>
                    </div>

                    <div class="d-flex flex-column">
                        <button class="btn btn-primary btn-sm" id="btn_editar_cobrador">Editar</button>
                    </div>

                </div>


            </div>
            
        </div>

        <div class="card mt-3">
            <div class="card-header d-flex flex-row justify-content-between">
                <div>Clientes</div>
                <a class="btn btn-primary btn-sm" href="/xpdcobros/usuarios/organizacion/{{cobrador['id']}}/cliente/crear">Agregar</a>
            </div>
            <div class="card-body">
                <div class="list-group">
    % if len(pagadores) == 0 :            
                    <div class="list-group-item">
                        No hay clientes registrados
                    </div>
    % end                        
    % for cliente in pagadores:
                    <div class="list-group-item d-flex flex-row justify-content-between align-content-center">
                        <div class="d-flex flex-column">
                            <span><b>&#x1F464; {{cliente['nombre']}}</b></span>
                            <span>&#x1F4E7; {{cliente['email']}}</span>
                            <span>Por cobrar: {{ - cliente['saldo'] if cliente['saldo'] < 0.00 else "0.00" }}</span>
                            <span>Saldo a favor: {{ cliente['saldo'] if cliente['saldo'] > 0.00 else "0.00" }}</span>
                        </div>
                        <div class="d-flex flex-column">
                            <a class="btn btn-primary btn-sm" href="/xpdcobros/usuarios/organizacion/{{cobrador['id']}}/cliente/{{cliente['id']}}">Ver Mas ...</a>
                        </div>
                    </div>
    % end
                </div>
            </div>
        </div>        

    </div>
    <div class="col-4 small">

        <div class="card mt-3">
            <div class="card-header d-flex flex-row justify-content-between">
                <div>Usuarios Gestores</div>
                <button class="btn btn-primary btn-sm" id="btn_agregar_usuario">Agregar</button>
            </div>
            <div class="card-body">
                <div class="list-group">
    % if len(usuariosCobrador) == 0 :            
                    <div class="list-group-item">
                        No hay usuarios registrados
                    </div>
    % end                        
    % for usuariox in usuariosCobrador:
                    <div id="usuario_{{usuariox['id']}}" class="list-group-item d-flex flex-row justify-content-between align-content-center">
                        <div class="d-flex flex-column {{"text-secondary" if usuariox['activo'] == 0 else ""}}">
                            <span><b>&#x1F464; {{usuariox['username']}}</b></span>
                            <span>&#x1F4E7; {{usuariox['email']}}</span>
                        </div>
                        <div class="d-flex flex-column">
    % if usuariox['activo'] == 1 and cobrador['id_usuario'] != usuariox['id_usuario'] :
                            <button class="btn btn-danger btn-sm btn_deshabilitar_usuario" data-id_usuario_cobrador="{{usuariox['id']}}">Deshabilitar</button>
    % elif usuariox['activo'] == 0 :
                            <button class="btn btn-primary btn-sm btn_habilitar_usuario"  data-id_usuario_cobrador="{{usuariox['id']}}">Habilitar</button>
    % end                        
                        </div>
                    </div>
    % end
                </div>
            </div>
        </div>

        <div class="card mt-3">
            <div class="card-header d-flex flex-row justify-content-between">
                <div>Cuentas Bancarias</div>
                <a class="btn btn-primary btn-sm" href="/xpdcobros/usuarios/organizacion/{{cobrador['id']}}/cuentasbco/crear">Agregar</a>
            </div>
            <div class="card-body">
                <div class="list-group">
    % if len(ctascbo) == 0 :            
                    <div class="list-group-item">
                        No hay cuentas registradas
                    </div>
    % end                        
    % for cuenta in ctascbo:
                    <div id="cuenta_{{cuenta['id']}}" class="list-group-item d-flex flex-row justify-content-between">
                        <div class="d-flex flex-column {{"text-secondary" if cuenta['activo'] == 0 else ""}}">
                            <span>&#x1F4B0; {{cuenta['nombre_banco']}} {{cuenta['tipo_cuenta']}} {{cuenta['numero_cuenta'][:3]}}*****{{cuenta['numero_cuenta'][-3:]}}</span>
                            <span>Saldo: {{cuenta['saldo']}}</span>
                        </div>
                        <div class="d-flex flex-column">
                            <a class="btn btn-secondary btn-sm" href="/xpdcobros/usuarios/organizacion/{{cobrador['id']}}/cuentasbco/{{cuenta['id']}}">Editar</a>
    % if cuenta['activo'] == 1 :
                            <button class="btn btn-danger btn-sm btn_deshabilitar_cuenta" data-id_cuenta="{{cuenta['id']}}">Deshabilitar</button>
    % elif cuenta['activo'] == 0 :
                            <button class="btn btn-primary btn-sm btn_habilitar_cuenta" data-id_cuenta="{{cuenta['id']}}">Habilitar</button>
    % end                        
                        </div>
                    </div>
    % end
                </div>
            </div>
        </div>


    </div>
    </div>



<form id="frm_cobrador" method="POST">
    <input type="hidden" name="accion" value="">
    <input type="hidden" name="email" value="">
    <input type="hidden" name="id_usuario_cobrador" value="">
    <input type="hidden" name="id_cuenta" value="">
</form>
<script src="/static/js/cobrador.js?2"></script>
% include('xpdcobros/pie.tpl', usuario = usuario)
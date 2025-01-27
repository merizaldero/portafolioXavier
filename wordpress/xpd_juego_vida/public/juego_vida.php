<div class="card">
  <div class="card-body">
    <div class="row">
      <div class="col-4">

        <div class="bg-light" data-bs-toggle="collapse" href="#xpdjv_divInyectarPatron">
          Insertar Patr&oacute;n
        </div>
        <div class="collapse show" id="xpdjv_divInyectarPatron">
            <div class="d-flex flex-row">
                <form onsubmit="return false;" class="pt-2 container">
                    <div class="row">Tama&ntilde;o Patr&oacute;n:</div>
                    <div class="row">
                      <div class="col">Ancho:</div>  
                      <input type="number" class="col form-control" id="xpdjv_txtColumnasPatron" value="5" maxlength="3" size="3" >
                    </div>
                    <div class="row">
                      <div class="col">Alto:</div>
                      <input type="number" class="col form-control" id="xpdjv_txtFilasPatron" value="5" maxlength="3" size="3" >
                    </div>
                </form>
                <div id="xpdjv_tableroPatron" class="xpdjv_tablero" >                
                </div>
            </div>
            <div class="mt-2 alert alert-info">
              Hacer click sobre la pantalla, y el patr&oacute;n ser&aacute; inyectado &gt; &gt; 
            </div>            
        </div>

        <div class="bg-light" data-bs-toggle="collapse" href="#xpdjv_divTamanoPanel">
            Resoluci&oacute;n
        </div>
        <div class="collapse show" id="xpdjv_divTamanoPanel">
            <div class="row">
              <div class="col">Ancho:</div>  
              <input type="number" class="col form-control" id="xpdjv_txtColumnas" value="50" maxlength="4">
            </div>
            <div class="row">
              <div class="col">Alto:</div>
              <input type="number" class="col form-control" id="xpdjv_txtFilas" value="50" maxlength="4">
            </div>
            <div class="row">
              <div class="col-10">Modo Armaged&oacute; (Vac&iacute;o)</div>
              <input type="checkbox" class="col" id="xpdjv_chkArmagedon">
            </div>
            <div class="py-2 input-group">
                <button class="btn btn-primary" id="xpdjv_btnArrancar">Aplicar</button>
            </div>    
        </div>

      </div>
      <div class="col-8">
        <div id="xpdjv_tablero" class="xpdjv_tablero" ></div>
      </div>
    </div>
  </div>
</div>

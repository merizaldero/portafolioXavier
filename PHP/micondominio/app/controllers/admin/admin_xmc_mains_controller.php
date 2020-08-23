<?php

class AdminXmcMainsController extends MvcAdminController {

    var $default_columns = array('id', 'name');
    public function index(){
        
    }

    public function ver_flujoestados(){
        $url = MvcRouter::admin_url(array('controller' => 'flujoestados', 'action' => 'index'));
        $this->redirect($url);
    }
    public function ver_tipoconstruccions(){
        $url = MvcRouter::admin_url(array('controller' => 'tipoconstruccions', 'action' => 'index'));
        $this->redirect($url);
    }
    public function ver_condominios(){
        $url = MvcRouter::admin_url(array('controller' => 'condominios', 'action' => 'index'));
        $this->redirect($url);
    }
    public function ver_habitantes(){
        $url = MvcRouter::admin_url(array('controller' => 'habitantes', 'action' => 'index'));
        $this->redirect($url);
    }

}

package ec.xpd.hulkstore.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.SessionAttributes;

import ec.xpd.hulkstore.domain.MovimientoProducto;
import ec.xpd.hulkstore.domain.Producto;
import ec.xpd.hulkstore.domain.Usuario;
import ec.xpd.hulkstore.service.MovimientoProductoService;
import ec.xpd.hulkstore.service.ProductoService;
import ec.xpd.hulkstore.service.UsuarioService;

/**
 * Controlador principal para aplicacion
 * @author Marcelo Xavier Merizalde
 *
 */
@Controller
@SessionAttributes("beanSesion")
public class HulkStoreController {

	private static final String FWD_LOGIN = "login";
	private static final String FWD_INVENTARIO = "productos";
	private static final String FWD_PRODUCTO = "producto";
	private static final String FWD_NUEVO_MOVIMIENTO = "nuevoMovimiento";
	
	private static final String ATTR_MENSAJE = "mensaje";
	

	@Autowired
	private UsuarioService usuarioService;
	
	@Autowired
	private ProductoService productoService;
	
	@Autowired
	private MovimientoProductoService movimientoProductoService;
	
	@ModelAttribute("beanSesion")
	public SessionBean beanSesion() {
	    return new SessionBean();
	}
	
	@GetMapping("/hulkstore")
    public String index(@ModelAttribute("beanSesion") SessionBean sessionBean, Model model) {
        if(sessionBean != null && sessionBean.getUsuario() != null){
        	return prepararForwardMain(model, sessionBean);
        } else {
        	return FWD_LOGIN;
        }
    }
	
	private String prepararForwardMain(Model model, SessionBean sessionBean) {
		List<Producto> productosMuestra = null;
		try {
			if(model.containsAttribute("nombreProducto")) {
				productosMuestra = productoService.findByNombreProducto((String)model.asMap().get("nombreProducto"));
			}else {
				productosMuestra = productoService.findAll();	
			}
			model.addAttribute("productos", productosMuestra);
		}catch(Exception ex) {
			model.addAttribute(ATTR_MENSAJE, "Error al obtener Productos");
		}
		return FWD_INVENTARIO;
	}
	
	@PostMapping("/buscarProducto")
    public String buscarProducto(@RequestParam(name = "nombreProducto") String nombreProducto,@ModelAttribute("beanSesion") SessionBean sessionBean, Model model) {
        if(sessionBean != null && sessionBean.getUsuario() != null){
        	if(nombreProducto !=null && !nombreProducto.isEmpty()) {
        		model.addAttribute("nombreProducto",nombreProducto.trim());
        	}
        	return prepararForwardMain(model, sessionBean);
        } else {
        	return FWD_LOGIN;
        }
    }

	@PostMapping("/login")
	public String login( @RequestParam(name="username", required=false) String username, @RequestParam(name="password", required=false) String password, @ModelAttribute("beanSesion") SessionBean sessionBean, Model model ) {
		
		Usuario usuario = null;
		try {
			usuario = usuarioService.login(username, password);
			if(usuario == null) {
				model.addAttribute(ATTR_MENSAJE, "Usuario / clave incorrectos");
				return FWD_LOGIN;
			}else {
				sessionBean.setUsuario(usuario);
				return prepararForwardMain( model , sessionBean);
			}
		}catch(Exception ex) {
			model.addAttribute(ATTR_MENSAJE, "Error al autenticar usuario");
			return FWD_LOGIN;
		}
		
	}
	
	@GetMapping("/logout")
	public String logout( @ModelAttribute("beanSesion") SessionBean sessionBean, Model model ) {
		
		sessionBean.setUsuario(null);
		return FWD_LOGIN;
		
	}

	@GetMapping("/producto")
	public String verItem( @RequestParam(name="idProducto", required=true) int idProducto, @ModelAttribute("beanSesion") SessionBean sessionBean, Model model ) {
		
		if(sessionBean != null && sessionBean.getUsuario() != null){
			Producto producto = productoService.getById(idProducto);
			return prepararForwardItem(producto, model, sessionBean);
        } else {
        	return FWD_LOGIN;
        }
	}

	private String prepararForwardItem(Producto producto, Model model, SessionBean sessionBean) {
		List<MovimientoProducto> movimientos = null;
		try {
			if(producto.getIdProducto() == null) {
				producto.setActivo(true);
				producto.setUsuarioCreacion(sessionBean.getUsuario().getIdUsuario());
			} else {
				producto.setUsuarioModificacion(sessionBean.getUsuario().getIdUsuario());
				movimientos = movimientoProductoService.findByProducto(producto.getIdProducto());
				model.addAttribute("movimientos", movimientos);	
			}
			sessionBean.setProducto(producto);
			
			return FWD_PRODUCTO;
		}catch(Exception ex) {
			model.addAttribute(ATTR_MENSAJE, "Error al recuperar Producto");
			return FWD_INVENTARIO;
		}
	}
	
	@GetMapping("/nuevoproducto")
	public String nuevoItem( @ModelAttribute("beanSesion") SessionBean sessionBean, Model model ) {
		if(sessionBean != null && sessionBean.getUsuario() != null){
			Producto producto = new Producto();
			producto.setNombreProducto("Nuevo Producto");
			producto.setActivo(true);
			return prepararForwardItem( producto, model, sessionBean);
        } else {
        	return FWD_LOGIN;
        }
	}

	@PostMapping("/guardaritem")
	public String guardarItem( 
			@RequestParam(name="idProducto")
			Integer idProducto,
			@RequestParam(name="nombreProducto")
			String nombreProducto,
			@RequestParam(name="cantidadDisponible")
			int cantidadDisponible,
			@RequestParam(name="activo",required = false,defaultValue = "0")
			String activo,
			@ModelAttribute("beanSesion") SessionBean sessionBean, Model model ) {
		if(sessionBean != null && sessionBean.getUsuario() != null){
			
			Producto producto = sessionBean.getProducto();
			producto.setIdProducto(idProducto);
			producto.setNombreProducto(nombreProducto);
			producto.setCantidadDisponible(cantidadDisponible);
			producto.setActivo("1".equals(activo));
			producto.setUsuarioCreacion(sessionBean.getUsuario().getIdUsuario());
			
			try {
				producto = productoService.guardarProducto(producto);
			}catch(Exception ex) {
				model.addAttribute(ATTR_MENSAJE, "No se pudo Guardar Producto. "+ex.getLocalizedMessage());
			}
			
			return prepararForwardItem( producto, model, sessionBean);
        } else {
        	return FWD_LOGIN;
        }
	}
	
	@GetMapping("/nuevomovimiento")
	public String nuevoMovimiento( @ModelAttribute("beanSesion") SessionBean sessionBean, Model model ) {
		if(sessionBean != null && sessionBean.getUsuario() != null){
			
			MovimientoProducto movimiento =  new MovimientoProducto();
			movimiento.setProducto(sessionBean.getProducto());
			movimiento.setCantidad(0);
			movimiento.setSaldo(sessionBean.getProducto().getCantidadDisponible());
			movimiento.setIdUsuario(sessionBean.getUsuario().getIdUsuario());
			
			sessionBean.setMovimientoProducto(movimiento);
			
			return FWD_NUEVO_MOVIMIENTO;
			
        } else {
        	return FWD_LOGIN;
        }
	}
	
	@PostMapping("/guardarmovimiento")
	public String guardarMovimiento( 
			@RequestParam(name="concepto")
			String concepto,
			@RequestParam(name="cantidad")
			int cantidad,
			@ModelAttribute("beanSesion") SessionBean sessionBean, Model model ) {
		if(sessionBean != null && sessionBean.getUsuario() != null){
			
			MovimientoProducto movimiento = sessionBean.getMovimientoProducto();
			movimiento.setConcepto(concepto);
			movimiento.setCantidad(cantidad);
			
			
			try {
				movimiento = movimientoProductoService.guardarMovimientoProducto(movimiento);
				return prepararForwardItem( movimiento.getProducto(), model, sessionBean);
			}catch(Exception ex) {
				model.addAttribute(ATTR_MENSAJE, "No se pudo Guardar Movimiento "+ex.getLocalizedMessage());
				return FWD_NUEVO_MOVIMIENTO;
				
			}
			
			
        } else {
        	return FWD_LOGIN;
        }
	}
	
}

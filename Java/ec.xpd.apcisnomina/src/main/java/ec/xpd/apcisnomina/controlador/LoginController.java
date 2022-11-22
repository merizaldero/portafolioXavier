package ec.xpd.apcisnomina.controlador;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class LoginController {
	@PostMapping("/login")
	public String login(@RequestParam("username") String username, HttpServletResponse response) {
		Cookie cookie = new Cookie("username", username);
		response.addCookie( cookie );
		System.out.println("cookie de sesion agregada");
		return "/static/index.html";
	}
}

import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.text.SimpleDateFormat;
import java.util.*;


public class Captura
{
    private static final SimpleDateFormat FFECHA = new SimpleDateFormat("ddMMMyyyy",new Locale("es","EC"));
    private static final SimpleDateFormat FHORA = new SimpleDateFormat("HHmm");
    
    public void robo(String directorio, String ux) throws Exception
    {
        Calendar now = Calendar.getInstance();
        String path = String.format("%s%s%s_%s_%s.jpg", directorio, File.separator, ux, FFECHA.format(now.getTime()) , FHORA.format(now.getTime()) );
        Robot robot = new Robot();
        BufferedImage screenShot = robot.createScreenCapture(new Rectangle(Toolkit.getDefaultToolkit().getScreenSize()));
        ImageIO.write(screenShot, "JPG", new File(path));
        System.out.println(path);
    }

    public static void main(String[] args) throws Exception
    {
        String ux = "815613";
        String directorio = "C:\\Users\\xavier\\Pictures\\capturas";
        for(int i= 0; i< args.length; i++) {
        	if(args[i].equals("-u")) {
        		ux = args[++i];
        	}
        	if(args[i].equals("-d")) {
        		directorio = args[++i];
        	}
        }
    	
        Captura s2i = new Captura();
        s2i.robo(directorio, ux);
    }
}
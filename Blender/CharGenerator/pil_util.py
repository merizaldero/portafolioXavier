import os.path
from os import makedirs
from PIL import Image
import argparse
import cv2
import numpy as np
#import imageio
#import pcx

LOG_PATH = os.path.join(os.path.dirname( os.path.abspath( __file__) ), "pil_util.log")
CHARACTER_HEIGHT = 105.0

def crop_images(input_dir, output_dir):
    escala = -1
    archivo = open( LOG_PATH, "at" )
    print(input_dir, file = archivo)
    print(output_dir, file = archivo)
    archivo.close()
    makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if not file.endswith('.png'):
            continue
        image = cv2.imread(os.path.join(input_dir, file))
        background_color = image[0,0]
        
        # RECORTA EN EJE Y
        arriba = None
        abajo = None
        for fila in range (0, image.shape[0]):
            if arriba is None:
                conteo = len([ x for x in image[ fila ] if len( [ x[i]  for i in range(0,image.shape[2]) if x[i] != background_color[i] ] ) != 0 ])
                if conteo != 0:
                    arriba = fila
            if abajo is None and fila > 0:
                conteo = len([ x for x in image[ -fila ] if len( [ x[i]  for i in range(0,image.shape[2]) if x[i] != background_color[i] ] ) != 0 ])
                if conteo != 0:
                    abajo = - fila
            if arriba is not None and abajo is not None:
                break
        
        izquierda = None
        derecha = None

        # Recorta en eje X 
        for columna in range (0, image.shape[1]):
            if izquierda is None:
                conteo = len([ x for x in image[ :, columna ] if len( [ x[i]  for i in range(0,image.shape[2]) if x[i] != background_color[i] ] ) != 0 ])
                if conteo != 0:
                    izquierda = columna
            if derecha is None and columna > 0:
                conteo = len([ x for x in image[ :, - columna ] if len( [ x[i]  for i in range(0,image.shape[2]) if x[i] != background_color[i] ] ) != 0 ])
                if conteo != 0:
                    derecha = - columna
            if izquierda is not None and derecha is not None:
                break
        print("{0} : {1}:{2} , {3}:{4} ".format(file, arriba, abajo, izquierda, derecha) )
        
        
        new_image = image[arriba:abajo, izquierda:derecha]
        
        # Escala imagen alto referencia 105 px
        if escala == -1:
            escala = CHARACTER_HEIGHT / new_image.shape[0]
        tamano = ( int(new_image.shape[1] * escala), int(new_image.shape[0] * escala) )
        resize_image = cv2.resize(new_image, tamano , interpolation=cv2.INTER_LINEAR )

        # agrega canal alfa y aplica transparencia a background-color
        image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2BGRA)
        background_color = image[0,0]
        #alpha_channel = cv2.split(image)[3]
        mask = cv2.bitwise_not(cv2.inRange(image, background_color, background_color))
        image = cv2.bitwise_and(image, image, mask=mask)

        cv2.imwrite(os.path.join(output_dir, file), image)

def convert_images(input_dir, output_dir):
    archivo = open( LOG_PATH, "at" )
    print(input_dir, file = archivo)
    print(output_dir, file = archivo)
    archivo.close()
    makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if not file.endswith('.png'):
            continue
        image = Image.open(os.path.join(input_dir, file))
        image.load()
        bg_color = image.getpixel( (0,0) )
        backgrd = Image.new("RGB", image.size, bg_color )
        # backgrd.paste(image, mask=image.split()[3])
        backgrd.paste(image)
        backgrd.save(os.path.join(output_dir, file.replace(".png", ".pcx")))

def main():
    parser = argparse.ArgumentParser(description='Operaciones PIL no disponibles en blender')
    parser.add_argument('operacion')
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')

    args = parser.parse_args()

    if args.operacion == "crop_images":
        crop_images( args.input_dir, args.output_dir)
    else:
        convert_images(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()

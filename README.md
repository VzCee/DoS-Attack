##  DoS Attack Using Protocol CDP
- Este Proyecto esta basado en una practica realizada con fines educativos, en el cual realizamos un ataque DoS utilizando Script basados en Scapy en el Lenguaje Python.


## Función Del Script
- Este script de Python utiliza la librería scapy para realizar un ataque de ARP Spoofing (o envenenamiento de caché ARP). El objetivo de este ataque es posicionarse como un "hombre en el medio" (Man-in-the-Middle, MitM) entre una víctima y el gateway (puerta de enlace) de la red. Al lograrlo, todo el tráfico entre la víctima e Internet pasará a través de la máquina del atacante, permitiendo su escucha, manipulación o filtrado.

## Video de Demostracion
- **https://youtu.be/FHRJCyYAE5I**

## Topologia en PNETLab
<img width="536" height="553" alt="image" src="https://github.com/user-attachments/assets/b888fd6e-2f8e-496f-a4b4-092bfa749b67" />

**En la topologia utilizamos las siguientes conexiones en la topologia;**
##Router conexion hacia el **Switch** e0/0 > e0/0
- **Router**

Conexion hacia el **Switch** e0/0 > e0/0

Conexion hacia el **Net** > e0/0


- **Atacante**
Conexión con **Net** > etho1

Conexión con **Switch** etho0 > e0/1


- **Victima**
Conexión con **Switch** etho0 > e0/2




## Parámetros usados en Atacante
`python3 cdp_dos.py --help`

**usage: cdp_dos.p**y `[-h] [-i INTERFACE] [-c COUNT] [-d DELAY]`

`Script de ataque DoS mediante inundación de paquetes CDP con Scapy.`

**options:
  -h, --help**            `show this help message and exit**`
  
 **-i INTERFACE**, `--interface INTERFACE`

  
                        Interfaz de red por la que se enviarán los paquetes (por defecto: eth0).
  **-c COUNT**, `--count COUNT`
                        `Número total de paquetes a enviar (por defecto: 10000).`
                        
                        
  **-d DELAY, `--delay DELAY`
                        Retraso en segundos entre cada paquete (por defecto: 0.001).**



## Requisitos para utilizar la herramienta
- Python 3.8+.
- Librería `scapy`.
- Acceso a internet.

## Medidas de mitigación
- Usar `firewalls`.
- Limitar `permisos de ejecución`.
- `Monitoreo` de logs.



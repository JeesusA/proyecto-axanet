# manage_clients.py
# Programa para gestionas los clientes de Axanet crear, leer, modificar y eliminar archivos de clientes.
# Usa diccionarios para mapear nombres a archivos y facilitar la busqueda.

# Importamos solo las herramientas especificas que vamos a usar
from os import remove, path  # remove para eliminar archivo, path para verificar existencia
from pathlib import Path     # Para manejar rutas de archivos de forma segura
from datetime import datetime # Para obtener la fecha y hora actuales
from sys import exit         # Para salir del programa si es necesario

# Definamos las constantes de las rutas de los archivos
CARPETA_CLIENTES = Path("proyecto_axanet/clientes") # Ruta donde guardaremos los archivos de clientes
ARCHIVO_INDICE = CARPETA_CLIENTES.parent / "index.txt"  # Archivo donde se guardan los nombres y IDs de los clientes
                                                        # Este archivo índice se guarda en el directorio padre de clientes, 
                                                        # es decir, en proyecto_axanet

# Sinmulacion de usuarios del equipo.
USUARIOS_EQUIPO = ["Ana Garcia", "Carlos Lopez"]

# Diccionario global para mapear nombres normalizados a rutas de archivos
archivos_clientes = {} # Este diccionario estará vacío al inicio

def normalizar_nombre(nombre):
    # Convertimos el nombre a minusculas y reemplazamos espacio por guiones bajos
    nombre_normalizado = nombre.lower().replace(" ", "_")
    return nombre_normalizado # Devolvemos el nombre normalizado

# Función para cargar los archivos de clientes existentes en el diccionario
def cargar_archivos_clientes():
    # Creamos el directorio padre y luego el de clientes si no existen
    CARPETA_CLIENTES.parent.mkdir(exist_ok=True)  # Crea proyecto_axanet
    CARPETA_CLIENTES.mkdir(exist_ok=True)         # Crea clientes
    # Revisamos si el archivo índice existe
    if path.exists(ARCHIVO_INDICE):
        # Abrimos el archivo índice en modo lectura
        with open(ARCHIVO_INDICE, 'r') as archivo:
            # Leemos cada línea del archivo
            for linea in archivo:
                # Separamos la línea en client_id y nombre (formato: "client_id:nombre")
                client_id, nombre = linea.strip().split(':')
                # Normalizamos el nombre para usarlo como clave en el diccionario
                nombre_normalizado = normalizar_nombre(nombre)
                # Creamos la ruta del archivo del cliente (ejemplo: clientes/juan_perez.txt)
                archivo_cliente = CARPETA_CLIENTES / f"{nombre_normalizado}.txt"
                # Agregamos al diccionario: nombre normalizado -> ruta del archivo
                archivos_clientes[nombre_normalizado] = archivo_cliente

# Funcion para generar un ID unico para un cliente
def generar_id_cliente(nombre):
    # Sacamos las iniciales del nombre (primeras letras de cada palabra)
    iniciales = ''.join(palabra[0] for palabra in nombre.split()[:2]).upper()
    # Obtenemos la fecha y hora actual en formato YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Combinamos iniciales y timestamp para el ID (ejemplo: JP_20250528070600)
    return f"{iniciales}_{timestamp}"

# Funcion para notificar a los usuarios del equipo
def notificar_equipo(mensaje):
    # Simulamos notificar a cada usuario del equipo
    for usuario in USUARIOS_EQUIPO:
        print(f"Notificando a {usuario}: {mensaje}")

# Funcion para crear un nuevo cliente
def crear_cliente():
    # Mostramos un mensaje para indicar que estamos creando a un cliente
    print("=== Crear Nuevo Cliente ===")
    # Solicitamos los datos del cliente
    nombre = input("Ingrese el nombre del cliente: ").strip()
    nombre_normalizado = normalizar_nombre(nombre)

    # Verificamos si el cliente ya existe en el diccionario
    if nombre_normalizado in archivos_clientes:
        print("Error: Ya existe un cliente con ese nombre.")
        return
    
    telefono = input("Ingresa el teléfono: ").strip()
    correo = input("Ingresa el correo electrónico: ").strip()
    primer_servicio = input("Ingresa la descripción del primer servicio: ").strip()

    # Generamos un ID único para el cliente
    client_id = generar_id_cliente(nombre)
    # Creamos la ruta del archivo del cliente
    archivo_cliente = CARPETA_CLIENTES / f"{nombre_normalizado}.txt"

    # Intentamos escribir el archivo del cliente
    try:
        with open(archivo_cliente, "w") as archivo:
            # Escribimos los datos del cliente en el archivo
            archivo.write(f"Nombre: {nombre}\n")
            archivo.write(f"ID_Cliente: {client_id}\n")
            archivo.write(f"Teléfono: {telefono}\n")
            archivo.write(f"Correo: {correo}\n")
            archivo.write(f"Fecha Registro: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            archivo.write(f"Servicios: \n")
            archivo.write(f"- {primer_servicio} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")

        # Agregamos el cliente al archivo indice
        with open(ARCHIVO_INDICE, 'a') as archivo:
            archivo.write(f"{client_id}:{nombre}\n")

        # Actualizamos el diccionario
        archivos_clientes[nombre_normalizado] = archivo_cliente
        print(f"Cliente creado con exito. ID: {client_id}")
        # Notificamos al equipo
        notificar_equipo(f"Se ha creado un nuevo cliente: {nombre}")
    except IOError as e:
        # Manejamos errores si no se puede crear el archivo
        print(f"Error al crear el archivo del cliente: {e}")

# Funcion para leer y parsear la informacion de un cliente
def leer_info_cliente(nombre_normalizado):
    # Creamos un diccionario para guardar la informacion del cliente
    info_cliente = {}
    # Verificamos si el cliente existe y su archivo esta disponible
    if nombre_normalizado in archivos_clientes and path.exists(archivos_clientes[nombre_normalizado]):
        # Abrimos el archivo edl cliente en modo lectura
        with open(archivos_clientes[nombre_normalizado], "r") as archivo:
            # Leemos cada linea del archivo
            for linea in archivo:
                # Si la linea tiene un formato "clave: valor", la parseamos
                if ':' in linea:
                    clave, valor = linea.split(':', 1)  # Dividimos solo en la primera ocurrencia
                    info_cliente[clave.strip()] = valor.strip()  # Guardamos en el diccionario
                # Si la linea es un servicio (empieza con "-"), la agregamos a la lista de servicios
                elif linea.startswith('-'):
                    if 'Servicios' not in info_cliente:
                        info_cliente['Servicios'] = []
                    info_cliente['Servicios'].append(linea.strip())
    return info_cliente

# Funcion para visualizar informacion de un cliente
def visualizar_cliente():
    # Mostramos un mensaje para indicar que vamos a visualizar informacion
    print("=== Visualizar Informacion de Cliente ===")
    # Preguntamos si el usuario quiere buscar un cliente o listar todos
    accion = input("Ingresa 'b' para buscar a un cliente o 'l' para listar a todos los clientes:").strip().lower()

    if accion == 'b':
        # Si elige buscar, pedimos el nombre del cliente
        nombre = input("Ingrese el nombre del cliente a buscar: ").strip()
        nombre_normalizado = normalizar_nombre(nombre)
        # Leemos la informacion del cliente
        info_cliente = leer_info_cliente(nombre_normalizado)
        # Si encontramos informacion, la mostramos
        if info_cliente:
            print("\nDetalles del Cliente:")
            for clave, valor in info_cliente.items():
                print(f"{clave}: {valor}")
            # Notificamos al equipo
            notificar_equipo(f"Se ha consultado la informacion del cliente: {nombre}")
        else:
            print("No se encontró información para ese cliente.")
    elif accion == 'l':
        # Si elige listar, mostramos todos los clientes
        if archivos_clientes:
            print("\nClientes registrados:")
            for nombre in archivos_clientes.keys():
                info_cliente = leer_info_cliente(nombre)
                print(f"Nombre: {info_cliente.get('Nombre', 'Desconocido')}")
        else:
            print("No hay clientes registrados.")
    else:
        print("Acción no reconocida. Por favor, ingresa 'b' para buscar o 'l' para listar.")

# Funcion para agregar un servicio a un cliente existente
def agregar_servicio():
    # Mostramos un mensaje para indicar que vamos a agregar un servicio
    print("=== Agregar Servicio a Cliente Existente ===")
    # Solicitamos el nombre del cliente
    nombre = input("Ingrese el nombre del cliente: ").strip()
    nombre_normalizado = normalizar_nombre(nombre)

    # Verificamos el cliente existe
    if nombre_normalizado not in archivos_clientes:
        print("Error: No existe un cliente con ese nombre.")
        return
    
    # Solicitamos la descripcion del nuevo servicio
    servicio_desc = input("Ingrese la descripción del nuevo servicio: ").strip()
    # Leemos la informacion actual del cliente
    info_cliente = leer_info_cliente(nombre_normalizado)

    # Intentamos agregar el servicioa al archivo del cliente
    try:
        with open(archivos_clientes[nombre_normalizado], "a") as archivo:
            # Agregamos el nuevo servicio al final del archivo
            archivo.write(f"- {servicio_desc} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        print("Servicio agregado con éxito.")
        # Notificamos al equipo
        notificar_equipo(f"Se ha actualizado al cliente: {nombre} con un nuevo servicio: {servicio_desc}")
    except IOError as e:
        # Manejamos errores si no se puede agregar el servicio
        print(f"Error al agregar el servicio: {e}")

# Funcion para eliminar a un cliente
def eliminar_cliente():
    # Mostramos un mensaje para indicar que vamos a eliminar un cliente
    print("=== Eliminar Cliente ===")
    # Solicitamos el nombre del cliente a eliminar
    nombre = input("Ingrese el nombre del cliente a eliminar: ").strip()
    nombre_normalizado = normalizar_nombre(nombre)

    # Verificamos si el cliente existe
    if nombre_normalizado not in archivos_clientes:
        print("Error: No existe un cliente con ese nombre.")
        return
    
    # Pedimos confirmacion para eliminar
    confirmar = input(f"¿Estás seguro de que quieres eliminar al cliente '{nombre}'? (s/n): ").strip().lower()
    if confirmar == 's':
        try:
            # Eliminammos el archivo del cliente
            remove(archivos_clientes[nombre_normalizado])
            # Eliminamos la entrada del diccionario
            del archivos_clientes[nombre_normalizado]
            # Actualizamos el archivo indice
            with open(ARCHIVO_INDICE, 'r') as archivo:
                lineas = [linea for linea in archivo if normalizar_nombre(linea.split(':')[1].strip()) != nombre_normalizado]
            with open(ARCHIVO_INDICE, 'w') as archivo:
                archivo.writelines(lineas)
            print(f"Cliente '{nombre}' eliminado con éxito.")
            # Notificamos al equipo
            notificar_equipo(f"Se ha eliminado al cliente: {nombre}")
        except IOError as e:
            # Manejamos errores si no se puede eliminar el archivo
            print(f"Error al eliminar el cliente: {e}")
    else:
        print("Eliminación cancelada.")

# Funcion para mostrar el menu principal
def menu_principal():
    # Cargamos los clientes al iniciar el programa
    cargar_archivos_clientes()
    # Bucle infinito para mostrar el menu hasta que el usuario decida salir
    while True:
        print("\n=== Sistema de Gestion de Clientes Axanet ===")
        print("1. Crear Nuevo Cliente")
        print("2. Visualizar Informacion de Cliente")
        print("3. Agregar Servicio a Cliente")
        print("4. Eliminar Cliente")
        print("5. Salir")
        opcion = input("Seleccione una opcion (1-5): ").strip()
        if opcion == '1':
            crear_cliente()
        elif opcion == '2':
            visualizar_cliente()
        elif opcion == '3':
            agregar_servicio()
        elif opcion == '4':
            eliminar_cliente()
        elif opcion == '5':
            print("Saliendo del sistema. ¡Hasta luego!")
            exit(0)
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 5.")

# Ejecutamos el menu principal al iniciar el programa
if __name__ == "__main__":
    # Llamamos al menu principal para iniciar el programa
    menu_principal()

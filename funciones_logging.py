import re 
import sqlite3
import bcrypt
import csv
from datetime import datetime
from colorama import init,Fore
#------------------------------FUNCION DE LA CONEXION---------------------------------------------
def conexion():
    """
    Establece una conexión con la base de datos 'inventario.db'.

    Returns:
        Una tupla (conexion, cursor) si la conexión es exitosa.
        En caso de error, retorna (None, None).
    """

    try:
        con = sqlite3.connect("inventario.db")
        cur = con.cursor()
        return con, cur
    except sqlite3.Error as error:
        print(f"Error al conectar con la base de datos: {error}")
        return None, None
     
     
     
     
def validar_menu(opcion):
    """
    Valida que la opción ingresada sea 1 o 2.

    Args:
        opcion (str): Opción ingresada por el usuario.

    Returns:
        int: La opción convertida a entero si es válida (1 o 2).
             En caso contrario, imprime un mensaje y no retorna nada.
    """
    opciones= [1,2]
    if opcion.isdigit():
        opcion=int(opcion)
        if  opcion in opciones:
            return opcion
        else:
            print(Fore.YELLOW + "Las opciones son 1 o 2 ")
    else:
        print(Fore.RED + "Ingrese un numero.")
        
        
        
 #---------------------------------------------------FUNCIONES PARA CREAR----------------------------------------------------------------------       
def validar_contraseña(password):
    """
    Verifica que la contraseña cumpla con los requisitos de seguridad.

    Requisitos:
        - Mínimo 8 caracteres
        - Al menos una letra mayúscula
        - Al menos una letra minúscula
        - Al menos un número
        - Al menos un símbolo especial

    Args:
        password (str): La contraseña a validar.

    Returns:
        list: Lista de errores si la contraseña no cumple los requisitos.
        str: Contraseña hasheada si es válida.
    """
    errores = []
    if len(password) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres.")
    
    if not re.search(r'[A-Z]', password):
        errores.append("Debe contener al menos una letra mayúscula.")
    
    if not re.search(r'[a-z]', password):
        errores.append("Debe contener al menos una letra minúscula.")
    
    if not re.search(r'[0-9]', password):
        errores.append("Debe contener al menos un número.")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errores.append("Debe contener al menos un símbolo especial.")
    if errores:
        return errores
    else:
         hash_contraseña = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
         return hash_contraseña.decode('utf-8')
            




def validar_direccion(direccion):
    """
    Valida que la dirección ingresada cumpla con los criterios establecidos.

    Criterios:
        - Entre 10 y 100 caracteres
        - Caracteres válidos (letras, números, espacios y algunos símbolos)
        - Debe contener al menos un número

    Args:
        direccion (str): Dirección ingresada.

    Returns:
        list: Lista de errores si la dirección no es válida.
        str: Dirección válida si no hay errores.
    """
    
    errores = []
    if len(direccion) < 10:
        errores.append("La dirección es demasiado corta.")
    if len(direccion) > 100:
        errores.append("La dirección es demasiado larga.")
    if re.search(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,\-#]", direccion):
        errores.append("La dirección contiene caracteres no permitidos.")
    if not re.search(r'\d+', direccion):
        errores.append("La dirección debe incluir un número.")

    if errores:
        return errores
    else:
        return direccion
        
        
def pedir_email(cur):
    """
    Solicita al usuario que ingrese un email válido y verifica que no esté registrado.

    Args:
        cur (sqlite3.Cursor): Cursor para consultar la base de datos.

    Returns:
        str: Email válido y no registrado.
        None: Si el usuario decide salir.
    """
    continuar_email= True
    while continuar_email:
        usuario = input("Escriba su email (o 'salir' para volver al menú anterior): ")
        if usuario.lower() == "salir":
            return None
        elif re.search(r'[^a-zA-Z0-9@._\-]', usuario):
            print("El email contiene símbolos no permitidos.")
        else:
            continuar_email= False

        cur.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        if cur.fetchone():
            print("Ese usuario ya está registrado.")
        else:
            return usuario
        
        

def pedir_nombre():
    """
    Solicita al usuario que ingrese un nombre válido.

    Criterios:
        - No vacío
        - Solo letras y espacios permitidos

    Returns:
        str: Nombre validado y limpio.
        None: Si el usuario decide salir.
    """
    
    continuar_nombre= True
    while continuar_nombre:
        nombre = input("Ingrese su nombre: ")
        if not nombre.strip():
            print("El campo no puede estar vacío.")
        elif re.search(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', nombre):
            print("El nombre contiene símbolos no permitidos.")
        elif nombre. lower() == "salir":
            return None
        else:
            continuar_nombre= False
            return nombre.strip()




def pedir_contraseña():
    """
    Solicita al usuario que ingrese una contraseña y la valida.

    Muestra los requisitos y repite hasta que la contraseña sea válida.

    Returns:
        str: Contraseña hasheada válida.
    """
    continuar_contraseña= True
    print(Fore.BLUE + "La contraseña debe tener:")
    print(Fore.BLUE + "- Al menos una mayúscula, una minúscula, un número y un carácter especial")
    
    while continuar_contraseña:
        contraseña = input("Ingrese contraseña: ")
        contraseña_hash = validar_contraseña(contraseña)
        if type(contraseña_hash) == list:
            print(Fore.RED + "Errores:")
            for error in contraseña_hash:
                print(Fore.RED + f"- {error}")
        else:
            continuar_contraseña= False
            return contraseña_hash

def pedir_direccion():
    """
    Solicita al usuario que ingrese una dirección válida, validándola mediante la función `validar_direccion`.

    El ciclo se repite hasta que el usuario proporciona una dirección sin errores de validación.
    Si se detectan errores, se muestran en rojo utilizando la librería `colorama`.

    Returns:
        str: Una dirección válida proporcionada por el usuario.
        """
    continuar_direccion= True
    while continuar_direccion:
        direccion = input("Ingrese su ubicación: ")
        errores = validar_direccion(direccion)
        if isinstance(errores, list) and errores:
            print(Fore.RED + "Errores:")
            for error in errores:
                print(Fore.RED + "-", error)
        else:
            continuar_direccion= False
            return direccion

def pedir_edad():
    """
    Solicita al usuario que ingrese su edad y valida que sea un número entero mayor o igual a 18.

    La función sigue solicitando la edad hasta que el usuario proporciona un valor numérico válido
    y mayor o igual a 18 años. Si el valor ingresado no es un número o es menor a 18, se muestra
    un mensaje de error.

    Returns:
        int: Edad válida ingresada por el usuario (mayor o igual a 18).
    """
    continuar_edad= True
    while continuar_edad:
        edad_input = input("Ingrese su edad: ")
        try:
            edad = int(edad_input)
            if edad < 18:
                print("Necesitas tener al menos 18 años.")
            else:
                continuar_edad= False
                return edad
        except ValueError:
            print("Ingrese un número válido.")

def inputs_crear():
    
    
    
    """
    Solicita y valida todos los datos necesarios para crear un nuevo usuario.

    Esta función interactúa con el usuario a través de la consola para recopilar
    la información requerida para un registro, incluyendo email, nombre, contraseña,
    dirección, edad, y fecha de registro. También establece el rol por defecto como "usuario".

    Returns:
        tupla o None: Una tupla con los siguientes valores si se completan correctamente:
            (usuario, nombre, contraseña, direccion, edad, fecha_registro, rol),
             `None` si ocurre un error de conexión o si el email ya está registrado.
    """
    con, cur = conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None

    usuario = pedir_email(cur)
    if usuario is None:
        return None

    nombre = pedir_nombre()
    contraseña = pedir_contraseña()
    direccion = pedir_direccion()
    edad = pedir_edad()
    fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    rol = "usuario"

    return usuario, nombre, contraseña, direccion, edad, fecha_registro, rol




def crear_usuario(usuario, nombre, password, direccion, edad, fecha_registro, rol):
    con, cur = conexion()
    
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return

    try:
        cur.execute("""
            INSERT INTO usuarios (usuario, nombre, contraseña, direccion, edad, fecha_registro, rol)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (usuario, nombre, password, direccion, edad, fecha_registro, rol)
        )
        con.commit()
        print(Fore.GREEN + "Usuario agregado con éxito.")
    except sqlite3.Error as error:
        print(Fore.RED + f"Error en la base de datos: {error}")
    finally:
        con.close()
        
#-----------------------------------------------------------FUNCIONES PARA VALIDAR------------------------------------------------------
def registrar_log(usuario, mensaje, archivo="registro_log.csv"):
    """
    Registra un mensaje en un archivo CSV junto con la fecha, hora y el nombre del usuario.

    Se utiliza para llevar un historial de acciones o errores relacionados con usuarios.

    Args:
        usuario (str): Nombre o identificador del usuario que genera el mensaje.
        mensaje (str): Descripción del evento o acción a registrar.
        archivo (str, optional): Nombre del archivo CSV donde se guarda el registro. 
            Por defecto es "registro_log.csv".
"""
    with open(archivo, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), usuario, mensaje])





def solicitar_email():
    """
    Solicita al usuario que ingrese un correo electrónico y lo valida.

    Verifica que el email no esté vacío, no contenga caracteres inválidos, 
    y cumpla con un formato básico. El usuario puede escribir 'salir' para cancelar.

    Returns:
        str o None: El correo electrónico ingresado si es válido, o None si el usuario decide salir.
        """
    continuar_email= True
    while continuar_email:
        usuario = input("Correo electrónico (o escriba 'salir' para volver al menú): ").strip()
        if usuario.lower() == "salir":
            return None
        elif not usuario:
            print("El campo no puede estar vacío.")
        elif re.search(r"[^a-zA-Z0-9@._\-]", usuario):
            print("El correo contiene caracteres inválidos.")
        elif not re.search(r"@.*\.", usuario):
            print("Formato de correo inválido.")
        else:
            continuar_email= False
            return usuario

def solicitar_contraseña():
    """
    Solicita al usuario que ingrese una contraseña.

    Verifica que no esté vacía. El usuario puede escribir 'salir' para cancelar.

    Returns:
        str or None: La contraseña si es válida, o None si el usuario decide salir.
        """
    continuar_contraseña= True
    while continuar_contraseña:
        contraseña = input("Contraseña (escriba 'salir' para volver al menú): ").strip()
        if contraseña.lower() == "salir":
            return None
        elif not contraseña:
            print("El campo no puede estar vacío.")
        else:
            continuar_contraseña= False
            return contraseña






def verificar_credenciales(cur, usuario, contraseña):
    """
    Solicita al usuario que ingrese un correo electrónico y lo valida.

    Verifica que el email no esté vacío, no contenga caracteres inválidos, 
    y cumpla con un formato básico. El usuario puede escribir 'salir' para cancelar.

    Returns:
        str or None: El correo electrónico ingresado si es válido, o None si el usuario decide salir.
        """
    
    
    query = "SELECT nombre, contraseña, rol FROM usuarios WHERE usuario = ?"
    cur.execute(query, (usuario,))
    resultado = cur.fetchone()

    if not resultado:
        return False, None, None 

    nombre, hash_contraseña, rol = resultado
    if bcrypt.checkpw(contraseña.encode("utf-8"), hash_contraseña.encode("utf-8")):
        return True, nombre, rol
    else:
        return False, nombre, rol







def validar_credenciales():
    """
    Maneja el proceso de inicio de sesión para validar credenciales de un usuario.

    Solicita correo y contraseña, los valida contra la base de datos, y permite
    un máximo de 3 intentos. Registra eventos de fallos y salidas voluntarias.

    Returns:
        str or None: El rol del usuario si el inicio de sesión es exitoso, o None si falla o se cancela.
"""
    intentos = 0
    max_intentos = 3
    con, cur = conexion()

    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None

    try:
        while intentos < max_intentos:
            usuario = solicitar_email()
            if usuario is None:
                print("Saliendo...")
                return None
            contraseña = solicitar_contraseña()
            if contraseña is None:
                print("Saliendo...")
                return None
            valido, nombre, rol = verificar_credenciales(cur, usuario, contraseña)
            if valido:
                print(Fore.GREEN + f"Contraseña correcta. ¡Bienvenido, {nombre}! Rol: {rol}")
                return rol
            else:
                if nombre:
                    intentos += 1
                    mensaje = "Contraseña incorrecta"
                else:
                    intentos += 1
                    mensaje = "Usuario no encontrado"

            registrar_log(usuario, mensaje)
            print(Fore.YELLOW + f"{mensaje}. Intento {intentos}/{max_intentos}")
        print(Fore.RED + "Se quedo sin intentos.")
    finally:
        con.close()    

    

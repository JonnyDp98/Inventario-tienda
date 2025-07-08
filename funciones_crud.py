import sqlite3
import re
from colorama import init, Fore
from datetime import * 
from tabulate import tabulate
from funciones_logging import conexion
init(autoreset=True)


#------------------------------------------------VALIDAR OPCION------------------------------------------
def crud_admin(opcion):
    """Valida que la opcion sea 1,2,3,4,5 o 6.
    Args:
        opcion (str): Opción ingresada por el usuario.

    Retorna:
        int: Opción válida convertida en entero si está en la lista de opciones.
        """
    opciones= [1,2,3,4,5,6]
    if opcion.isdigit():
        opcion = int(opcion)
        if opcion in opciones:
            return opcion
        else:
            print("la opcion debe ser 1,2,3,4,5,6")
    else:
        print("La opcion debe ser numerica.")

#---------------------------------------------------------------AGREGAR PRODUCTO-----------------------------------------


def pedir_nombre():
    """Pide nombre al usuario del producto.
    Retorna:
        str o None: Nombre válido del producto o None si se ingresa 'salir'.
    """
    continuar_nombre= True
    while continuar_nombre:
        nombre = input("Ingrese nombre del nuevo producto o modificar producto: ").strip()
        if not nombre:
            print(Fore.RED + "El campo no puede estar vacío.")
        elif nombre.lower() == "salir":
            return None
        elif re.search(r"[^a-zA-Z0-9.\-\s]", nombre):
            print(Fore.RED + "El nombre contiene símbolos no permitidos.")
        else:
            continuar_nombre=False
            return nombre


        
def pedir_descripcion():
    """Pide descripcion del producto.
    Retorna:
        str: Descripción válida del producto.
    """
    continuar_descripcion= True
    while continuar_descripcion:
        descripcion= input("Ingrese descripcion del producto o descripcion a modificar:").strip()
        if not descripcion:
            print(Fore.RED + "El campo no puede estar vacio")
        elif re.search(r"[^a-zA-Z0-9.\-\s]", descripcion):
            print(Fore.RED + "La descripcion contiene simbolos no permitidos.")
        else:
            continuar_descripcion=False
            return descripcion
        
            
  
def pedir_cantidad():
    """Pide una cantidad del producto  en str y si es un numero lo convierte a entero.
    Retorna:
        int: Cantidad válida del producto.
    """
    continuar_cantidad= True
    while continuar_cantidad:
        cantidad= input("Ingrese la cantidad del producto o cantidad a modificar:").strip()
        try:
            cantidad=int(cantidad)
        except ValueError:
            print("El ingreso debe ser numerico")
        else:
            continuar_cantidad=False
            return cantidad



def pedir_precio():
    """Pide un precio del producto  en str y si es un numero lo convierte a entero.
    Retorna:
        float: Precio válido del producto.
    """
    continuar_precio= True
    while continuar_precio:
        precio= input("Ingrese precio del producto o precio a modificar:")
        try:
            precio= float(precio)
        except ValueError:
            print("El ingreso debe ser numerico")
        else:
            continuar_precio= False
            return precio
        
        
        
def pedir_categoria():
    """Pide una categoria del producto.
    Retorna:
        str o None: Categoría válida del producto o None si se ingresa "salir".
    """
    continuar_categoria=True
    while continuar_categoria:
        categoria= input("Categoria del producto o categoria a modificar:")
        if not categoria:
            print(Fore.RED + "El campo no puede estar vacio.")
        elif categoria.lower() == "salir":
            return None
        elif re.search(r'[^a-zA-Z0-9.]', categoria):
            print(Fore.RED + "El nombre contiene símbolos no permitidos.")
        else:
            continuar_categoria=False
            return categoria


        
def pedir_inputs_agregar():
    con, cur = conexion()
    """Esta funcion se encarga de pedir todos los datos del producto y luego insertarlos en la base de datos"""
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None
    else:
        nombre= pedir_nombre()
        descripcion= pedir_descripcion()
        cantidad= pedir_cantidad()
        precio= pedir_precio()
        categoria= pedir_categoria()
        try:
            query="""INSERT INTO productos(nombre, descripcion, cantidad, precio, categoria)
                    VALUES (?, ?, ?, ?, ?)"""
            cur.execute(query,(nombre,descripcion,cantidad,precio,categoria))
            con.commit()
            print("Producto agregado con exito")
        except sqlite3.Error as error:
            print(f"Error al insertar en la base de datos {error}")
        finally:
            con.close()
            

    

#------------------------------------------------MOSTRAR INVENTARIO COMPLETO----------------------------------------------------------------------
def mostrar_inventario():
    """
  Muestra todos los productos registrados hasta el momento  
    """
    con,cur=conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None         
    else:
        try:
            query="""SELECT * FROM productos"""
            cur.execute(query)
        except sqlite3.Error as error:
            print(f"error al consultar la base de datos")       
        else:
            resultado_inventario= cur.fetchall()
            if resultado_inventario:
                print("Se encontraron estos productos")
                print(tabulate(resultado_inventario, headers=["ID", "Nombre", "Descripcion", "Cantidad","Precio","Categoria"], tablefmt="double_grid"))      
            else:
                print("no hay productos en el inventario")
        finally:
            con.close()
            
#---------------------------------------------------------------BUSCAR MEDIANTE ID-------------------------------------------------------------------------------------
def buscar_id():
    """Valida que el ID ingresado sea un numero, si los es lo convierte a entero.
   Retorna:
        int: si lo que ingreso el usuario es un numero lo convierte a entero y lo devuelve como entero.
    
    
    """
    continuar_id= True
    while continuar_id:
        id= input("Escriba la id a buscar: ")
        try:
            id= int(id)
            if id <= 0:
                print(Fore.YELLOW + "La ID no puede ser 0")
            else:
                continuar_id=False
                return id
        except ValueError:
            print("La ID debe ser numerica.")
            
def buscar_por_id():
    """
    Busca en la base de datos un producto con la ID ingresada por el usuario.
    Retorna:
    Una tupla o None: si encuentra esa ID    
    """
    con, cur= conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None         
    else:
        id=buscar_id()
        try:
            query="""SELECT * FROM productos WHERE id= ?"""
            cur.execute(query,(id,))
            resultado_id= cur.fetchone()
             
            if resultado_id:
                print(tabulate([resultado_id], headers=["ID", "Nombre", "Descripcion", "Cantidad","Precio","Categoria"], tablefmt="double_grid"))  
                return resultado_id
            else:
                print(Fore.RED + "Producto no encontrado")
        except sqlite3.Error as error:
            print(Fore.RED + f"ERROR EN LA BASE DE DATOS,{error}")
            return None
        finally:
            con.close()
            
    
#---------------------------------------------------------------------ACTUALIZAR ID------------------------------------------------------------------------------------
#aca voy a reutilizar funciones de agregar producto y visualizacion ya utilizadas para resumir mas el codigo
def opciones_modificar(opcion):
    """
    Valida si la opción ingresada es un número entero entre 1 y 6.

    Args:
        opcion (str): Valor ingresado por el usuario.

    Retorna:
        int: La opción validada si es válida.
        None: Si la opción no es válida o ocurre un error.
        """
    opciones= [1, 2, 3, 4, 5, 6]
    try:
        opcion= int(opcion)
        if not opcion in opciones:
            print(Fore.YELLOW + "La opcion debe ser 1,2,3, 4, 5 o 6")
        else:
            return opcion
    except ValueError:
        print(Fore.RED + "La opcion debe ser un numero")
        
        
        
def modificar_datos(id,campo,nuevo_valor):
    """
    Actualiza un campo específico de un producto en la base de datos.

    Parámetros:
        id (int): ID del producto a actualizar.
        campo (str): Nombre del campo a modificar (ej. 'nombre', 'precio').
        nuevo_valor (any): Nuevo valor a asignar al campo.
    """
    con, cur= conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None         
    else:
        try:
            query = f"UPDATE productos SET {campo} = ? WHERE id = ?"
            cur.execute(query, ( nuevo_valor, id))
            con.commit()
            print("actualizado correctamente")
        except sqlite3.Error as error:
            print(f"Error al actualizar {campo}: {error}")
        finally:
            con.close()
            
    
    



def actualizar_por_id():#En esta funcion quiero remarcar algo, decidi controlar de esta forma lo que se desea modificar para evitar posibles inyecciones.
    """
    Interfaz interactiva para actualizar campos de un producto existente por su ID.

    Solicita al usuario qué campo desea modificar y aplica los cambios en la base de datos.
    """
    continuar_actualizar= True
    id_producto = buscar_por_id()
    if id is None:
        return
    else:
        id_encontrada=id_producto[0]
        while continuar_actualizar:
            print("Que desea modificar?")
            print("1. Nombre.")
            print("2. Descripcion")
            print("3. Cantidad")
            print("4. Precio")
            print("5. Categoria")
            print("6.  Salir")
            opcion= input("Elige la opcion a modificar:" )
            validar_actualizacion=opciones_modificar(opcion)
            if validar_actualizacion == 1:
                print(Fore.GREEN + "ACTUALIZACION NOMBRE")
                nuevo_nombre= pedir_nombre()
                modificar_datos(id_encontrada, "nombre",nuevo_nombre)
            elif validar_actualizacion == 2:
                print(Fore.GREEN + "ACTUALIZACION DESCRIPCION")
                nueva_descripcion= pedir_descripcion()
                modificar_datos(id_encontrada, "descripcion",nueva_descripcion)
            elif validar_actualizacion == 3:
                print(Fore.GREEN + "ACTUALIZACION CANTIDAD")
                nueva_cantidad= pedir_cantidad()
                modificar_datos(id_encontrada, "cantidad", nueva_cantidad)
            elif validar_actualizacion == 4:
                print(Fore.GREEN + "ACTUALIZACION PRECIO")
                nuevo_precio= pedir_precio()
                modificar_datos(id_encontrada, "precio", nuevo_precio)
            elif validar_actualizacion == 5:
                print("ACTUALIZACION CATEGORIA")
                nueva_categoria= pedir_categoria()
                modificar_datos(id_encontrada, "categoria", nueva_categoria)
            elif validar_actualizacion == 6:
                print("SALIENDO...")
                continuar_actualizar= False    
                
                
                
#------------------------------------------------------------------------------------ELIMINAR PRODUCTO-----------------------------------------------------------------------
def opcion_eliminar(opcion):
    """
    Valida si la opción ingresada es 1 (Sí) o 2 (No) para confirmar la eliminación.

    Args:
        opcion (str): Valor ingresado por el usuario.

    Retorna:
        int: La opción validada si es válida.
        None: Si la opción no es válida o ocurre un error.
    """
    opciones= [1, 2, 3]
    try:
        opcion= int(opcion)
        if not opcion in opciones:
            print(Fore.YELLOW + "La opcion debe ser 1,2 o 3")
        else:
            return opcion
    except ValueError:
        print(Fore.RED + "La opcion debe ser un numero")




def eliminar_producto():
    """
    Permite eliminar un producto de la base de datos solicitando confirmación del usuario.

    Realiza una búsqueda previa del ID y elimina el registro si se confirma.
    """
    con, cur= conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None         
    else:
        try:    
            continuar_eliminar= True
            id=buscar_id()
            while continuar_eliminar: 
                print("Seguro que desea eliminar este producto?")
                print("1. Si")
                print("2. No")
                eleccion_eliminar= input("Elija su opcion: ")
                resultado_eliminar= opcion_eliminar(eleccion_eliminar)
                if resultado_eliminar == 1:
                    try:
                        query = """DELETE FROM productos WHERE id = ?"""
                        cur.execute(query, (id,))
                        con.commit()
                        print(Fore.GREEN + "Producto eliminado con éxito")
                    except sqlite3.Error as error:
                        print(f"Error al eliminar: {error}")
                    finally:
                        continuar_eliminar = False
                elif resultado_eliminar == 2:
                    continuar_eliminar = False
        finally:
            con.close()
                 
                
#----------------------------------------------------------------------VERIFICAR STOCK-------------------------------------------------------------------------------------------
def entrada_cantidad(entrada):
    """
    Valida la entrada del usuario para filtros de cantidad con operadores (>, <, =).

    Parámetros:
        entrada (str): Expresión ingresada por el usuario (ej. '>10', '50', '=5').

    
    """
    if entrada.isdigit():
        return '=', int(entrada)  
    elif entrada and entrada[0] in "<>=" and entrada[1:].isdigit():
        return entrada[0], int(entrada[1:])  
    else:
        print("Entrada inválida. Solo se permiten números o expresiones como <123, >50, =10.")
        return None, None

    i







def verificar_stock():
    """
    Solicita al usuario una condición de cantidad y muestra los productos que cumplen con ella.

    Permite usar operadores como '<', '>', '=' para realizar la búsqueda.
    """
    con, cur= conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None      
    else:
        continuar_stock= True
        while continuar_stock:
            stock=input("cantidad a verificar: ")
            if stock.lower() == 'salir':
                continuar_stock = False
            else:
                operador, cantidad = entrada_cantidad(stock)
                if cantidad is not None:
                    try:#TRY/EXCEPT COMO DECIA EL FEEDBACK
                        query = f"SELECT * FROM productos WHERE cantidad {operador} ?"
                        cur.execute(query, (cantidad,))
                        resultados = cur.fetchall()
                        print(tabulate(resultados, headers=["ID", "Nombre", "Descripcion", "Categoria", "Precio", "Categoria"], tablefmt="double_grid"))
                        return resultados
                    except sqlite3.Error as error:
                        print(f"Error en la base de datos {error}")
                else:
                    print(Fore.RED + "No se encontraron productos")
        con.close()                    
                        
#------------------------------------------------------------------------USUARIO-----------------------------------------------------------------------------------------
def opcion_usuario(opcion):
    opciones=[1,2,3]
    try:#TRY/EXCEPT COMO DECIA EL FEEDBACK
        opcion= int(opcion)
        if opcion in opciones:
            return opcion
        else:
            print(Fore.YELLOW + "La opcion debe ser 1 o 2")
            return
    except ValueError:
        print(Fore.RED + "La opcion debe ser un numero.")
    
        
    
#-------------------------------------------------------------------------------------------------MOSTRAR  TODOS PRODUCTOS USUARIOS----------------------------------------------------------
def mostrar_productos_usuarios():
    """
    Muestra todos los productos disponibles en la base de datos.
    """
    con,cur=conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None         
    else:
        try:#TRY/EXCEPT COMO DECIA EL FEEDBACK
            query="""SELECT ID,nombre, descripcion,precio,categoria FROM productos"""
            cur.execute(query)
        except sqlite3.Error as error:
            print(f"error al consultar la base de datos")       
        else:
            resultado_inventario= cur.fetchall()
            if resultado_inventario:
                print("Se encontraron estos productos")
                print(tabulate(resultado_inventario, headers=["ID", "Nombre", "Descripcion","Precio","Categoria"], tablefmt="double_grid"))      
            else:
                print("no hay productos en el inventario")
        finally:
            con.close()            
        
#.------------------------------------------------------------------BUSCAR PRODUCTO USUARIO-------------------------------------------------------------------
#NUSCAR POR ID
def buscar_id_usuario():
    """
    Solicita al usuario una ID de producto y la valida.

    Retorna:
        str: La ID ingresada si es válida.
        None: Si la ID no es válida o ocurre un error.
        """
    continuar_id= True
    while continuar_id:
        id_producto= input("Escriba la id a buscar: ")
        try:#IMPLEMENTACION DE TRY/EXCEPT COMO DECIA EL FEEDBACK
            id= int(id_producto)
            if id_producto <= 0:
                print(Fore.YELLOW + "La ID no puede ser 0")
            else:
                continuar_id=False
                return id_producto
        except ValueError:
            print("La ID debe ser numerica.")
            
def buscar_por_id_usuario():
    """
    Busca un producto en la base de datos usando su ID.

    Muestra la información del producto si se encuentra.

    Retorna:
        tuple: Información del producto si se encuentra.
        None: Si no se encuentra el producto o ocurre un error.
    """
    con, cur= conexion()
    if con is None or cur is None:
        print("No se puede conectar a la base de datos.")
        return None         
    else:
        producto_id=buscar_id()
        try:#TRY/EXCEPT COMO DECIA EL FEEDBACK
            query="""SELECT ID,nombre,descripcion,precio,categoria FROM productos WHERE id= ?"""
            cur.execute(query,(producto_id,))
            resultado_id= cur.fetchone()
            if resultado_id:
                print(tabulate([resultado_id], headers=["ID", "Nombre", "Descripcion","Precio","Categoria"], tablefmt="double_grid"))  
                return resultado_id
            else:
                print(Fore.RED + "Producto no encontrado")
        except sqlite3.Error as error:
            print(Fore.RED + f"ERROR EN LA BASE DE DATOS,{error}")
            return None
        finally:
            con.close()
    
from funciones_logging import *
from funciones_crud import *
def main():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Ya soy usuario")
        print("2. Crear usuario")
        opcion = input("Elija una opción: ")
        validar = validar_menu(opcion)
        if validar == 1:
            rol = validar_credenciales()
            if rol:
                if rol == "admin":
                    while True:
                        print("---ADMINISTRADOR----")
                        print("1. Agregar producto")
                        print("2. Mostrar inventario")
                        print("3. Busqueda por ID")
                        print("4. Actualizar por ID")
                        print("5. Eliminar por ID")
                        print("6. Verificar stock")
                        opcion= input("Elija una opcion:")
                        seleccion = crud_admin(opcion)  
                        if seleccion == 1:
                            pedir_inputs_agregar()
                        elif seleccion == 2:
                            mostrar_inventario()
                        elif seleccion == 3:
                            buscar_por_id()
                        elif seleccion == 4:
                            actualizar_por_id()
                        elif seleccion == 5: 
                            verificar_stock()
                        elif seleccion == 6:
                            print("Saliendo...")
                            break
                elif rol == "usuario":
                    print("------USUARIO----------")
                    print("1. Mostrar productos")
                    print("2. Producto especifico")
                    opcion= input("Elija su opcion")
                    resultado= opcion_usuario(opcion)
                    if resultado == 1:
                        mostrar_productos_usuarios()
                    elif resultado == 2:
                        buscar_por_id_usuario()
                        

        elif validar == 2:
            datos = inputs_crear()
            if datos:
                crear_usuario(*datos)
            else:
                print("Registro cancelado o fallido.")
                
                
if __name__ == "__main__":
    main()
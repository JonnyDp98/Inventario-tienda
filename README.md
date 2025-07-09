# 🛒 Inventario de Tienda

**Inventario de Tienda** es una aplicación de consola desarrollada en Python que permite gestionar productos de una tienda. El sistema ofrece distintas funcionalidades dependiendo del tipo de usuario (administrador o visitante).

## 📋 Descripción

El sistema permite realizar operaciones de **alta, baja, modificación y búsqueda (ABM)** de productos si el usuario tiene permisos administrativos. Si el usuario es un visitante, solo puede **visualizar los productos disponibles** o **buscar un producto por su ID**.

---

## 💻 Tecnologías y librerías utilizadas

- "sqlite3": para la gestión de la base de datos local.(Estandar en Python)
- "datetime": para el manejo de fechas y tiempos.(Estandar en Python)
- "bcrypt": para el cifrado de contraseñas.(Dependencia)
- "colorama": para el resaltado de texto en la consola.(Dependencia)
- "csv": para operaciones con archivos CSV.(Estandar en Python)
- "re": para validaciones con expresiones regulares.(Estandar en Python)
- "tabulate":ermite mostrar listas o datos tabulares en formato de tabla.(Dependencia)

---

## ⚙️ Instalación

1. Clona este repositorio o descarga los archivos del proyecto.
2. Asegúrate de tener Python instalado (versión 3.8 o superior).
3. Instala las dependencias necesarias ejecutando:

```bash
pip install bcrypt colorama tabulate


## ▶️ Cómo usar la aplicación

Desde la terminal:

```bash
python main.py



## Autor

**Jonathan Romero**

**Nota Extra para el uso**
Para las cuentas admin ingresar la contraseña: Admin123!   y para los usuarios comunes usar Usuario123!


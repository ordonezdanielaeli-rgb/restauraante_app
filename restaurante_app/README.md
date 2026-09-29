# Restaurante App - Semana 16

## Descripción

Restaurante App es una aplicación desarrollada en Python utilizando Tkinter para gestionar información básica de un restaurante mediante una interfaz gráfica.

El proyecto continúa la aplicación desarrollada en semanas anteriores y mantiene una arquitectura modular para separar los datos, modelos, servicios e interfaz gráfica.

## Objetivo

Aplicar los conceptos de manejo de eventos mediante botones y componentes de Tkinter, permitiendo realizar operaciones básicas sobre los productos del restaurante.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
└── main.py

README.md
```

## Componentes utilizados

* Tkinter
* ttk
* Frame
* LabelFrame
* Label
* Entry
* Button
* Notebook
* Treeview

## Funcionalidades

### Inicio de sesión

La aplicación inicia mostrando una pantalla de acceso. Las credenciales son validadas mediante `RestauranteServicio`.

### Productos

La sección de productos permite:

* Registrar productos.
* Consultar productos mediante su ID.
* Cargar la información de un producto.
* Actualizar productos.
* Eliminar productos.
* Mostrar los productos en una tabla.
* Guardar los cambios en `productos.json`.

### Usuarios

La sección de usuarios permite consultar la información registrada en `usuarios.json`.

## Manejo de eventos

Las acciones de los botones se realizan mediante el parámetro `command=` de Tkinter.

Los botones utilizados son:

* Registrar.
* Cargar / Consultar.
* Actualizar.
* Eliminar.
* Limpiar.
* Cerrar sesión.

## Persistencia

La información de los productos se almacena en el archivo:

```text
restaurante_app/datos/productos.json
```

La lectura y escritura de los archivos JSON se realiza mediante `ArchivoServicio`.

Las operaciones y validaciones relacionadas con los productos se encuentran en `RestauranteServicio`.

## Flujo de la aplicación

```text
Inicio
   ↓
LoginView
   ↓
Validación mediante RestauranteServicio
   ↓
MainView
   ↓
Productos / Usuarios
   ↓
Operaciones sobre productos
   ↓
RestauranteServicio
   ↓
productos.json
   ↓
Actualización de la interfaz
```

## Ejecución

Desde la carpeta `restaurante_app`, ejecutar:

```bash
python main.py
```

## Usuario de prueba

```text
Usuario: admin
Contraseña: 1234
```

## Tecnologías

* Python
* Tkinter
* JSON
* Programación Orientada a Objetos
* Arquitectura modular

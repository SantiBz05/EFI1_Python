# API de Tienda de Celulares

Esta API permite gestionar equipos en el sistema. Se pueden realizar operaciones de obtención, creación, edición y eliminación de equipos.

## Endpoints
### Autenticación (POST)
**Obtener token de autenticacion**
- **URL**: `/login`
- **Método**: `POST`
- **Descripción**: Permite obtener el token de autenticacion en condicion de admin o usuario estandar.
#### Ejemplo de Solicitud

```bash
{
        "usuario" : "admin",
        "contrasenia" : "admin",
}
```
#### Respuesta Exitosa
```
[
    "token: Bearer -token de autenticacion-"
]
```
### 1. Obtener Equipos (GET)

- **URL**: `/equipos`
- **Método**: `GET`
- **Descripción**: Recupera una lista de todos los equipos. Los administradores obtendrán todos los detalles, mientras que los usuarios normales recibirán una versión simplificada.
  
#### Ejemplo de Solicitud

```bash
{
        "username": "admin",
        "password": "admin",
}
```
#### Respuesta Exitosa
```
[
    {
        "id": 1,
        "precio": 1500.00,
        "modelo_id": 2,
        "marca_id": 1,
        "caracteristicas_id": 3,
        "categoria_id": 4,
        "proveedor_id": 5,
        "activo": true
    }
    ...
]
```
### 2. Crear un Nuevo Equipo (POST)
- **URL**: /equipos
- **Método**: POST
- **Descripción**: Crea un nuevo equipo en el sistema. Solo los administradores pueden crear nuevos equipos.
#### Ejemplo de Solicitud
```bash
{
    "precio": 1500.00,
    "modelo_id": 2,
    "marca_id": 1,
    "caracteristicas_id": 3,
    "categoria_id": 4,
    "proveedor_id": 5,
    "activo": true
}
```
#### Respuesta Exitosa
```
{
    "id": 1,
    "precio": 1500.00,
    "modelo_id": 2,
    "marca_id": 1,
    "caracteristicas_id": 3,
    "categoria_id": 4,
    "proveedor_id": 5,
    "activo": true
}
```

### 3. Actualizar un Equipo (PUT)
- **URL**: /equipos
- **Método**: PUT
- **Descripción**: Actualiza la información de un equipo existente. Solo los administradores pueden realizar esta acción.
#### Ejemplo de Solicitud
```bash
{
    "id": 1,
    "precio": 1600.00,
    "modelo_id": 3,
    "marca_id": 2,
    "caracteristicas_id": 4,
    "categoria_id": 5,
    "proveedor_id": 6,
    "activo": true
}
```
#### Respuesta Exitosa
``` bash
{
    "id": 1,
    "precio": 1600.00,
    "modelo_id": 3,
    "marca_id": 2,
    "caracteristicas_id": 4,
    "categoria_id": 5,
    "proveedor_id": 6,
    "activo": true
}
```

### 4. Eliminar un Equipo (DELETE)
- **URL**: /equipos
- **Método**: DELETE
- **Descripción**: Elimina un equipo del sistema. Solo los administradores pueden realizar esta acción.
#### Ejemplo de Solicitud
``` bash
{
    "id": 1
}
```
#### Respuesta Exitosa
```
{
    "Mensaje": "Equipo eliminado correctamente."
}
```
#### Notas
- **Asegúrate de incluir un token JWT válido en el encabezado de autorización para todas las solicitudes que requieran autenticación.** 
- **Solo los usuarios con privilegios de administrador pueden crear, actualizar o eliminar equipos.**
- 
### 5. Ver registros de un modelo (GET)
- **Descripción**: Este método te permitira ver los registros existentes en los siguientes modelos:
- Marca
- Categoria
- Proveedor
- Inventario
- Accesorio
- Caracteristica
- Facbricante
- Modelo
- Pedido
- Sucursal
- mpleado
- Cliente
- Venta
- **URL**: /ruta del modelo al que quieras acceder
- **Método**: GET
#### Ejemplo de Solicitud
- Para acceder a los registros solo has de introducir el token que indica que has logeado sesion correctamente y luego ejecutar el metodo GET en la direccion url que desees.

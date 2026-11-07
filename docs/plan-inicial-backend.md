# Plan técnico inicial del backend de TaskFlow

## Arquitectura

API monolítica sencilla con FastAPI, Pydantic y SQLAlchemy:

- Las rutas HTTP validan solicitudes y definen las respuestas.
- Los esquemas Pydantic describen las entradas y salidas.
- Una capa CRUD encapsula las consultas y escrituras.
- Los modelos SQLAlchemy representan las tablas SQLite.
- Una sesión de base de datos se crea por solicitud y se cierra al terminar.
- La aplicación permite inyectar un motor de base de datos para que las pruebas no usen la base de desarrollo.

No se añaden dependencias. Se utilizan FastAPI, SQLAlchemy y Uvicorn ya declarados, Pydantic incluido con FastAPI y Pytest, HTTPX y Ruff del grupo de desarrollo.

## Estructura propuesta

```text
taskflow-backend/
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       └── tasks.py
├── docs/
│   └── plan-inicial-backend.md
└── tests/
    ├── conftest.py
    └── test_tasks.py
```

### Responsabilidad por archivo

- `.gitignore`: excluye `.venv/`, cachés de Python/Pytest/Ruff, archivos `*.pyc` y la base local `taskflow.db`.
- `app/__init__.py`: marca `app` como paquete Python.
- `app/main.py`: crea la aplicación, registra CORS limitado a `http://localhost:5173`, monta el router y prepara las tablas al iniciar.
- `app/database.py`: define la ruta absoluta de SQLite relativa al directorio del proyecto, el motor, la fábrica de sesiones y la dependencia de sesión por solicitud.
- `app/models.py`: define la tabla y el modelo SQLAlchemy de tareas.
- `app/schemas.py`: define esquemas de creación, actualización y respuesta, junto con las opciones permitidas de estado y prioridad.
- `app/crud.py`: implementa lectura, creación, actualización y eliminación.
- `app/routers/__init__.py`: marca el paquete de rutas.
- `app/routers/tasks.py`: declara los endpoints y convierte los casos sin resultado en respuestas `404`.
- `tests/conftest.py`: configura un motor SQLite temporal, una aplicación de prueba y un cliente HTTP aislados de la base de desarrollo.
- `tests/test_tasks.py`: cubre los casos de éxito y validación de los endpoints.

## Endpoints REST

| Método | Ruta | Resultado |
|---|---|---|
| `POST` | `/tasks` | Crea una tarea; responde `201` con el recurso creado. |
| `GET` | `/tasks` | Devuelve la lista de tareas; responde `200`, también si está vacía. |
| `GET` | `/tasks/{task_id}` | Devuelve la tarea (`200`) o `404` si no existe. |
| `PUT` | `/tasks/{task_id}` | Reemplaza la tarea (`200`) o responde `404` si no existe. |
| `DELETE` | `/tasks/{task_id}` | Elimina la tarea (`204`) o responde `404` si no existe. |

## Modelo de datos

Tabla `tasks`:

| Campo | Tipo | Reglas |
|---|---|---|
| `id` | Entero | Clave primaria autoincremental. |
| `title` | Texto | Obligatorio, no vacío ni compuesto solo por espacios. |
| `description` | Texto nullable | Opcional. |
| `priority` | Texto | Obligatorio: `baja`, `media` o `alta`. |
| `status` | Texto | Obligatorio: `pendiente`, `en_progreso` o `completada`. |

La base de desarrollo será `taskflow.db` en la raíz del proyecto, sin depender del directorio de trabajo desde el que se invoque Uvicorn.

## Validación y errores

- Pydantic rechazará títulos vacíos o con solo espacios, y recortará espacios alrededor de un título válido.
- Al crear, título, prioridad y estado son obligatorios; descripción puede omitirse.
- En `PUT`, título, prioridad y estado son obligatorios; descripción puede omitirse y, si se omite, quedará en `null`.
- Valores de estado o prioridad fuera de las opciones declaradas se rechazan.
- Errores de validación devuelven el formato estándar FastAPI `422` con el detalle del campo.
- Un ID inexistente devuelve `404` con el formato estándar `detail` de FastAPI.
- No se imponen límites de longitud ni paginación en esta primera versión.

## Pruebas automatizadas

Las pruebas usan una base SQLite temporal distinta de `taskflow.db` y un motor inyectado a la aplicación de prueba.

1. Crear tarea con todos los campos y comprobar `201` y la respuesta.
2. Crear tarea sin descripción y comprobar que se acepta.
3. Listar una colección vacía y una colección con tareas.
4. Consultar una tarea existente y una inexistente.
5. Actualizar con `PUT` y comprobar todos los campos.
6. Eliminar y comprobar que deja de estar disponible.
7. Comprobar `404` al actualizar o eliminar una tarea inexistente.
8. Comprobar `422` para título vacío o en blanco, prioridad inválida, estado inválido y campos requeridos ausentes.
9. Comprobar que solicitudes CORS del frontend local reciben permiso y que un origen diferente no se autoriza.

## Secuencia de implementación

1. Crear este documento y el `.gitignore`.
2. Implementar conexión y modelo SQLAlchemy con base local en ruta estable.
3. Definir los esquemas Pydantic y validaciones.
4. Implementar CRUD y rutas REST.
5. Configurar la fábrica de aplicación, CORS y creación de esquema al iniciar.
6. Configurar pruebas aisladas con SQLite temporal.
7. Ejecutar Pytest y Ruff, y corregir los errores encontrados.
8. Documentar los comandos de uso local.

## Comandos para Windows CMD

Ejecutar desde la raíz del proyecto:

```cmd
uv run uvicorn app.main:app --reload
```

La documentación interactiva estará en `http://127.0.0.1:8000/docs`.

En otra ventana de CMD, también desde la raíz:

```cmd
uv run pytest
uv run ruff check .
```

## Riesgos y decisiones

- La creación de tablas al iniciar es suficiente para el proyecto educativo, pero no ofrece migraciones. Se reconsiderará si el esquema evoluciona o se conservan datos entre versiones.
- La descripción omitida en `PUT` se establecerá en `null`, manteniendo el significado de reemplazo completo.
- El listado es ilimitado y usa ID entero autoincremental para mantener pequeño el contrato inicial.
- CORS permite el origen exacto `http://localhost:5173`; otros orígenes no deben considerarse autorizados.
- El motor de pruebas se inyecta para evitar cualquier escritura o inicialización de esquema sobre la base de desarrollo.

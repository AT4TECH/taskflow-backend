# AGENTS.md — TaskFlow Backend

## Propósito del repositorio

Este repositorio contiene la API REST de TaskFlow, una aplicación para gestionar tareas.

El backend permite crear, consultar, actualizar y eliminar tareas. La API está destinada al frontend React. CORS permite el origen `http://localhost:5173`.

## Stack tecnológico

- Python 3.12 para desarrollo, según `.python-version`. El requisito declarado en `pyproject.toml` es Python `>=3.12`.
- FastAPI para los endpoints HTTP.
- SQLAlchemy para el acceso a datos.
- SQLite como base de datos local.
- uv para gestionar dependencias y ejecutar comandos.
- Pytest para las pruebas automatizadas.
- Ruff para el análisis estático y el estilo del código.

## Comandos del proyecto

Ejecutar desde la raíz del repositorio.

Instalar o sincronizar dependencias:

```cmd
uv sync
```

Iniciar el servidor de desarrollo. Al arrancar, la aplicación puede crear las tablas que falten en la base de datos local `taskflow.db`.

```cmd
uv run uvicorn app.main:app --reload
```

Ejecutar las pruebas. Las pruebas de API deben reutilizar la fixture `client` de `tests/conftest.py`, que usa una base SQLite temporal.

```cmd
uv run pytest
```

Verificar el estilo del código:

```cmd
uv run ruff check .
```

Documentación interactiva de la API:

`http://127.0.0.1:8000/docs`

## Organización del código

- `app/main.py`: inicialización de FastAPI y configuración principal.
- `app/database.py`: conexión y sesión de base de datos.
- `app/models.py`: modelos de persistencia de SQLAlchemy.
- `app/schemas.py`: esquemas de entrada y salida.
- `app/crud.py`: operaciones de acceso y modificación de datos.
- `app/routers/tasks.py`: rutas HTTP de las tareas.
- `tests/`: pruebas automatizadas.
- `docs/`: documentación y planes del proyecto.

## Reglas de arquitectura

1. Mantener las rutas HTTP en `app/routers/`.
2. Mantener las operaciones de persistencia en `app/crud.py`.
3. Definir los modelos de base de datos en `app/models.py`.
4. Definir los esquemas de validación en `app/schemas.py`.
5. Evitar colocar consultas SQL directamente en los endpoints.
6. Mantener la compatibilidad de los contratos JSON consumidos por el frontend.
7. No introducir nuevas dependencias sin justificar su necesidad.

### Contrato HTTP de tareas

- `GET /tasks` devuelve la lista de tareas con `200`.
- `POST /tasks` crea una tarea y devuelve el recurso con `201`.
- `GET /tasks/{task_id}` devuelve la tarea con `200`.
- `PUT /tasks/{task_id}` reemplaza la tarea completa y devuelve el recurso actualizado con `200`.
- `DELETE /tasks/{task_id}` elimina la tarea y devuelve `204` sin cuerpo.
- Las operaciones sobre una tarea inexistente devuelven `404`. Los datos de entrada inválidos devuelven `422`.

## Convenciones del equipo

- Usar `snake_case` para funciones, variables y archivos Python.
- Usar `PascalCase` para clases.
- Mantener nombres descriptivos y código legible.
- Agregar o actualizar pruebas cuando cambie el comportamiento de la API.
- Ejecutar Pytest y Ruff antes de dar por terminada una implementación.
- Trabajar en ramas independientes creadas desde `main`.
- Utilizar nombres de rama como `feat/nombre-de-la-mejora`, `fix/nombre-del-error` o `chore/nombre-de-la-tarea`.
- Utilizar mensajes de commit descriptivos, por ejemplo `feat: agregar filtro de tareas`.

## Restricciones de seguridad

- No publicar credenciales, tokens ni archivos `.env`.
- No incluir la base de datos local `taskflow.db` en Git.
- No modificar ni eliminar datos existentes sin autorización.
- No ejecutar comandos destructivos sin aprobación.
- No modificar configuraciones de producción sin autorización.
- No cambiar endpoints existentes sin considerar el impacto en el frontend.
- No modificar archivos ajenos a la solicitud sin una justificación clara.

## Trabajo con agentes de IA

Las inspecciones de solo lectura pueden realizarse sin aprobación.

Antes de modificar cualquier archivo:

1. Leer este archivo y revisar los archivos relacionados.
2. Identificar los componentes afectados.
3. Proponer un plan con archivos, pasos, riesgos y pruebas.
4. Obtener la aprobación explícita del usuario antes de modificar archivos.
5. Implementar únicamente el alcance aprobado.
6. Ejecutar las verificaciones correspondientes.
7. Resumir los cambios y sus resultados.

Para las solicitudes del taller, la implementación debe realizarse en una rama y fusionarse a `main` mediante un pull request. Crear y fusionar un pull request son acciones separadas, y cada una requiere autorización del equipo.
---
name: validar-api-taskflow
description: Valida el contrato HTTP de la API REST de TaskFlow cuando se solicite comprobar su comportamiento o detectar regresiones en los endpoints de tareas.
---

# Validar la API de TaskFlow

1. Desde la raíz del repositorio, lee `AGENTS.md` y compara el contrato con `app/routers/tasks.py`, `app/schemas.py` y las aserciones de `tests/test_tasks.py`.
2. Reutiliza la fixture `client` de `tests/conftest.py`. Configura el cliente con el motor de pruebas y sustituye `get_db` para que las solicitudes y la limpieza de tablas usen SQLite temporal. Ejecuta las operaciones de escritura únicamente mediante esa fixture. Evita iniciar el servidor de desarrollo o abrir, modificar o eliminar `taskflow.db`.
3. Ejecuta ambos comandos con el entorno existente.

   ```text
   uv run --no-sync --offline pytest -rA
   uv run --no-sync --offline ruff check .
   ```

   Si falta una herramienta o dependencia, registra qué comando quedó bloqueado y ejecuta las comprobaciones que sigan disponibles. Pide autorización antes de instalar dependencias o ejecutar scripts externos.

## Contrato que se debe comprobar

- `GET /tasks` devuelve `200` y una lista JSON, incluso cuando está vacía.
- `POST /tasks` devuelve `201` y la tarea creada.
- `GET /tasks/{task_id}` devuelve `200` y la tarea solicitada.
- `PUT /tasks/{task_id}` reemplaza la tarea completa y devuelve `200` con la tarea actualizada.
- `DELETE /tasks/{task_id}` devuelve `204` con el cuerpo vacío.
- Una tarea inexistente devuelve `404` al consultarla, reemplazarla o eliminarla. Las entradas inválidas devuelven `422`.
- Las representaciones JSON de una tarea respetan los campos y tipos de `TaskRead`.

## Informe

Enumera las pruebas aprobadas, fallidas y omitidas. Resume el resultado de Ruff e identifica qué aspectos del contrato quedaron sin verificar y por qué. Distingue los fallos observados de los casos que la suite no cubre. Limita el trabajo a la validación y al informe, sin cambiar el contrato, la implementación ni las pruebas.

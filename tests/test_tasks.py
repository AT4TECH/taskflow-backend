from fastapi.testclient import TestClient


def task_payload() -> dict[str, str]:
    return {
        "title": "Preparar entrega",
        "description": "Revisar el proyecto",
        "priority": "alta",
        "status": "pendiente",
    }


def create_task(client: TestClient) -> dict[str, object]:
    response = client.post("/tasks", json=task_payload())
    assert response.status_code == 201
    return response.json()


def test_create_task_with_optional_description(client: TestClient) -> None:
    payload = task_payload()
    payload.pop("description")

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    assert response.json()["description"] is None
    assert response.json()["title"] == "Preparar entrega"


def test_list_tasks_empty_and_with_results(client: TestClient) -> None:
    assert client.get("/tasks").json() == []

    task = create_task(client)
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [task]


def test_read_existing_and_missing_task(client: TestClient) -> None:
    task = create_task(client)

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json() == task
    assert client.get("/tasks/999").status_code == 404


def test_replace_task_with_put(client: TestClient) -> None:
    task = create_task(client)
    updated = {
        "title": "Entrega lista",
        "priority": "media",
        "status": "completada",
    }

    response = client.put(f"/tasks/{task['id']}", json=updated)

    assert response.status_code == 200
    assert response.json() == {
        "id": task["id"],
        "title": "Entrega lista",
        "description": None,
        "priority": "media",
        "status": "completada",
    }


def test_put_missing_task_returns_404(client: TestClient) -> None:
    response = client.put("/tasks/999", json=task_payload())

    assert response.status_code == 404


def test_delete_task_and_missing_task(client: TestClient) -> None:
    task = create_task(client)

    response = client.delete(f"/tasks/{task['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{task['id']}").status_code == 404
    assert client.delete("/tasks/999").status_code == 404


def test_rejects_empty_or_whitespace_title(client: TestClient) -> None:
    for title in ("", "   "):
        payload = task_payload()
        payload["title"] = title

        response = client.post("/tasks", json=payload)

        assert response.status_code == 422


def test_rejects_invalid_priority_and_status(client: TestClient) -> None:
    for field, value in (("priority", "urgente"), ("status", "bloqueada")):
        payload = task_payload()
        payload[field] = value

        response = client.post("/tasks", json=payload)

        assert response.status_code == 422


def test_create_requires_priority_and_status(client: TestClient) -> None:
    for field in ("priority", "status"):
        payload = task_payload()
        payload.pop(field)

        response = client.post("/tasks", json=payload)

        assert response.status_code == 422


def test_put_requires_editable_fields(client: TestClient) -> None:
    task = create_task(client)

    response = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Actualizada", "priority": "baja"},
    )

    assert response.status_code == 422


def test_cors_allows_only_local_frontend(client: TestClient) -> None:
    allowed = client.options(
        "/tasks",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    disallowed = client.options(
        "/tasks",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert allowed.status_code == 200
    assert (
        allowed.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )
    assert disallowed.status_code == 400
    assert "access-control-allow-origin" not in disallowed.headers

from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import create_app


@pytest.fixture
def test_engine(tmp_path) -> Generator[Engine, None, None]:
    database_url = URL.create(
        "sqlite",
        database=str(tmp_path / "test_tasks.db"),
    )
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def client(test_engine: Engine) -> Generator[TestClient, None, None]:
    app: FastAPI = create_app(test_engine)
    test_session = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    def override_get_db() -> Generator[Session, None, None]:
        with test_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)

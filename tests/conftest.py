"""Conftest package

Defines test settings, fixtures and dependencies overrides.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import get_test_settings
from src.database import Base
from src.main import app, get_db

settings = dict(get_test_settings())
SQLALCHEMY_DATABASE_URL = settings["SQLALCHEMY_DATABASE_URL"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def client(session):
    # Dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

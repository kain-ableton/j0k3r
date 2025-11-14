from __future__ import annotations
import os, importlib, pkgutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Declarative base used by all models
Base = declarative_base()

# Global engine/session factory
_engine = None
_SessionLocal: sessionmaker | None = None

def _default_db_url() -> str:
    # SQLite file under settings/
    settings = Path("settings")
    settings.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{(settings/'jok3r.sqlite').resolve()}"

def init_engine(url: str | None = None, echo: bool = False):
    """Initialize global SQLAlchemy engine and session factory."""
    global _engine, _SessionLocal
    if url is None:
        url = os.getenv("JOK3R_DB_URL", _default_db_url())
    if _engine is None or str(_engine.url) != url:
        connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
        _engine = create_engine(url, echo=echo, future=True, connect_args=connect_args)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
    return _engine

def get_engine():
    if _engine is None:
        init_engine()
    return _engine

def get_session():
    """Return a new Session; caller is responsible for closing it."""
    if _SessionLocal is None:
        init_engine()
    return _SessionLocal()  # type: ignore[misc]

def import_all_models():
    """Import all model modules under lib.db (except base/Session/__init__/enums)."""
    import lib.db as db_pkg  # noqa: F401
    pkg = db_pkg
    skip = {"__init__", "base", "Session", "enums"}
    prefix = pkg.__name__ + "."
    for _, name, _ in pkgutil.iter_modules(pkg.__path__, prefix):
        short = name.rsplit(".", 1)[-1]
        if short in skip:
            continue
        importlib.import_module(name)

def create_all():
    """Initialize engine, import models, and create tables."""
    eng = init_engine()
    import_all_models()
    Base.metadata.create_all(bind=eng)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
### Db > Base
###
import sqlalchemy
import sqlalchemy.orm
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

try:  # SQLAlchemy >= 1.4
    from sqlalchemy.orm import declarative_base
except ImportError:  # SQLAlchemy 1.2–1.3
    from sqlalchemy.ext.declarative import declarative_base

from lib.core.Config import *


Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///' + DB_FILE)
Session = sqlalchemy.orm.sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""

    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

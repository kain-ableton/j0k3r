#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
### Db > Base
###
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from lib.core.Config import *


Base = sqlalchemy.ext.declarative.declarative_base()
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

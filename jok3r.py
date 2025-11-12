#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
# Jok3r main function
###
import os
import sys
import traceback

from sqlalchemy.exc import SQLAlchemyError

from lib.core.ArgumentsParser import ArgumentsParser
from lib.core.Config import *
from lib.core.Exceptions import (ArgumentsException, AttackException,
                                 EnvironmentException, SettingsException)
from lib.core.Settings import Settings
from lib.controller.MainController import MainController
from lib.db.Mission import Mission
from lib.db.Session import Base, engine, session_scope
from lib.output.Logger import logger


def ensure_database_initialized():
    """Create required database tables if they do not already exist."""

    Base.metadata.create_all(engine)


def ensure_default_mission(session):
    """Guarantee that the default mission exists in the database."""

    mission = session.query(Mission).filter(Mission.name == 'default').first()
    if not mission:
        mission = Mission(name='default', comment='Default scope')
        session.add(mission)


def run_dependency_checks(settings):
    """Validate runtime prerequisites and surface actionable guidance."""

    issues = []

    db_dir = os.path.dirname(DB_FILE)
    if db_dir and not os.path.isdir(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except OSError as exc:
            issues.append('Cannot create database directory "{dir}": {err}'.format(
                dir=db_dir, err=exc))

    try:
        connection = engine.connect()
        connection.close()
    except SQLAlchemyError as exc:
        issues.append('Database connection failed: {err}'.format(err=exc))

    if settings.toolbox.nb_tools() == 0:
        issues.append('No tools loaded from toolbox configuration. '
                      'Verify settings/toolbox.conf and rerun the update workflow.')

    if issues:
        raise EnvironmentException('\n'.join(issues))


def main():
    print(BANNER)

    try:
        settings = Settings()
        run_dependency_checks(settings)
        arguments = ArgumentsParser(settings)

        ensure_database_initialized()

        with session_scope() as session:
            ensure_default_mission(session)
            controller = MainController(arguments, settings, session)
            controller.run()

        return 0

    except KeyboardInterrupt:
        print()
        logger.error('Ctrl+C received ! User aborted')
        return 130
    except EnvironmentException as exc:
        logger.error('Environment check failed. Resolve the following issues before retrying:')
        for issue in str(exc).splitlines():
            issue_text = issue.strip()
            if issue_text:
                logger.error('  - {0}'.format(issue_text.lstrip('- ')))
        return 2
    except (SettingsException, AttackException, ArgumentsException, ValueError) as exc:
        logger.error(exc)
        return 1
    except Exception as exc:  # pragma: no cover - defensive logging of unexpected issues
        logger.error('Unexpected error occured: {0}'.format(str(exc)))
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

import unittest
from uuid import uuid4

from lib.db.Mission import Mission
from lib.db.Session import Base, engine, session_scope
# Import all models to ensure SQLAlchemy relationships can be resolved
from lib.db.Host import Host  # noqa: F401
from lib.db.Service import Service  # noqa: F401
from lib.db.Screenshot import Screenshot  # noqa: F401
from lib.db.Credential import Credential  # noqa: F401
from lib.db.Option import Option  # noqa: F401
from lib.db.Product import Product  # noqa: F401
from lib.db.Result import Result  # noqa: F401
from lib.db.Vuln import Vuln  # noqa: F401
from lib.db.CommandOutput import CommandOutput  # noqa: F401


class SessionScopeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(engine)

    def test_commit_on_success(self):
        mission_name = f'unittest-{uuid4()}'

        with session_scope() as session:
            session.add(Mission(name=mission_name, comment='session-scope-test'))

        with session_scope() as session:
            mission = session.query(Mission).filter_by(name=mission_name).first()
            self.assertIsNotNone(mission)
            session.delete(mission)

    def test_rollback_on_exception(self):
        mission_name = f'unittest-{uuid4()}'

        with self.assertRaises(RuntimeError):
            with session_scope() as session:
                session.add(Mission(name=mission_name, comment='session-scope-rollback'))
                raise RuntimeError('boom')

        with session_scope() as session:
            mission = session.query(Mission).filter_by(name=mission_name).first()
            self.assertIsNone(mission)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

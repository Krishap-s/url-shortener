import pytest
import sqlalchemy

from infrastructure import db


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",
        action="store",
        default="sqlite:///:memory:",
        help="url of the database to use for tests",
    )


@pytest.fixture(scope="session")
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = request.config.getoption("--dburl")
    engine_ = sqlalchemy.create_engine(
        db_url.replace("postgres://", "postgresql://"), echo=True
    )
    yield engine_
    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    # Create tables
    """returns a SQLAlchemy scoped session factory"""
    return db.orm.scoped_session(db.orm.sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(request, db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    yield session_
    session_.rollback()
    session_.close()

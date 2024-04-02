from sqlalchemy.pool import NullPool


class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/test_db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@pgbouncer:5432/test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS= {
        'poolclass': NullPool,
    }

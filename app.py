import subprocess

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


@app.route('/init_db')
def create():
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()
    return 'OK'


@app.route('/create_error')
def create_error():
    user= User(name='Test User')
    try:
        db.session.begin()
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        user = User(name='Test User3')
        db.session.add(user)
        db.session.commit()
        # sqlalchemy.exc.PendingRollbackError: This Session's transaction has been rolled back due to a previous exception during flush.
        # To begin a new transaction with this Session, first issue Session.rollback().
        # Original exception was: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "user_name_key"
        # DETAIL:  Key (name)=(Test User) already exists.


@app.route('/create_error2')
def create_error2():
    try:
        db.session.begin()
        db.session.execute(text("SELECT * FROM something"))
    except Exception as e:
        print(e)
        user = User(name='Test User3')
        db.session.add(user)
        db.session.commit()
        # sqlalchemy.exc.InternalError: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block


@app.route('/create_error3')
def create_error3():
    engine = db.get_engine()
    with engine.connect() as connection:
        session = Session(bind=connection)
        session.begin()

        user = User(name='Test User3')
        session.add(user)

        with engine.connect() as connection2:
            session2 = Session(bind=connection2)
            session2.execute(text(
                "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'test_db' AND pid <> pg_backend_pid()"))

        session.commit()
        # sqlalchemy.exc.OperationalError: (psycopg2.errors.AdminShutdown) terminating connection due to administrator command
        # server closed the connection unexpectedly
        # 	This probably means the server terminated abnormally
        # 	before or while processing the request.

        # with pg_bouncer - no error


@app.route('/create_error4')
def create_error4():
    engine = db.get_engine()
    with engine.connect() as connection:
        session = Session(bind=connection)
        session.begin()

        user = User(name='Test User3')
        session.add(user)

        subprocess.check_output("ssh -o StrictHostKeyChecking=no test-postgres-db pkill -f postgres", shell=True)

        session.commit()
        # sqlalchemy.exc.OperationalError: (psycopg2.errors.AdminShutdown) terminating connection due to administrator command
        # server closed the connection unexpectedly
        # 	This probably means the server terminated abnormally
        # 	before or while processing the request.

    return "OK"


@app.route('/create_error5')
def create_error5():
    engine = db.get_engine()
    with engine.connect() as connection:
        session = Session(bind=connection)
        session.begin()

        user = User(name='Test User3')
        session.add(user)

        subprocess.check_output("ssh -o StrictHostKeyChecking=no test-postgres-db iptables -I INPUT -p tcp -m tcp --dport 5432 -j REJECT", shell=True)
        subprocess.check_output("ssh -o StrictHostKeyChecking=no test-postgres-db iptables -I OUTPUT -p tcp -m tcp --dport 5432 -j REJECT", shell=True)

        session.commit()

        # hangs

        subprocess.check_output(
            "ssh -o StrictHostKeyChecking=no test-postgres-db iptables -D INPUT -p tcp -m tcp --dport 5432 -j REJECT",
            shell=True)
        subprocess.check_output(
            "ssh -o StrictHostKeyChecking=no test-postgres-db iptables -D OUTPUT -p tcp -m tcp --dport 5432 -j REJECT",
            shell=True)

    return "OK"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', debug=True)

import sqlite3
from pathlib import Path
from flask import current_app, g

def get_db():
    if "db" not in g:
        db_path = Path(current_app.config["DATABASE"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db_path = Path(app.config["DATABASE"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(db_path)
        schema = Path(app.root_path, "database", "schema.sql").read_text(encoding="utf-8")
        db.executescript(schema)
        db.commit()
        db.close()
    app.teardown_appcontext(close_db)

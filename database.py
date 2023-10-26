import sqlalchemy
from databases import Database

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

Revista = sqlalchemy.Table(
    "revistas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("link", sqlalchemy.String),
    sqlalchemy.Column("image", sqlalchemy.String),
    sqlalchemy.Column("titulo", sqlalchemy.String),
)

metadata.create_all(engine)

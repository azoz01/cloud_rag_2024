import os
import sqlalchemy
import databases


database = databases.Database(f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_IP')}/user_history")

metadata = sqlalchemy.MetaData()

user_history = sqlalchemy.Table(
    "user_history",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, server_default=sqlalchemy.text("nextval('table_name_id_seq'::regclass)")),
    sqlalchemy.Column("username", sqlalchemy.String(30), nullable=False),
    sqlalchemy.Column("prompt", sqlalchemy.String(1000), nullable=False),
    sqlalchemy.Column("response", sqlalchemy.String(1000), nullable=True),
    sqlalchemy.Column("response_time", sqlalchemy.TIMESTAMP, nullable=True),
)

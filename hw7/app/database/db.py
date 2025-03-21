from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://store_user:SomePassword123@localhost/flowers_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_tables():
    Base.metadata.create_all(bind=engine)

# import psycopg2
# from psycopg2.extras import RealDictCursor
#
# def get_connection():
#     return psycopg2.connect(
#         host="localhost",
#         dbname="flowers_db",
#         user="store_user",
#         password="SomePassword123"
#     )

# def init_tables():
#     with get_connection() as conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cur:
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS users (
#                     id SERIAL PRIMARY KEY,
#                     email TEXT UNIQUE NOT NULL,
#                     full_name TEXT NOT NULL,
#                     password_hash TEXT NOT NULL,
#                     photo_url TEXT
#                 );
#             """)
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS flowers (
#                     id SERIAL PRIMARY KEY,
#                     name TEXT NOT NULL,
#                     quantity INT,
#                     price NUMERIC
#                 );
#             """)
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS purchase (
#                     id SERIAL PRIMARY KEY,
#                     user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
#                 );
#             """)
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS purchase_item (
#                     id SERIAL PRIMARY KEY,
#                     purchase_id INT NOT NULL REFERENCES purchase(id) ON DELETE CASCADE,
#                     flower_id INT NOT NULL REFERENCES flowers(id) ON DELETE CASCADE,
#                     quantity INT
#                 );
#             """)
#             conn.commit()  # ✅ Commits changes
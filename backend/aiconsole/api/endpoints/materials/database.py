from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql
import logging
from sqlalchemy import Column, Integer, String, Text, Enum, ARRAY, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String)
    usage = Column(Text)
    usage_examples = Column(ARRAY(Text))
    defined_in = Column(String)  # New field
    type = Column(String)  # New field
    default_status = Column(String)
    status = Column(String)  # New field
    override = Column(BOOLEAN)  # New field
    content_type = Column(Enum('api', 'dynamic_text', 'static_text', name='materialcontenttype'))
    content = Column(Text)
    content_static_text = Column(Text)
    default_status = Column(String)

_log = logging.getLogger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '../../../.env'))

try:
    load_dotenv(dotenv_path=project_root)
except Exception as e:
    _log.error(e)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# SQLAlchemy Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database_and_table():

    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;"),
        [DB_NAME]
    )
    db_exists = cursor.fetchone()

    if db_exists:
        _log.info(f"Database '{DB_NAME}' already exists. Skipping creation.")
        cursor.close()
        conn.close()
        return

    cursor.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(DB_NAME)
    ))
    _log.info(f"Database '{DB_NAME}' created successfully.")

    cursor.close()
    conn.close()

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = False
    cursor = conn.cursor()

    try:

        cursor.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'materialcontenttype') THEN
                            CREATE TYPE materialcontenttype AS ENUM ('static_text', 'dynamic_text', 'api');
                        END IF;
                    END
                    $$;
                """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id VARCHAR(255) PRIMARY KEY,        -- Ensure `id` is provided when inserting
                name VARCHAR(255) NOT NULL,
                version VARCHAR(50),
                usage TEXT,
                usage_examples TEXT[],
                content_type VARCHAR(50) NOT NULL,  -- Adjusted to VARCHAR for content type
                content TEXT,
                content_static_text TEXT,
                default_status VARCHAR(50) DEFAULT 'enabled',
                defined_in VARCHAR(255),
                type VARCHAR(50),
                status VARCHAR(50),
                override BOOLEAN DEFAULT FALSE
            );
        """)

        _log.info(f"Table 'materials' created successfully.")
        conn.commit()



        conn.commit()
    except Exception as e:
        conn.rollback()
        _log.error(f"Table 'materials' created successfully.")
    finally:
        cursor.close()
        conn.close()

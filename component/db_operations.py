from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.exc import SQLAlchemyError

def get_database_uri():
    host = os.environ.get("PG_HOST", "")
    port = os.environ.get("PG_PORT", "")
    username = os.environ.get("PG_USERNAME", "")
    password = os.environ.get("PG_PASSWORD", "")
    database_name = os.environ.get("PG_DB", "")
    database_schema = os.environ.get("PG_SCHEMA", "")
    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}?options=-csearch_path%3D{database_schema}"

def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Database migrations completed successfully!")
    except Exception as e:
        print(f"Error during database migration: {str(e)}")

def get_db_session():
    engine = create_engine(get_database_uri())
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    run_migrations()
    return get_db_session()

def test_database_connection():
    try:
        # Get the database URI
        db_uri = get_database_uri()
        
        # Create an engine
        engine = create_engine(db_uri)
        
        # Try to connect to the database
        with engine.connect() as connection:
            # Execute a simple query
            result = connection.execute("SELECT 1")
            
            # Fetch the result
            if result.scalar() == 1:
                print("Database connection successful!")
            else:
                print("Database connection failed: Unexpected result")
    
    except SQLAlchemyError as e:
        print(f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_database_connection()
    run_migrations()

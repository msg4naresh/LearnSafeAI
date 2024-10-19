import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def get_database_uri():
    host = os.environ.get("PG_HOST", "localhost")
    port = os.environ.get("PG_PORT", "5433")
    username = os.environ.get("PG_USERNAME", "postgres")
    password = os.environ.get("PG_PASSWORD", "postgres")
    database_name = os.environ.get("PG_DB", "learnsafeai")
    database_schema = os.environ.get("PG_SCHEMA", "public")
    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}?options=-csearch_path%3D{database_schema}"

def test_database_connection():
    try:
        db_uri = get_database_uri()
        engine = create_engine(db_uri)
        
        with engine.connect() as connection:
            # Use text() to create an executable SQL expression
            result = connection.execute(text("SELECT 1"))
            
            # Fetch the result (method differs between SQLAlchemy versions)
            if hasattr(result, 'scalar'):
                # For newer SQLAlchemy versions
                value = result.scalar()
            else:
                # For older SQLAlchemy versions
                value = result.fetchone()[0]
            
            if value == 1:
                print("Database connection successful!")
            else:
                print("Database connection failed: Unexpected result")
    
    except SQLAlchemyError as e:
        print(f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_database_connection()

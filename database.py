from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


# SQLALCHEMY_DATABASE_URL = f'{settings.DATABASE_URL}'
# SQLALCHEMY_DATABASE_URL = f'postgresql://root_joezzy:7i1GteVz51krwJdulNimlwb7FJzypuMP@dpg-cnj3om8l6cac739bqbig-a.oregon-postgres.render.com/fastapi_i719'
SQLALCHEMY_DATABASE_URL = f'postgres://root:7Iu1AruoCZCqbVwyD9Yc1RDQRnDma1x1@dpg-cnj4qd779t8c7399o0jg-a/fastapi_m4ho'

# SQLALCHEMY_DATABASE_URL = f'postgres://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}'


engine = create_engine( SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )


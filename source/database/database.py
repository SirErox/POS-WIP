from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
# Declaración Base
Base = declarative_base()

load_dotenv("any.env")
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_name=os.getenv("DB_NAME")

# Configuración de la Base de Datos
DATABASE_URL = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"  # Puedes cambiar por MySQL o PostgreSQL si necesitas.

# Creación del Motor
engine = create_engine(DATABASE_URL, echo=False)

# Creación de la Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar la base de datos
def init_db():
    from source.database.models import Table_usuario  # Importa tus modelos aquí
    Base.metadata.create_all(bind=engine)

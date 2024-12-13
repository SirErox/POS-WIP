from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from source.models import Base

load_dotenv("any.env")
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_name=os.getenv("DB_NAME")

engine=create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")

Base.metadata.create_all(engine)
print("tabla creada correctamente")
try:
    with engine.connect() as connection:
        print("conexion exitosa")
except Exception as e:
    print(f"error:{e}")

"""db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="test.db"
)

print("conexion exitosa") if db.is_connected() else print("FALLO")
"""
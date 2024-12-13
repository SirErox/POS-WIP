from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv("any.env")
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_name=os.getenv("DB_NAME")

engine=create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}") 
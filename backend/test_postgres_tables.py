from sqlalchemy import inspect
from app.database import engine

inspector = inspect(engine)

for table in inspector.get_table_names():
    print(table)
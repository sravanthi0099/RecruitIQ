from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://postgres:postgres123@localhost:5432/recruitiq"
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())
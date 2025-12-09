from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./app_backend/database.db"
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    from app_backend.models import User, Prediction
    SQLModel.metadata.create_all(engine)
    print("Database initialized and tables created!")

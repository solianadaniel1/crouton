# main.py

from fastapi import FastAPI, Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter, MemoryCRUDRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UserModel, Base
from schemas import UserCreate, User, UserUpdate

# SQLAlchemy database setup
DATABASE_URL = "sqlite:///./test.db"  # Change to your preferred database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI setup
app = FastAPI()

# Create CRUD router for SQLAlchemy
sqlalchemy_router = SQLAlchemyCRUDRouter(
    schema=User,
    create_schema=UserCreate,
    update_schema=UserUpdate,     
    db_model=UserModel,
    db=get_db,
    prefix="/users/"
)

# Create Memory CRUD router
memory_router = MemoryCRUDRouter(
    schema=User,
    create_schema=UserCreate,  
    update_schema=UserUpdate,  
    prefix="/memory-users/"
)

# Include both routers in the FastAPI app
app.include_router(sqlalchemy_router)
app.include_router(memory_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application"}

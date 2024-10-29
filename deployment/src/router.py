# main.py
from fastapi import FastAPI, Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter, MemoryCRUDRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UserModel, Base
from schemas import UserCreate, User, UserUpdate
from typing import List, Tuple, Type

# SQLAlchemy database setup
DATABASE_URL = "sqlite:///./test.db"  # Change to your preferred database
engine = create_engine(DATABASE_URL) #Creates a new SQLAlchemy engine instance for database interactions.
#creating new session objects. The session is used to interact with the database.
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

###############################create_route_objects and attach_list_of_routers#################

# Define a list of models and their corresponding schemas
models_and_schemas: List[Tuple[Type, Type, Type, str]] = [
    (UserModel, UserCreate, User, "/users/")
]

# Function to create route objects (CRUD routers)
def create_route_objects(models_and_schemas: List[Tuple[Type, Type, Type, str]]):
    routers = []
    for model, create_schema, read_schema, prefix in models_and_schemas:
        router = SQLAlchemyCRUDRouter(
            schema=read_schema,
            create_schema=create_schema,
            db_model=model,
            db=get_db,
            prefix=prefix
        )
        routers.append(router)
    return routers

# Function to attach a list of routers to the FastAPI app
def attach_list_of_routers(app: FastAPI, routers: List):
    for router in routers:
        app.include_router(router)

# Create routers and attach them to the app
routers = create_route_objects(models_and_schemas)
attach_list_of_routers(app, routers)

################################################################################


##############################create_routers##################################################

# # Define a list of models and their corresponding schemas
# models_and_schemas = [
#     (UserModel, UserCreate, User,"/users/")
# ]

# # Function to create routers for all models
# def create_routers(models_and_schemas):
#     routers = []
#     for model, create_schema, read_schema,prefix in models_and_schemas:
#         router = SQLAlchemyCRUDRouter(
#             schema=read_schema,
#             create_schema=create_schema,
#             db_model=model,
#             db=get_db,
#             prefix=prefix
#         )
#         routers.append(router)
#     return routers

# # Attach all routers to the FastAPI app
# for router in create_routers(models_and_schemas):
#     app.include_router(router)
################################################################################


##############################sqlalchemy_router##################################################

# # Create CRUD router for SQLAlchemy
# sqlalchemy_router = SQLAlchemyCRUDRouter(
#     schema=User,
#     create_schema=UserCreate,
#     update_schema=UserUpdate,     
#     db_model=UserModel,
#     db=get_db,
#     prefix="/users/"
# )

# # Create Memory CRUD router
# memory_router = MemoryCRUDRouter(
#     schema=User,
#     create_schema=UserCreate,  
#     update_schema=UserUpdate,  
#     prefix="/memory-users/"
# )

# # Include both routers in the FastAPI app
# app.include_router(sqlalchemy_router)
# app.include_router(memory_router)


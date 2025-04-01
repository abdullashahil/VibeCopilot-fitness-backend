from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import employees, trainers
from app.db.mongodb import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(trainers.router, prefix="/api/trainers", tags=["Trainers"])

@app.get("/")
async def root():
    return {"message": "Helloo, Fitness Appointment API http://localhost:8000/docs"}
from app.routes.tour_router import router as tour_router
from dotenv import load_dotenv
from fastapi import FastAPI
from mongoengine import connect
import os

load_dotenv()

DB = os.environ.get("DB_HOST")
connect(db="bhoboghure", host=DB)

app = FastAPI()

app.include_router(tour_router, prefix="/api/v1/tours", tags=["Tour"])

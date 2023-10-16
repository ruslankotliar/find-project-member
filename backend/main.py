import certifi
import pymongo.errors
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv


import os

from routes import (
    invite,
    projects,
    achievements,
    feedback,
    resume,
    search,
    subscription,
    teammate,
    verify,
)
from routes import user
from services.pdf import save_pdf

ca = certifi.where()

load_dotenv()
mongo_password = os.environ.get("MONGO_PASSWORD", None) or os.getenv(
    "MONGO_PASSWORD", None
)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(invite.router)
app.include_router(save_pdf.router)
app.include_router(projects.router)
app.include_router(achievements.router)
app.include_router(feedback.router)
app.include_router(resume.router)
app.include_router(search.router)
app.include_router(subscription.router)
app.include_router(teammate.router)
app.include_router(verify.router)


@app.on_event("startup")
def startup_db_client():
    try:
        print(mongo_password)
        app.mongodb_client = MongoClient(
            f"mongodb+srv://ruslankot101:{mongo_password}@cluster0.b6bendw.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=ca,
        )
        app.database = app.mongodb_client.pm_db
        try:
            app.database.create_collection("users")
        except pymongo.errors.CollectionInvalid:
            pass
        try:
            app.database.create_collection("projects")
        except pymongo.errors.CollectionInvalid:
            pass

        try:
            app.database.create_collection("achievements")
        except pymongo.errors.CollectionInvalid:
            pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/health")
def health():
    return {"status": "ok"}

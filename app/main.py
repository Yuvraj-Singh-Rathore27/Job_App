from fastapi import FastAPI
from app.db import Base, engine, test_connection
from app.models import user
from app.api.auth.views import router as auth_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Check DB
test_connection()

# REGISTER AUTH ROUTES HERE
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Backend running!"}

@app.get("/")
def health():
    return {"status": "ok"}


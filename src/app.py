# app/main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
# import settings
from backend.config.config import settings

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
# add routes
from backend.routes import login, register
app.include_router(login.router, prefix="/api/auth")
app.include_router(register.router, prefix="/api/auth")

# Simple health check route
@app.get("/")
def root():
    return {"message": "Welcome to Thrive Africa Backend"}

@app.get("/api/auth")
def auth_root():
    return {"message": "Auth endpoint"}
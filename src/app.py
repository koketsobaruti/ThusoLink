# app/main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
# import settings
from backend.config.config import settings

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
# add routes
from backend.routes import business, login, register, booking
app.include_router(login.router, prefix="/api/auth/logins")
app.include_router(register.router, prefix="/api/auth/registrations")
app.include_router(business.router, prefix="/api/business")
# app.include_router(booking.router, prefix="/api/bookings")

# Simple health check route
@app.get("/")
def root():
    return {"message": "Welcome to Thrive Africa Backend"}

@app.get("/api/auth")
def auth_root():
    return {"message": "Auth endpoint"}

# app/main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
# import settings from config folder in backend folder
# from backend.config.config import settings
from .backend.config.config import settings
app = FastAPI()
# Add CORS
origins = [
    "http://localhost:3000",  # React/Lovable frontend URL
    "http://127.0.0.1:3000",  # Optional alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)
# add routes
from .backend.routes import business, login, register, booking, services
app.include_router(login.router, prefix="/api/auth/logins")
app.include_router(register.router, prefix="/api/auth/registrations")
app.include_router(business.router, prefix="/api/business")
app.include_router(services.router, prefix="/api/services")
# app.include_router(booking.router, prefix="/api/bookings")

# Simple health check route
@app.get("/")
def root():
    return {"message": "Welcome to Thrive Africa Backend"}

@app.get("/api/auth")
def auth_root():
    return {"message": "Auth endpoint"}

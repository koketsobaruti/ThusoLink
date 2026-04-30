# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from .backend.config.config import Settings
# import settings from config folder in backend folder
# from backend.config.config import settings
# # import logger utils
from .backend.utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Main App")
# from .backend.tasks.scheduler import start_scheduler, shutdown_scheduler

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Lifespan events for startup and shutdown
#     """
#     # Startup
#     logger.info("🚀 Starting application...")
#     start_scheduler()  # ✅ Start background scheduler
#     yield
#     # Shutdown
#     logger.info("👋 Shutting down application...")
#     shutdown_scheduler()  # ✅ Stop scheduler gracefully
settings = Settings()  # Load settings at module level
from .backend.config.config import settings
app = FastAPI(
    title="ThusoLink Booking API",
    version="1.0.0" # ✅ Use lifespan context manager
)


# Add CORS
origins = [
    # "http://localhost:3000",  # React/Lovable frontend URL
    # "http://127.0.0.1:3000",  # Optional alternative
    "https://v0-create-next-app-beta.vercel.app/"
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
from .backend.routes import business, login, register, admin, services, booking
app.include_router(login.router, prefix="/api/auth/logins")
app.include_router(register.router, prefix="/api/auth/registrations")
app.include_router(business.router, prefix="/api/business")
app.include_router(services.router, prefix="/api/services")
app.include_router(booking.router, prefix="/api/bookings")

# Simple health check route
@app.get("/")
def root():
    return {"message": "Welcome to Thrive Africa Backend"}

@app.get("/api/auth")
def auth_root():
    return {"message": "Auth endpoint"}

@app.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Forbidden", status_code=403)
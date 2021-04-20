from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import root, settings
from controller.camera import Camera

# App initialization
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(root.router)
app.include_router(settings.router)

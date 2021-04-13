from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.camera import router as CameraRouter
from routes.root import router as RootRouter
from controller.camera import Camera

# App initialization
app = FastAPI()

# Camera initialization
can = Camera()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(RootRouter)
app.include_router(CameraRouter)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics # Import the exporter
from routes import root
from controller.camera import Camera
import os


# App initialization
# root_path probably not necessary anymore
app = FastAPI(root_path=os.getenv('ROOT_PATH', None))

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metriccs exporter
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

# Routes
app.include_router(root.router)

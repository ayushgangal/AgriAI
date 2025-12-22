from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Import your application's routers
from app.routers import queries, weather, crops, finance, voice, auth, crop_api

# --- Application Initialization ---
app = FastAPI(
    title="AgriAI Advisor API",
    description="API for the AgriAI agricultural advisor application.",
    version="1.0.0",
)

# --- CORS Middleware Configuration ---
# This is the crucial part that allows your frontend to connect.
origins = [
    "http://localhost",
    "http://localhost:3000",  # Default for Create React App
    "http://localhost:5173",  # Default for Vite (sometimes used for Vue/React)
    "http://localhost:4200",  # Default for Angular
    "http://localhost:8080",  # Common alternative dev port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- Include Routers ---
# This adds all the endpoints from your router files to the main application.
app.include_router(queries.router, prefix=settings.API_V1_STR, tags=["AI Queries"])
app.include_router(weather.router, prefix=settings.API_V1_STR, tags=["Weather"])
app.include_router(crops.router, prefix=settings.API_V1_STR, tags=["Crops"])
app.include_router(finance.router, prefix=settings.API_V1_STR, tags=["Finance"])
app.include_router(voice.router, prefix=settings.API_V1_STR, tags=["Voice Service"])
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
app.include_router(crop_api.router, tags=["Crop API"])

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the AgriAI Advisor API!"}

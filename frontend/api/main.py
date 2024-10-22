from fastapi import FastAPI
from api.endpoints import agent, orchestrators, metric
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI instance
app = FastAPI(title="Distributed AI System API", version="1.0.0")

# Middleware for CORS to allow frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router for each endpoint
app.include_router(agents.router, prefix="/agent", tags=["Agent"])
app.include_router(orchestrator.router, prefix="/orchestrators", tags=["Orchestrators"])
app.include_router(metrics.router, prefix="/metric", tags=["Metric"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Distributed AI System API"}
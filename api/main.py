from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
import uvicorn

from .config import settings
from .routers import query, tables, health, admin
from .services.pneuma_service import PneumaService
from .services.session_service import SessionService
from .middleware.logging import setup_logging

# Setup structured logging
setup_logging()
logger = structlog.get_logger()

# Global services
pneuma_service = None
session_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global pneuma_service, session_service

    # Startup
    logger.info("Starting Pneuma API server...")

    try:
        # Initialize services
        pneuma_service = PneumaService()
        await pneuma_service.initialize()

        session_service = SessionService()
        await session_service.initialize()

        logger.info("All services initialized successfully")

    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise

    yield

    # Shutdown
    logger.info("Shutting down Pneuma API server...")
    if session_service:
        await session_service.cleanup()


# Create FastAPI app
app = FastAPI(
    title="Pneuma Data Discovery API",
    description="REST API for Pneuma data discovery system with OpenWebUI integration",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(tables.router, prefix="/api/v1", tags=["tables"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# Dependency to get services
def get_pneuma_service() -> PneumaService:
    if pneuma_service is None:
        raise HTTPException(status_code=503, detail="Pneuma service not initialized")
    return pneuma_service


def get_session_service() -> SessionService:
    if session_service is None:
        raise HTTPException(status_code=503, detail="Session service not initialized")
    return session_service


# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "Pneuma Data Discovery API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


def main():
    """Entry point for running the server"""
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.api_log_level,
    )


if __name__ == "__main__":
    main()

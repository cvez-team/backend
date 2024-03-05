import os
import uvicorn
from apps.utils.create_app import create_app
from apps.routes.uploads_route import router as uploads_router

# Create FastAPI app instance
app = create_app()


# Add routes
app.include_router(uploads_router, prefix="/api")


# Launch FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 7860))

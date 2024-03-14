import os
import uvicorn
from apps.utils.create_app import create_app
from apps.routes.new import router as uploads_router
from apps.routes.match import router as match_router
from apps.routes.get import router as get_router
from apps.routes.update import router as update_router
from apps.routes.delete import router as delete_router
from dotenv import load_dotenv


# Load environment variables from the `.env` file
load_dotenv()
# Create FastAPI app instance
app = create_app()


# Add routes
app.include_router(uploads_router, prefix="/api")
app.include_router(match_router, prefix="/api")
app.include_router(get_router, prefix="/api")
app.include_router(update_router, prefix="/api")
app.include_router(delete_router, prefix="/api")


# Launch FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 7860))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 7860))

import os
import uvicorn
from apps.utils.create_app import create_app
from apps.routes.new import router as uploads_router
from dotenv import load_dotenv


# Load environment variables from the `.env` file
load_dotenv()
# Create FastAPI app instance
app = create_app()


# Add routes
app.include_router(uploads_router, prefix="/api")


# Launch FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 7860))

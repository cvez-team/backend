import os
import uvicorn
from apis import api_v1_router
from apis.create_app import create_app
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the `.env` file
load_dotenv(find_dotenv())
# Create FastAPI app instance
app = create_app()


# Add routes
app.include_router(api_v1_router, prefix="/api")


# Launch FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 7860))

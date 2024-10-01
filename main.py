import os
import uvicorn
from apis.dotenv import load_enviroment_variables
from apis.create_app import create_app
from apis import api_v1_router

# Load environment variables
load_enviroment_variables()

# Create FastAPI app instance
app = create_app()

# Add routes to the app
app.include_router(api_v1_router, prefix="/api")

# Launch FastAPI app by `python main.py`
if __name__ == "__main__":
    # Run app in Development option
    uvicorn.run(app, host="127.0.0.1", port=int(
        os.environ.get("PORT", 7860)), log_level="debug")

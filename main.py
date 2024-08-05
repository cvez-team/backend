import os
import uvicorn
from apis.create_app import create_app
from apis import api_v1_router

# Create FastAPI app instance
app = create_app()

# Add routes to the app
app.include_router(api_v1_router, prefix="/api")

# Launch FastAPI app by `python main.py`
if __name__ == "__main__":
    # Load dotenv file in Development option
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(raise_error_if_not_found=True))
    # Run app in Development option
    uvicorn.run(app, host="127.0.0.1", port=os.environ.get("PORT", 7860))

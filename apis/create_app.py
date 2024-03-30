from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .v1.configs.swagger_config import swagger_config


# Define create_app function.
# Avoid circular import by using this function
# to create FastAPI app instance.
def create_app():
    app = FastAPI(**swagger_config)

    # CORs handling
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

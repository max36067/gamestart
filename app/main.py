from fastapi import FastAPI
from app.api.v1 import router as api_v1_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_v1_router)
    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "Hello World"}

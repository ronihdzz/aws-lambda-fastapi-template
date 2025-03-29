from fastapi import FastAPI
from mangum import Mangum
from fastapi.openapi.utils import get_openapi
import os
from api.routers import api_v1_router
from api.endpoints import index_router

app = FastAPI(root_path=os.getenv("ROOT_PATH",""))


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Books API",
        version="1.0.0",
        description="A sample API for books",
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"  # 👈 force compatible version
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(api_v1_router)
app.include_router(index_router)

handler = Mangum(app)

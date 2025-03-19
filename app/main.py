from fake_data.db import lifespan
from fastapi import FastAPI

# from routers.connector_sources import router as connector_sources_router
# from routers.connectors import router as connector_router
from routers.connectors_and_sources import router as connectors_and_sources_router

app = FastAPI(lifespan=lifespan)
app.openapi_version = "3.0.1"

# Include the router in the app
# app.include_router(connector_router)
# app.include_router(connector_sources_router)
app.include_router(connectors_and_sources_router)

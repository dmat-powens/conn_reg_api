from fake_data.db import lifespan
from fastapi import FastAPI
from routers.connector_sources import router as connector_sources_router
from routers.connectors import router as connector_router

app = FastAPI(lifespan=lifespan)

# Include the router in the app
app.include_router(connector_router)
app.include_router(connector_sources_router)

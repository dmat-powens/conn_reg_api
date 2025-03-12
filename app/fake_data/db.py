import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from models.connector_sources import ConnectorSource
from models.connectors import Connector

# DB placeholders for model objects
CONNECTORS_DB = []
CONNECTOR_SOURCES_DB = []

# other way to define the data
# CONNECTOR_SOURCES_DB = [
#     ConnectorSource(
#         uuid_connector=UUID("123e4567-e89b-12d3-a456-426614174000"),
#         name="Source 1",
#         status="active",
#     ),
#     ConnectorSource(
#         uuid_connector=UUID("123e4567-e89b-12d3-a456-426614174001"),
#         name="Source 2",
#         status="inactive",
#     ),
# ]


# Load data on application startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    connectors_file_path = Path(__file__).parent / "connectors.json"
    with connectors_file_path.open() as f:
        fake_connectors_data = json.load(f)

    for connector in fake_connectors_data:
        CONNECTORS_DB.append(Connector.parse_obj(connector))
    print("\n\n\t\t>>>>>> Connectors data loaded successfully!\n\n")

    connector_sources_file_path = Path(__file__).parent / "connector_sources.json"
    with connector_sources_file_path.open() as f:
        fake_connector_sources_data = json.load(f)

    for source in fake_connector_sources_data:
        CONNECTOR_SOURCES_DB.append(ConnectorSource.parse_obj(source))
    print("\n\n\t\t>>>>>> Connector sources data loaded successfully!\n\n")

    yield

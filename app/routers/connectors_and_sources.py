from uuid import UUID

from fake_data.db import CONNECTORS_AND_SOURCES_DB
from fastapi import APIRouter, HTTPException
from models.connectors_and_sources import (
    ConnectorAndSources,
    ConnectorsAndSourcesList,
    ConnectorsAndSourcesUpdate,
    ConnectorSource,
)

router = APIRouter(prefix="/connectors", tags=["connectors"])

@router.get("/{uuid_connector}", response_model=ConnectorsAndSourcesList)
def retrieve_connector_sources(uuid_connector: UUID) -> ConnectorsAndSourcesList:
    filtered_sources = [
        source for source in CONNECTORS_AND_SOURCES_DB if source.uuid == uuid_connector
    ]
    if not filtered_sources:
        raise HTTPException(
            status_code=404,
            detail="No connector sources found for the given connector UUID",
        )
    return ConnectorsAndSourcesList(sources=filtered_sources)


@router.get("", response_model=ConnectorsAndSourcesList)
def retrieve_connectors_and_sources(uuid_connector: UUID | None = None) -> ConnectorsAndSourcesList:
    if uuid_connector:
        filtered_connectors = [
            connector for connector in CONNECTORS_AND_SOURCES_DB if connector.uuid == uuid_connector
        ]
        if not filtered_connectors:
            raise HTTPException(
                status_code=404,
                detail="No connectors found for the given connector UUID",
            )
        return ConnectorsAndSourcesList(connectors=filtered_connectors)
    return ConnectorsAndSourcesList(connectors=CONNECTORS_AND_SOURCES_DB)


@router.patch("", response_model=ConnectorsAndSourcesList)
def update_connectors_and_sources(
    connectors_update: ConnectorsAndSourcesUpdate,
) -> ConnectorsAndSourcesList:
    updated_connectors = []
    for connector_update in connectors_update.connectors:
        existing_connector = get_connector_by_uuid(connector_update.uuid)
        for source_update in connector_update.sources:
            existing_source = get_source_by_name(existing_connector, source_update.name)
            existing_source.available = source_update.available
        updated_connectors.append(existing_connector)
    return ConnectorsAndSourcesList(connectors=updated_connectors)


def get_connector_by_uuid(uuid: UUID) -> ConnectorAndSources:
    for connector in CONNECTORS_AND_SOURCES_DB:
        if connector.uuid == uuid:
            return connector
    raise HTTPException(status_code=404, detail="Connector not found")


def get_source_by_name(connector: ConnectorAndSources, name: str) -> ConnectorSource:
    for source in connector.sources:
        if source.name == name:
            return source
    raise HTTPException(status_code=404, detail="Source not found")


"""
Example body for patch request
{
  "connectors": [
    {
      "uuid": "123e4567-e89b-12d3-a456-426614174000",
      "sources": [
        {
          "name": "openapi",
          "available": false
        }
      ]
    },
    {
      "uuid": "123e4567-e89b-12d3-a456-426614174001",
      "sources": [
        {
          "name": "fallback",
          "available": true
        }
      ]
    }
  ]
}
"""

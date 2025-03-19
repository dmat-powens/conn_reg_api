from uuid import UUID

from fake_data.db import CONNECTOR_SOURCES_DB
from fastapi import APIRouter, HTTPException
from models.connector_sources import (
    ConnectorSource,
    ConnectorSourcesList,
    ConnectorSourcesUpdate,
)

router = APIRouter(prefix="/connectors", tags=["connector sources"])


@router.get("/{uuid_connector}/sources", response_model=ConnectorSourcesList)
def retrieve_connector_sources(uuid_connector: UUID) -> ConnectorSourcesList:
    filtered_sources = [
        source for source in CONNECTOR_SOURCES_DB if source.uuid_connector == uuid_connector
    ]
    if not filtered_sources:
        raise HTTPException(
            status_code=404,
            detail="No connector sources found for the given connector UUID",
        )
    return ConnectorSourcesList(sources=filtered_sources)


@router.patch("/{uuid_connector}/sources", response_model=ConnectorSourcesList)
def update_connector_sources(
    uuid_connector: UUID, connector_sources_update: ConnectorSourcesUpdate
) -> ConnectorSourcesList:
    updated_sources = []
    for source_update in connector_sources_update.sources:
        existing_source = get_connector_source_by_uuid_connector_and_name(
            uuid_connector, source_update.name
        )
        # if source_update.priority is not None:
        #     existing_source.priority = source_update.priority
        if source_update.unavailable is not None:
            existing_source.unavailable = source_update.unavailable
        # if source_update.unavailable_capabilities is not None:
        #     existing_source.unavailable_capabilities = source_update.unavailable_capabilities
        # if source_update.auth_mechanism is not None:
        #     existing_source.auth_mechanism = source_update.auth_mechanism
        # if source_update.sync_periodicity is not None:
        #     existing_source.sync_periodicity = source_update.sync_periodicity
        save_connector_source(existing_source)
        updated_sources.append(existing_source)
    return ConnectorSourcesList(sources=updated_sources)


def get_connector_source_by_uuid_connector_and_name(
    uuid_connector: UUID, name: str
) -> ConnectorSource:
    matching_sources = [
        source
        for source in CONNECTOR_SOURCES_DB
        if source.uuid_connector == uuid_connector and source.name == name
    ]
    if len(matching_sources) == 0:
        raise HTTPException(status_code=404, detail="Connector source not found")
    if len(matching_sources) > 1:
        raise HTTPException(
            status_code=400,
            detail="Multiple connector sources found with the same name",
        )
    return matching_sources[0]


def save_connector_source(updated_source: ConnectorSource):
    for i, source in enumerate(CONNECTOR_SOURCES_DB):
        if (
            source.uuid_connector == updated_source.uuid_connector
            and source.name == updated_source.name
        ):
            CONNECTOR_SOURCES_DB[i] = updated_source
            break

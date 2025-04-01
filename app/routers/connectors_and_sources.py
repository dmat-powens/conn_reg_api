from uuid import UUID

from fake_data.db import CONNECTORS_DB, SOURCES_DB
from fastapi import APIRouter, HTTPException, Query
from models.connectors_and_sources import (
    ConnectorAndSources,
    ConnectorsAndSourcesList,
    ConnectorsAndSourcesUpdate,
    ConnectorSource,
    TypeEnum,
)

router = APIRouter(prefix="/connectors", tags=["connectors"])

##
##? GET
##


@router.get("", response_model=ConnectorsAndSourcesList)
def retrieve_connectors(
    page: int = Query(
        1, ge=1, description="Page number for pagination. Must be greater than or equal to 1."
    ),
    limit: int = Query(
        3, ge=1, description="Number of connectors per page. Must be greater than or equal to 1."
    ),
    all: bool = Query(None, description="If True, returns all connectors without pagination."),
) -> ConnectorsAndSourcesList:
    """
    Retrieve a list of connectors and their associated sources.

    It supports pagination and an option to retrieve all connectors and sources at once.
    """
    connectors_dict = {connector.uuid: connector for connector in CONNECTORS_DB}
    sources_dict = {}

    for source in SOURCES_DB:
        if source.connector_uuid in connectors_dict:
            if source.connector_uuid not in sources_dict:
                sources_dict[source.connector_uuid] = []
            sources_dict[source.connector_uuid].append(source)

    connectors_and_sources = []
    for connector_uuid, connector in connectors_dict.items():
        connector_sources = sources_dict.get(connector_uuid, [])
        connectors_and_sources.append(
            ConnectorAndSources(uuid=connector.uuid, sources=connector_sources)
        )

    if all:
        return ConnectorsAndSourcesList(connectors=connectors_and_sources)

    start = (page - 1) * limit
    end = start + limit
    paginated_connectors = connectors_and_sources[start:end]

    return ConnectorsAndSourcesList(connectors=paginated_connectors)


@router.get("/{connector_uuid}", response_model=ConnectorAndSources)
def retrieve_connector(connector_uuid: UUID) -> ConnectorAndSources:
    connector = get_connector_by_uuid(connector_uuid)

    # Get all sources associated with this connector
    connector_sources = []
    for source in SOURCES_DB:
        if source.connector_uuid == connector_uuid:
            connector_sources.append(source)

    return ConnectorAndSources(uuid=connector.uuid, sources=connector_sources)


##
##? PUT
##


@router.put("/{connector_uuid}", response_model=ConnectorAndSources)
def create_or_update_connector(
    connector_uuid: UUID,
) -> ConnectorAndSources:
    """
    Create or update a connector (without sources).

    The connector UUID must exist in the external system.

    **DEMO ONLY**: This endpoint is currently disabled in production and is only available for demonstration purposes.
    """
    # Block the route from being used
    raise HTTPException(
        status_code=403,
        detail="This endpoint is currently only available for demonstration purposes and is not enabled in production.",
    )

    # The code below will never execute but shows the intended implementation

    try:
        # Try to get the existing connector
        existing_connector = get_connector_by_uuid(connector_uuid)
        return existing_connector
    except HTTPException:
        # Connector doesn't exist, create a new one
        new_connector = ConnectorAndSources(uuid=connector_uuid, sources=[])
        CONNECTORS_DB.append(new_connector)
        return new_connector


@router.put("/{connector_uuid}/sources", response_model=ConnectorAndSources)
def create_or_update_source(
    connector_uuid: UUID,
    source: ConnectorSource,
) -> ConnectorAndSources:
    """
    Create or update a source for a specific connector.

    The connector must already exist. If a source with the same type already exists,
    it will be updated; otherwise, a new source will be created.

    **DEMO ONLY**: This endpoint is currently disabled in production and is only available for demonstration purposes.
    """
    # Block the route from being used
    # 403 Forbidden: This would suggest that the server understands the request
    # but refuses to authorize it due to permissions or policy restrictions.
    raise HTTPException(
        status_code=403,
        detail="This endpoint is currently only available for demonstration purposes and is not enabled in production.",
    )

    # The code below will never execute but shows the intended implementation

    # Find the connector (will raise 404 if not found)
    existing_connector = get_connector_by_uuid(connector_uuid)

    # Ensure the source has the correct connector_uuid
    source.connector_uuid = connector_uuid

    # Check if source already exists
    for i, existing_source in enumerate(SOURCES_DB):
        if existing_source.connector_uuid == connector_uuid and existing_source.type == source.type:
            # Update the existing source
            SOURCES_DB[i] = source
            break
    else:
        # Source doesn't exist, add it
        SOURCES_DB.append(source)

    # Get all sources associated with this connector to return
    connector_sources = []
    for db_source in SOURCES_DB:
        if db_source.connector_uuid == connector_uuid:
            connector_sources.append(db_source)

    return ConnectorAndSources(uuid=connector_uuid, sources=connector_sources)


##
##? PATCH
##


@router.patch("/{connector_uuid}", response_model=ConnectorAndSources)
def update_connector(
    connector_uuid: UUID,
) -> ConnectorAndSources:
    """
    Partial update of a connector's fields.

    This operation will not create new resources - the connector must already exist.

    **DEMO ONLY**: This functionality is planned for future implementation.
    """
    # Find the connector (will raise 404 if not found)
    existing_connector = get_connector_by_uuid(connector_uuid)

    # Future implementation for updating connector fields
    # 501 Not Implemented: This indicates that the server does not support the functionality requiredto fulfill the
    # request. It's specifically designed for situations where a feature is planned but not yet implemented.
    raise HTTPException(
        status_code=501, detail="Updating connector fields is not implemented in this version"
    )

    # This code will never execute but shows the intended future implementation
    # return ConnectorAndSources(uuid=connector_uuid, sources=existing_connector.sources)


@router.patch("/{connector_uuid}/sources/{source_type}", response_model=ConnectorAndSources)
def update_source(
    connector_uuid: UUID,
    source_type: str,
    available: bool = None,
) -> ConnectorAndSources:
    """
    Partial update of a specific source of a connector.

    Both the connector and source must already exist. This operation will not create new resources.
    Currently, only the 'available' field can be updated.

    source_type must be one of: 'openapi', 'directaccess', 'fallback'.
    """
    # Find the connector (will raise 404 if not found)
    existing_connector = get_connector_by_uuid(connector_uuid)

    # Find the source (will raise 404 if not found)
    source = get_source_by_type(connector_uuid, source_type)

    # Update the 'available' field if provided
    if available is not None:
        source.available = available
    else:
        raise HTTPException(
            status_code=400,
            detail="The 'available' parameter must be provided when updating a source",
        )

    # Get all sources associated with this connector to return
    connector_sources = []
    for db_source in SOURCES_DB:
        if db_source.connector_uuid == connector_uuid:
            connector_sources.append(db_source)

    return ConnectorAndSources(uuid=connector_uuid, sources=connector_sources)


##
##? DELETE
##


@router.delete("/{connector_uuid}", response_model=ConnectorAndSources)
def delete_connector(
    connector_uuid: UUID,
) -> ConnectorAndSources:
    """
    Delete a connector and all its associated sources.

    **DEMO ONLY**: This endpoint is currently disabled in production and is only available for demonstration purposes.
    """
    # Block the route from being used
    raise HTTPException(
        status_code=403,
        detail="This endpoint is currently only available for demonstration purposes and is not enabled in production.",
    )

    # The code below will never execute but shows the intended implementation
    existing_connector = get_connector_by_uuid(connector_uuid)

    # Store connector before deletion for the response
    deleted_connector = ConnectorAndSources(uuid=existing_connector.uuid, sources=[])

    # First delete all sources associated with this connector
    for source in list(SOURCES_DB):  # Create a copy of the list to safely modify during iteration
        if source.connector_uuid == connector_uuid:
            deleted_connector.sources.append(source)
            SOURCES_DB.remove(source)

    # Then delete the connector itself
    CONNECTORS_DB.remove(existing_connector)

    # Return the deleted connector and its sources for confirmation
    return deleted_connector


@router.delete("/{connector_uuid}/sources/{source_type}", response_model=ConnectorAndSources)
def delete_source(
    connector_uuid: UUID,
    source_type: str,
) -> ConnectorAndSources:
    """
    Delete a specific source from a connector.

    Both the connector and the source must exist. The source is identified by its type.

    **DEMO ONLY**: This endpoint is currently disabled in production and is only available for demonstration purposes.
    """
    # Block the route from being used
    raise HTTPException(
        status_code=403,
        detail="This endpoint is currently only available for demonstration purposes and is not enabled in production.",
    )

    # The code below will never execute but shows the intended implementation

    # Find the connector (will raise 404 if not found)
    connector = get_connector_by_uuid(connector_uuid)

    # Find and remove the specified source
    deleted_source = None
    for i, source in enumerate(SOURCES_DB):
        if source.connector_uuid == connector_uuid and source.type == source_type:
            deleted_source = source
            SOURCES_DB.remove(source)
            break

    if not deleted_source:
        raise HTTPException(
            status_code=404,
            detail=f"Source with type '{source_type}' not found for connector '{connector_uuid}'",
        )

    # Get the updated list of sources for this connector to return
    remaining_sources = []
    for source in SOURCES_DB:
        if source.connector_uuid == connector_uuid:
            remaining_sources.append(source)

    return ConnectorAndSources(uuid=connector_uuid, sources=remaining_sources)


@router.delete("/{connector_uuid}", response_model=ConnectorsAndSourcesList)
def delete_connector_and_or_source(
    connector_uuid: UUID,
    source_type: str = None,
) -> ConnectorsAndSourcesList:
    """
    Delete a connector or a specific source from a connector.

    - If source_type is provided, only that source will be deleted
    - If source_type is not provided, the entire connector and all its sources will be deleted

    **DEMO ONLY**: This endpoint is currently disabled in production and is only available for demonstration purposes.
    """
    # Block the route from being used
    raise HTTPException(
        status_code=403,
        detail="This endpoint is currently only available for demonstration purposes and is not enabled in production.",
    )

    # The code below will never execute but shows the intended implementation
    existing_connector = get_connector_by_uuid(connector_uuid)

    # If source_type is provided, delete only that source
    if source_type:
        # Find and remove the specified source
        for i, source in enumerate(existing_connector.sources):
            if source.type == source_type:
                existing_connector.sources.pop(i)
                break
        else:
            raise HTTPException(
                status_code=404, detail=f"Source with type '{source_type}' not found"
            )

        return ConnectorsAndSourcesList(connectors=[existing_connector])

    # Otherwise, delete the entire connector
    else:
        # Remove the connector from the database (would happen if enabled)
        CONNECTORS_AND_SOURCES_DB.remove(existing_connector)

        # Return the deleted connector for confirmation
        return ConnectorsAndSourcesList(connectors=[existing_connector])


##
## Helpers
##


def get_connector_by_uuid(uuid: UUID) -> ConnectorAndSources:
    for connector in CONNECTORS_DB:
        if connector.uuid == uuid:
            return connector
    raise HTTPException(status_code=404, detail="Connector not found")


def get_source_by_type(connector_uuid: UUID, type: str) -> ConnectorSource:
    for source in SOURCES_DB:
        if source.connector_uuid == connector_uuid and source.type == type:
            return source
    raise HTTPException(status_code=404, detail="Source not found")


"""
#! Do no patch patch on array of connectors and sources, or we would mix partial update and bulk update
@router.patch("", response_model=ConnectorsAndSourcesList)
def update_connectors_and_sources(
  connectors_update: ConnectorsAndSourcesUpdate,
) -> ConnectorsAndSourcesList:
  updated_connectors = []
  for connector_update in connectors_update.connectors:
    existing_connector = get_connector_by_uuid(connector_update.uuid)
    for source_update in connector_update.sources:
      existing_source = get_source_by_type(existing_connector, source_update.type)
      existing_source.available = source_update.available
    updated_connectors.append(existing_connector)
  return ConnectorsAndSourcesList(connectors=updated_connectors)
"""


'''
# Using PUT is more RESTful when the resources existence are checked in an external service (Backend DB)
# Single endpoint for both connector and source operations. Uses a query parameter to determine the operation scope.
# Preserves the RESTful nature of treating connectors as the primary resource
@router.put("/{connector_uuid}", response_model=ConnectorsAndSourcesList)
def create_connector_and_or_source(
    connector_uuid: UUID,
    source: ConnectorSource,
    source_type: str = None,
) -> ConnectorsAndSourcesList:
    """
    Create or update a connector, optionally focusing on a specific source.

    - If source_type is provided, only that source will be added
    - If source_type is not provided, the entire connector will be added

    The connector UUID and source type must exist in the external system.

    **DEMO ONLY**: This endpoint is currently disabled in production and is only available for demonstration purposes.
    """
    # Block the route from being used
    raise HTTPException(
        status_code=403,
        detail="This endpoint is currently only available for demonstration purposes and is not enabled in production.",
    )

    # The code below will never execute but shows the intended implementation

    # If source_type is specified, we're adding/updating just one source
    if source_type:
        # Verify that the source type in the query matches the one in the body
        if source_type != source.type:
            raise HTTPException(
                status_code=400,
                detail="Source type in the query parameter must match the source type in the request body",
            )

        try:
            existing_connector = get_connector_by_uuid(connector_uuid)

            # Check if source already exists
            for i, existing_source in enumerate(existing_connector.sources):
                if existing_source.type == source_type:
                    # Update the existing source
                    existing_connector.sources[i] = source
                    break
            else:
                # Source doesn't exist, add it
                existing_connector.sources.append(source)

        except HTTPException:
            # Connector doesn't exist, create it with the specified source
            new_connector = ConnectorAndSources(uuid=connector_uuid, sources=[source])
            CONNECTORS_AND_SOURCES_DB.append(new_connector)
            return ConnectorsAndSourcesList(connectors=[new_connector])

        return ConnectorsAndSourcesList(connectors=[existing_connector])

    # If no source_type is specified, we're creating/updating the entire connector
    else:
        # Normal connector creation/update logic
        # This would be similar to your existing create_or_update_connector function
        pass

    return ConnectorsAndSourcesList(connectors=[existing_connector])
'''

from uuid import UUID

from fake_data.db import CONNECTORS_DB
from fastapi import APIRouter, HTTPException
from models.connectors import Connector, ConnectorsList, ConnectorsUpdate

router = APIRouter(prefix="/connectors", tags=["connectors"])


@router.get("", response_model=ConnectorsList)
def retrieve_connectors() -> ConnectorsList:
    return ConnectorsList(connectors=CONNECTORS_DB)


@router.patch("", response_model=ConnectorsList)
def update_connectors(connectors_update: ConnectorsUpdate) -> ConnectorsList:
    updated_connectors = []
    for connector_update in connectors_update.connectors:
        existing_connector = get_connector_by_uuid(connector_update.uuid)
        if connector_update.months_to_fetch is not None:
            existing_connector.months_to_fetch = connector_update.months_to_fetch
        if connector_update.hidden is not None:
            existing_connector.hidden = connector_update.hidden
        save_connector(existing_connector)
        updated_connectors.append(existing_connector)
    return ConnectorsList(connectors=updated_connectors)


def get_connector_by_uuid(uuid: UUID) -> Connector:
    for connector in CONNECTORS_DB:
        if connector.uuid == uuid:
            return connector
    raise HTTPException(status_code=404, detail="Connector not found")


def save_connector(updated_connector: Connector):
    for i, connector in enumerate(CONNECTORS_DB):
        if connector.uuid == updated_connector.uuid:
            CONNECTORS_DB[i] = updated_connector
            break


"""
Data for patch sources request
123e4567-e89b-12d3-a456-426614174000
{
  "sources": [
  {
    "name": "openapi",
    # "priority": 1
  },
  {
    "name": "directaccess",
    "sync_periodicity": 1.15
  }
]
}
"""

from enum import Enum
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    root_validator,
)


class TypeEnum(str, Enum):
    OPENAPI = "openapi"
    FALLBACK = "fallback"
    DIRECTACCESS = "directaccess"


# class StatusEnum(str, Enum):
#     STABLE = "stable"
#     UNSTABLE = "unstable"
#     DOWN = "down"
#     UNKNOWN = "unknown"


# class Stability(BaseModel):
#     status: StatusEnum = Field(
#         StatusEnum.UNKNOWN,
#         title="Status",
#         description="The status of the connector",
#     )
#     # TODO: check nullability
#     last_update: str = Field(
#         ...,
#         title="Last update",
#         description="The date and time of the last update of the connector (format: YYYY-MM-DD HH:MM:SS)",
#         pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
#     )

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {
#                 "stability": {
#                     "status": "stable",
#                     "last_update": "2025-03-10 14:00:25",
#                 }
#             }
#         }
#     )


class ConnectorSource(BaseModel):
    connector_uuid: UUID = Field(
        ...,
        title="Connector UUID",
        description="The unique identifier for the connector",
        exclude=True,
    )
    uuid: UUID = Field(
        ...,
        title="Connector source UUID",
        description="The unique identifier for the connector source",
    )
    type: TypeEnum = Field(
        ...,
        title="Connector source type",
        description="The type of the connector source",
    )
    available: bool = Field(
        ...,
        title="Available",
        description="Whether the source is set as available or not",
    )
    # stability: Stability = Field(
    #     ...,
    #     title="Connector stability",
    #     description="The stability of the connector, compounded to the worst stability of the enabled connector sources.",
    # )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "connector_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "uuid": "eb4bbb24-0ef2-11f0-ae6f-429fb861f004",
                "type": "openapi",
                "available": False,
                # "stability": {"status": "stable", "last_update": "2025-03-10 14:00:25"},
            }
        }
    )


class ConnectorAndSources(BaseModel):
    uuid: UUID = Field(
        ...,
        title="Connector UUID",
        description="The unique identifier for the connector",
    )
    sources: list[ConnectorSource] = Field(
        ...,
        title="Connector sources",
        description="The list of sources for the connector",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "sources": [
                    {
                        "uuid": "eb4bbb24-0ef2-11f0-ae6f-429fb861f004",
                        "type": "openapi",
                        "available": True,
                        # "stability": {
                        #     "status": "stable",
                        #     "last_update": "2025-03-10 14:00:25",
                        # },
                    },
                    {
                        "uuid": "eb4bbb24-0ef2-11f0-ae6f-429fb861f005",
                        "type": "directaccess",
                        "available": True,
                        # "stability": {
                        #     "status": "unstable",
                        #     "last_update": "2025-03-08 11:00:25",
                        # },
                    },
                ],
            }
        }
    )


class ConnectorsAndSourcesList(BaseModel):
    connectors: list[ConnectorAndSources] = Field(
        ..., title="Connectors", description="The list of connectors and their sources"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "connectors": [
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174000",
                        "sources": [
                            {
                                "uuid": "eb4bbb24-0ef2-11f0-ae6f-429fb861f004",
                                "type": "openapi",
                                "available": True,
                                # "stability": {
                                #     "status": "stable",
                                #     "last_update": "2025-03-10 14:00:25",
                                # },
                            },
                            {
                                "uuid": "eb4bbb24-0ef2-11f0-ae6f-429fb861f003",
                                "type": "directaccess",
                                "available": True,
                                # "stability": {
                                #     "status": "unstable",
                                #     "last_update": "2025-03-08 11:00:25",
                                # },
                            },
                        ],
                    },
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174001",
                        "sources": [
                            {
                                "uuid": "eb4bbb24-0ef2-11f0-ae6f-429fb861f004",
                                "type": "openapi",
                                "available": False,
                                # "stability": {
                                #     "status": "stable",
                                #     "last_update": "2025-04-10 18:37:39",
                                # },
                            },
                            {
                                "uuid": "eb4bbb24-0ef2-11f0-ae6f-429fb861f002",
                                "type": "fallback",
                                "available": True,
                                # "stability": {
                                #     "status": "stable",
                                #     "last_update": "2025-03-24 12:39:53",
                                # },
                            },
                        ],
                    },
                ]
            }
        }
    )


class ConnectorSourceUpdate(BaseModel):
    type: TypeEnum = Field(
        ...,
        title="Connector source type",
        description="The type of the connector source",
    )
    uuid: UUID = Field(
        ...,
        title="Connector source UUID",
        description="The unique identifier for the connector source",
    )
    available: bool = Field(
        ...,
        title="Available",
        description="Whether the source is set as available or not",
    )

    @root_validator(pre=True)
    def check_available_field(cls, values):
        if "available" not in values:
            raise ValueError("The 'available' field must be provided")
        return values


class ConnectorAndSourcesUpdate(BaseModel):
    uuid: UUID = Field(
        ...,
        title="Connector UUID",
        description="The unique identifier for the connector",
    )
    sources: list[ConnectorSourceUpdate] = Field(
        ...,
        title="Connector sources update",
        description="The list of sources to update for the connector",
    )


class ConnectorsAndSourcesUpdate(BaseModel):
    connectors: list[ConnectorAndSourcesUpdate] = Field(
        ..., title="Connectors update", description="The connectors and their sources to update"
    )

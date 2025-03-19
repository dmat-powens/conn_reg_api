from datetime import datetime
from enum import Enum
from uuid import UUID

from dateutil.relativedelta import relativedelta
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    root_validator,
)


def example_date_strings():
    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute)
    then = now - relativedelta(hours=1)
    return (now.strftime("%Y-%m-%d %H:%M:%S"), then.strftime("%Y-%m-%d %H:%M:%S"))


class NameEnum(str, Enum):
    openapi = "openapi"
    fallback = "fallback"
    directaccess = "directaccess"


# class PriorityEnum(int, Enum):
#     high = 0
#     medium = 1
#     low = 2


class AuthMechanismEnum(str, Enum):
    webauth = "webauth"
    credentials = "credentials"


class StatusEnum(str, Enum):
    stable = "stable"
    unstable = "unstable"
    down = "down"


class Stability(BaseModel):
    status: StatusEnum = Field(
        ...,
        title="Status",
        description="The status of the connector",
    )
    last_update: str = Field(
        ...,
        title="Last update",
        description="The date and time of the last update of the connector (format: YYYY-MM-DD HH:MM:SS)",
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "stability": {
                    "status": "stable",
                    "last_update": "2025-03-10 14:00:25",
                }
            }
        }
    )


class ConnectorSource(BaseModel):
    # TODO: check nullity of all those fields
    uuid_connector: UUID = Field(
        ...,
        title="Connector UUID",
        description="The unique identifier for the connector",
    )
    name: NameEnum = Field(
        ...,
        title="Connector source name",
        description="The type name of the connector source",
    )
    # priority: PriorityEnum = Field(
    #     ...,
    #     title="Connector source priority",
    #     description="The priority of the connector source",
    # )
    # sync_periodicity: float | None = Field(
    #     ...,
    #     title="Connector source sync_periodicity",
    #     description="The interval in days between two synchronizations",
    #     ge=0.0,
    # )
    # auth_mechanism: AuthMechanismEnum | None = Field(
    #     ...,
    #     title="Connector source auth_mechanism",
    #     description="The authentication mechanism of the connector source",
    # )
    # TODO: better constraints this to a list of enum strings? (backend API sends strings representing lists)
    # TODO: At least check values are valid
    # unavailable_capabilities: str | None = Field(
    #     ...,
    #     title="Connector source unavailable_capabilities",
    #     description="The list of unavailable capabilities",
    # )
    # unavailable: str | None = Field(
    #     ...,
    #     title="Connector source unavailable",
    #     description="The date when the source was made unavailable if any",
    #     pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
    # )
    unavailable: bool = Field(
        ...,
        title="Unavailable",
        description="Whether the source is set as unavailable",
    )
    # TODO: check nullity
    stability: Stability = Field(
        ...,
        title="Connector stability",
        description="The stability of the connector, compounded to the worst stability of the enabled connector sources.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "uuid_connector": "123e4567-e89b-12d3-a456-426614174000",
                "name": "openapi",
                # "priority": 0,
                # "sync_periodicity": None,
                # "auth_mechanism": "webauth",
                # "unavailable_capabilities": "transfer",
                # "unavailable": "2024-07-20 11:05:45",
                "unavailable": False,
                "stability": {"status": "stable", "last_update": "2025-03-10 14:00:25"},
            }
        }
    )


class ConnectorSourceUpdate(BaseModel):
    name: NameEnum = Field(
        ...,
        title="Connector source name",
        description="The type name of the connector source",
    )
    # priority: PriorityEnum | None = Field(
    #     None,
    #     title="Priority",
    #     description="The priority to be set for the connector source",
    # )
    # sync_periodicity: float | None = Field(
    #     None,
    #     title="Synchronization Periodicity",
    #     description="The periodicity of synchronization to be set for the connector source",
    # )
    # auth_mechanism: AuthMechanismEnum | None = Field(
    #     None,
    #     title="Authentication Mechanism",
    #     description="The authentication mechanism to be set for the connector source",
    # )
    # unavailable_capabilities: str | None = Field(
    #     None,
    #     title="Unavailable Capabilities",
    #     description="The list of capabilities that needs to be set unavailable, if any",
    # )
    # TODO: allow 0/1 and false/true to be valid values and make the transformation into a date string if true/1 submitted
    # unavailable: str | None = Field(
    #     None,
    #     title="Unavailable",
    #     description="The date when the source is to be made unavailable if any",
    # )
    unavailable: bool = Field(
        ...,
        title="Unavailable",
        description="Whether the source is set as unavailable",
    )

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(
            values.get(field) is not None
            for field in [
                # "priority",
                "unavailable",
                # "unavailable_capabilities",
                # "auth_mechanism",
                # "sync_periodicity",
            ]
        ):
            raise ValueError(
                "No field was submitted for update"
                # "At least one field amongst 'unavailable', 'unavailable_capabilities', "
                # "'auth_mechanism', or 'sync_periodicity' must be provided",
            )
        return values


class ConnectorSourcesUpdate(BaseModel):
    sources: list[ConnectorSourceUpdate] = Field(
        ...,
        title="Connector sources update",
        description="The connector sources to update",
    )


class ConnectorSourcesList(BaseModel):
    sources: list[ConnectorSource] = Field(
        ...,
        title="Connector sources",
        description="The list of sources for the connector",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sources": [
                    {
                        "uuid_connector": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "openapi",
                        # "priority": 0,
                        # "sync_periodicity": None,
                        # "auth_mechanism": "webauth",
                        # "unavailable_capabilities": "transfer",
                        "unavailable": "2024-07-20 11:05:45",
                        "unavailable": False,
                        "stability": {
                            "status": "stable",
                            "last_update": "2025-03-10 14:00:25",
                        },
                    },
                    {
                        "uuid_connector": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "directaccess",
                        # "priority": 2,
                        # "sync_periodicity": 30,
                        # "auth_mechanism": "credentials",
                        # "unavailable_capabilities": "bank,profile",
                        # "unavailable": None,
                        "unavailable": True,
                        "stability": {
                            "status": "unstable",
                            "last_update": "2025-03-08 11:00:25",
                        },
                    },
                ]
            }
        }
    )

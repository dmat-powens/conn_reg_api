from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    root_validator,
)


class Connector(BaseModel):
    uuid: UUID = Field(
        ...,
        title="Connector UUID",
        description="The unique identifier for the connector",
    )
    # hidden: bool = Field(
    #     ...,
    #     title="Connector hidden property",
    #     description="Whether the connector is hidden or not",
    # )
    # Can be = 0 in clients API, but not at bi_connector level, which means trying to get the maximum months possible.
    # In ConReg API, it is not possible to set months_to_fetch = 0.
    # TODO: check nullity
    # months_to_fetch: PositiveInt | None = Field(
    #     ...,
    #     title="Connector months_to_fetch value",
    #     description="Number of months of history retrieved during synchronization",
    #     le=24,
    # )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                # "hidden": False,
                # "months_to_fetch": 0,
            }
        }
    )


class ConnectorUpdate(BaseModel):
    uuid: UUID = Field(
        ...,
        title="Connector UUID",
        description="The unique identifier for the connector",
    )
    months_to_fetch: PositiveInt | None = Field(
        None,
        title="Connector months_to_fetch value",
        le=24,
        description="Number of months of history retrieved during synchronization",
    )
    hidden: bool | None = Field(
        None,
        title="Connector hidden property",
        description="Whether the connector is hidden or not",
    )

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if values.get("months_to_fetch") is None and values.get("hidden") is None:
            raise ValueError(
                "At least one field amongst 'months_to_fetch' or 'hidden' must be provided"
            )
        return values


class ConnectorsUpdate(BaseModel):
    connectors: list[ConnectorUpdate] = Field(
        ..., title="Connectors update", description="The connectors to update"
    )


class ConnectorsList(BaseModel):
    connectors: list[Connector] = Field(
        ..., title="Connectors", description="The list of connectors"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "connectors": [
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174000",
                        # "hidden": False,
                        # "months_to_fetch": 24,
                    },
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174001",
                        # "months_to_fetch": 3,
                        # "hidden": True,
                    },
                ]
            }
        }
    )

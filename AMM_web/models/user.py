"""User models for admin management."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class UserSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int | None = None
    username: str | None = None
    email: str | None = None
    role: str | None = None
    is_active: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("is_active", "isActive"),
    )
    first_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("first_name", "firstName"),
    )
    last_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("last_name", "lastName"),
    )

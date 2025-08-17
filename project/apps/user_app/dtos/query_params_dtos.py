import pydantic


class UserQueryParamsDTO(pydantic.BaseModel):
    limit: int | None = None
    offset: int | None = None

    is_archived: bool | None = None

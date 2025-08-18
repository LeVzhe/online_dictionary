import datetime

import pydantic


class CurrentUserDTO(pydantic.BaseModel):
    id: int
    login: str
    email: str
    created_at: datetime.datetime


class ListUsersDTO(pydantic.BaseModel):
    id: int
    login: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UsersByIdDTO(pydantic.BaseModel):
    id: int
    login: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_archived: bool

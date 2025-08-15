import datetime

import pydantic


class CurrentUserDTO(pydantic.BaseModel):
    id: int
    login: str
    email: str
    created_at: datetime.datetime

import pydantic


class UserDTO(pydantic.BaseModel):
    login: str
    email: str

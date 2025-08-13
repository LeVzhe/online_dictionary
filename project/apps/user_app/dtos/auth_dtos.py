import pydantic


class UserDTO(pydantic.BaseModel):
    login: str
    email: str


class LoginUsingUsernamePasswordDto(pydantic.BaseModel):
    login: str
    password: str
    user_agent: str

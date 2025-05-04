from .configured_base_model import ConfiguredBaseModel


class GetCurrentUserResponse(ConfiguredBaseModel):

    id: int
    display_name: str
    email: str


class SignUpWithEmailAndPasswordRequest(ConfiguredBaseModel):

    display_name: str
    email: str
    password: str


class SignInWithEmailAndPasswordRequest(ConfiguredBaseModel):

    email: str
    password: str


class SignInWithEmailAndPasswordResponse(ConfiguredBaseModel):

    access_token: str

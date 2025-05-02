from pydantic import BaseModel


class SignUpWithEmailAndPasswordRequest(BaseModel):

    display_name: str
    email: str
    password: str


class SignInWithEmailAndPasswordRequest(BaseModel):

    email: str
    password: str


class SignInWithEmailAndPasswordResponse(BaseModel):

    access_token: str

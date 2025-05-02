from fastapi import APIRouter, HTTPException, Depends, status

from auth_demo_backend.application.services.auth_service import AuthService
from ..models import (
    SignInWithEmailAndPasswordRequest,
    SignInWithEmailAndPasswordResponse,
    SignUpWithEmailAndPasswordRequest,
)
from ..dependencies import get_auth_service

router = APIRouter(prefix="/auth")


@router.post(
    "/sign-up",
    summary="Sign Up With Email and Password",
    status_code=status.HTTP_201_CREATED,
)
def sign_up_with_email_and_password(
    request: SignUpWithEmailAndPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
):

    try:
        auth_service.sign_up_with_email_and_password(
            display_name=request.display_name,
            email=request.email,
            password=request.password,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.post(
    "/sign-in",
    summary="Sign In With Email and Password",
    response_model=SignInWithEmailAndPasswordResponse,
)
def sign_in_with_email_and_password(
    request: SignInWithEmailAndPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
):

    try:
        access_token = auth_service.sign_in_with_email_and_password(
            email=request.email,
            password=request.password,
        )

        return SignInWithEmailAndPasswordResponse(
            access_token=access_token,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.post("/sign-in/google", summary="Sign In with Google")
def sign_in_with_google():

    pass

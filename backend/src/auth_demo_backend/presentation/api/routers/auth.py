from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
import httpx

from auth_demo_backend.config import Config
from auth_demo_backend.application.services.auth_service import AuthService
from ..models import (
    SignInWithEmailAndPasswordRequest,
    SignInWithEmailAndPasswordResponse,
    SignUpWithEmailAndPasswordRequest,
    GetCurrentUserResponse,
)
from ..dependencies import get_auth_service, get_oauth, get_config

router = APIRouter(prefix="/auth")


@router.get(
    "/current-user",
    summary="Get Current User",
    response_model=GetCurrentUserResponse,
)
async def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):

    # Get the access token from the request
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")

    # Get the current user
    try:
        user = auth_service.get_current_user(access_token)

        return GetCurrentUserResponse(
            id=user.id,
            display_name=user.display_name,
            email=user.email,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        ) from error


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


@router.get("/sign-in/google", summary="Sign In With Google")
async def sign_in_with_google(
    request: Request,
    oauth: OAuth = Depends(get_oauth),
):

    google_client: StarletteOAuth2App = oauth.create_client("google")
    redirect_uri = request.url_for("sign_in_with_google_callback")

    redirect_response = await google_client.authorize_redirect(
        request=request,
        redirect_uri=redirect_uri,
        prompt="consent",
    )

    return redirect_response

    authorization_url_with_state = await google_client.create_authorization_url(
        redirect_uri=str(redirect_uri),
        prompt="consent",
    )

    print("authorization_url_with_state:")
    print(authorization_url_with_state)

    authorization_url = authorization_url_with_state.get("url")
    state = authorization_url_with_state.get("nonce")

    return RedirectResponse(url=authorization_url)


@router.get("/sign-in/google/callback", summary="Sign In With Google Callback")
async def sign_in_with_google_callback(
    request: Request,
    config: Config = Depends(get_config),
    oauth: OAuth = Depends(get_oauth),
):

    google_client: StarletteOAuth2App = oauth.create_client("google")
    # access_token_response = await google_client.authorize_access_token(request)

    redirect_uri = str(request.url_for("sign_in_with_google_callback"))

    print(f"request.query_params: {request.query_params}")
    print(f"request.query_params.get('code'): {request.query_params.get('code')}")
    print(f"request.query_params.get('state'): {request.query_params.get('state')}")

    access_token_response = await google_client.fetch_access_token(
        redirect_uri=redirect_uri,
        code=request.query_params.get("code"),
        state=request.query_params.get("state"),
    )

    print(access_token_response)

    return RedirectResponse(url=config.frontend_base_url)


@router.get(
    "/sign-out",
    summary="Sign Out",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def sign_out(
    request: Request,
    config: Config = Depends(get_config),
    oauth: OAuth = Depends(get_oauth),
):

    # Get the access token from the request
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")

    google_client: StarletteOAuth2App = oauth.create_client("google")

    # Clear the session
    request.session.clear()

    # Revoke Google token
    is_revoked = await revoke_google_token(access_token)

    if not is_revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to revoke Google token",
        )

    # Redirect to the home page
    return RedirectResponse(url=config.frontend_base_url)


async def revoke_google_token(token: str):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://oauth2.googleapis.com/revoke",
                params={"token": token},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        return True
    except Exception:
        return False

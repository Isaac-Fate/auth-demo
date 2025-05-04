from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App


from auth_demo_backend.application.services.auth_service import AuthService
from ..models import (
    SignInWithEmailAndPasswordRequest,
    SignInWithEmailAndPasswordResponse,
    SignUpWithEmailAndPasswordRequest,
    GetCurrentUserResponse,
)
from ..dependencies import get_auth_service, get_oauth

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

    google_client = oauth.create_client("google")
    redirect_uri = request.url_for("sign_in_with_google_callback")

    redirect_response = await google_client.authorize_redirect(
        request=request,
        redirect_uri=redirect_uri,
    )

    return redirect_response


@router.get("/sign-in/google/callback", summary="Sign In With Google Callback")
async def sign_in_with_google_callback(
    request: Request,
    oauth: OAuth = Depends(get_oauth),
):

    google_client: StarletteOAuth2App = oauth.create_client("google")
    access_token_response = await google_client.authorize_access_token(request)

    # return access_token_response

    print(access_token_response)

    return RedirectResponse(url="http://localhost:3000")


@router.get(
    "/sign-out",
    summary="Sign Out",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def sign_out(
    request: Request,
    oauth: OAuth = Depends(get_oauth),
):

    # Get the access token from the request
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")

    google_client: StarletteOAuth2App = oauth.create_client("google")

    # Clear the session
    request.session.clear()

    # Revoke the access token
    google_client.revoke_token(access_token)

    # return RedirectResponse(google_logout_url)

    # Redirect to the home page
    return RedirectResponse(url="/")

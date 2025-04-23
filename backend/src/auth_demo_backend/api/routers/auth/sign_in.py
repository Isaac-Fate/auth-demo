from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from authlib.integrations.starlette_client import StarletteOAuth2App, OAuthError
from sqlalchemy import Engine

from auth_demo_backend.api.dependencies import (
    get_config,
    get_google_oauth_app,
    get_db_engine,
)
from auth_demo_backend.config import Config
from auth_demo_backend.models import UserInfo, EmailPasswordSignInData
from auth_demo_backend import services


router = APIRouter(prefix="/sign-in")


@router.post("/")
async def sign_in(
    data: EmailPasswordSignInData,
    db_engine: Engine = Depends(get_db_engine),
):

    data = EmailPasswordSignInData.model_validate(data)
    user = services.sign_in_with_email(db_engine, data)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Failed to sign in",
        )

    return user


@router.get("/google")
async def sign_in_with_google(
    request: Request,
    google_oauth_app: StarletteOAuth2App = Depends(get_google_oauth_app),
):

    redirect_uri = request.url_for("sign_in_with_google_callback")

    # Get the redirect resposne
    response = await google_oauth_app.authorize_redirect(
        request,
        redirect_uri,
        prompt="consent",
    )

    return response


@router.get("/google/callback")
async def sign_in_with_google_callback(
    request: Request,
    config: Config = Depends(get_config),
    google_oauth_app: StarletteOAuth2App = Depends(get_google_oauth_app),
):

    try:
        access_token_response_data = await google_oauth_app.authorize_access_token(
            request
        )

    except OAuthError:
        return RedirectResponse(url="/")

    # Get the user info
    user_info = UserInfo.model_validate(access_token_response_data["userinfo"])

    print(user_info)

    return RedirectResponse(url=f"{config.frontend_url}")

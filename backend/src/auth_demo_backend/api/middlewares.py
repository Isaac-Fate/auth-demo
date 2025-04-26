from typing import Callable, Awaitable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from auth_demo_backend.services.auth import verify_access_token


async def auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
):
    # List of paths that don't require authentication
    open_paths = [
        # Authentication
        "/sign-up",
        "/sign-in",
        "/verify-access-token",
        # Documentation
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    # Pass through open paths
    if request.url.path in open_paths:
        return await call_next(request)

    # Check for Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"},
        )

    # Extract the access token
    access_token = auth_header.split(" ")[1]

    try:
        jwt_secret_key = request.app.state.config.jwt_secret_key
        user_info = verify_access_token(access_token, jwt_secret_key)

        print(user_info)

        # Store the user info in the request state for later use
        request.state.user_info = user_info

        # Send the request to the next middleware or route handler
        return await call_next(request)

    except Exception as e:

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": f"failed to verify access token: {e}"},
        )

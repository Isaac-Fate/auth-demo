from fastapi import Request, Response
from typing import Callable, Awaitable


SKIP_PATHS = [
    "/api/health",
    "/api/auth/sign-up",
    "/api/auth/sign-in",
]


async def auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
):

    # Skip the paths that do not require authentication
    if request.url.path in SKIP_PATHS:
        return await call_next(request)

    # Get the access token from the request
    access_token = request.headers.get("Authorization")

    # Remove the "Bearer " prefix from the access token
    access_token = access_token.removeprefix("Bearer ")

    # Verify the access token
    # verify_access_token(access_token)

    response = await call_next(request)

    return response

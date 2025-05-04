from fastapi import Request, Response
from typing import Callable, Awaitable


SKIP_PATHS = [
    "/api/health",
]

SKIP_PATH_PREFIXES = [
    "/api/auth",
]


async def auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
):

    # Skip the paths that do not require authentication

    if request.url.path in SKIP_PATHS:
        return await call_next(request)

    if any(request.url.path.startswith(prefix) for prefix in SKIP_PATH_PREFIXES):
        return await call_next(request)

    # Get the access token from the request
    access_token = request.headers.get("Authorization", "").removeprefix("Bearer ")

    # Verify the access token
    # verify_access_token(access_token)

    print(f"access token detected in middleware: {access_token}")

    response = await call_next(request)

    return response

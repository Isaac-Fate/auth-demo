from fastapi import APIRouter, Request
from .sign_up import router as sign_up_router
from .sign_in import router as sign_in_router


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/get-user-info")
def get_user_info(request: Request):

    # Get the user info from the request state
    user_info = request.state.user_info

    return user_info


# Register sub-routers
router.include_router(sign_up_router)
router.include_router(sign_in_router)

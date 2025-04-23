from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from auth_demo_backend.api.dependencies import get_db_session
from auth_demo_backend.models import UserCreate, User
from auth_demo_backend import services


router = APIRouter(prefix="/sign-up")


@router.post("/", response_model=User)
async def sign_up(
    user_create: UserCreate,
    db_session: Session = Depends(get_db_session),
):

    try:
        user = services.create_user_by_email_and_password(db_session, user_create)
        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

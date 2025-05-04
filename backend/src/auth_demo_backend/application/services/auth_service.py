from auth_demo_backend.domain.services.auth_service import (
    AuthService as DomainAuthService,
)
from auth_demo_backend.domain.entities import User


class AuthService:

    def __init__(self, domain_auth_service: DomainAuthService) -> None:

        self._domain_auth_service = domain_auth_service

    def get_current_user(self, access_token: str) -> User:

        return self._domain_auth_service.verify_access_token(access_token)

    def sign_up_with_email_and_password(
        self,
        display_name: str,
        email: str,
        password: str,
    ):

        # Create a new user
        user = User.from_sign_up(
            display_name=display_name,
            email=email,
            password=password,
        )

        # Register the user
        self._domain_auth_service.register_user(user, None)

    def sign_in_with_email_and_password(self, email: str, password: str):

        access_token = self._domain_auth_service.sign_in_with_email_and_password(
            email,
            password,
        )

        return access_token

    def sign_in_with_google():
        pass

    def sign_in_with_github():
        pass

    def sign_out():
        pass

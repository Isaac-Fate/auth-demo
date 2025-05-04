from typing import Optional

from ..repositories import IUnitOfWork
from ..ports import IAccessTokenIssuer
from ..entities import User, Account


class AuthService:

    def __init__(
        self,
        unit_of_work: IUnitOfWork,
        access_token_issuer: IAccessTokenIssuer,
    ):

        self._unit_of_work = unit_of_work
        self._access_token_issuer = access_token_issuer

    def register_user(
        self,
        user: User,
        account: Optional[Account] = None,
    ):

        # Find the user by email
        with self._unit_of_work:
            existing_user = self._unit_of_work.user_repository.find_user_by_email(
                user.email
            )

        # No existing user, create a new one
        if existing_user is None:

            # No account is provided, create a new user
            if account is None:

                with self._unit_of_work:
                    self._unit_of_work.user_repository.add_user(user)

            # An account is provided, create a new user and link it to the account
            else:

                with self._unit_of_work:

                    # Add the user
                    self._unit_of_work.user_repository.add_user(user)

                    # Link the account to the user
                    account.link_to_user(user.id)

                    # Add the account
                    self._unit_of_work.account_repository.add_account(account)

        else:

            # No account is provided, raise an error
            if account is None:
                raise ValueError("User with this email already exists")

            # An account is provided
            else:

                # Check if there is an account with the same provider
                with self._unit_of_work:
                    existing_account = self._unit_of_work.account_repository.find_account_by_user_id_and_provider(
                        account.provider,
                        existing_user.id,
                    )

                # No existing account, create a new one
                if existing_account is None:

                    # Link the account to the user
                    account.link_to_user(existing_user.id)

                    # Add the account
                    with self._unit_of_work:
                        self._unit_of_work.account_repository.add_account(account)

                # An account with the same provider already exists, raise an error
                else:
                    raise ValueError("Account with this provider already exists")

    def find_user_accounts(self, user: User) -> list[Account]:

        with self._unit_of_work:
            return self._unit_of_work.account_repository.find_accounts_by_user_id(
                user.id
            )

    def sign_in_with_email_and_password(self, email: str, password: str) -> str:

        # Find the user by email
        with self._unit_of_work:
            user = self._unit_of_work.user_repository.find_user_by_email(email)

        if user is None:
            raise ValueError("User not found")

        # Verify the password
        if not user.check_password(password):
            raise ValueError("Invalid password")

        # Issue the access token
        access_token = self._access_token_issuer.issue_access_token(user)

        return access_token

    def verify_access_token(self, access_token: str) -> User:

        # Verify the access token and get the user
        user = self._access_token_issuer.verify_access_token(access_token)

        return user

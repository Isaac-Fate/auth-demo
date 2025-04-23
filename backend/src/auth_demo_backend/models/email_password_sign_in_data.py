from typing import Literal
from .sign_in_data_base import SignInDataBase
from .account_provider import AccountProvider


class EmailPasswordSignInData(SignInDataBase):

    account_provider: Literal[AccountProvider.EMAIL] = AccountProvider.EMAIL
    email: str
    password: str

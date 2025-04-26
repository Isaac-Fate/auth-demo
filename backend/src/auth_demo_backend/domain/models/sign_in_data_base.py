from .configured_base_model import ConfiguredBaseModel
from .account_provider import AccountProvider


class SignInDataBase(ConfiguredBaseModel):

    account_provider: AccountProvider

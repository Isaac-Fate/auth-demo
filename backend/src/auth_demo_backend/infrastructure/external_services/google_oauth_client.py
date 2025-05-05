from typing import Optional
import base64
import json
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App

from auth_demo_backend.domain.ports import IOAuthClient
from auth_demo_backend.domain.entities import User, Account
from auth_demo_backend.domain.value_objects import AccountProvider


class GoogleOAuthClient(IOAuthClient):

    def __init__(self, oauth: OAuth) -> None:

        self._client: StarletteOAuth2App = oauth.create_client("google")

    async def create_authorization_url(
        self,
        redirect_uri: str,
        prompt: Optional[str] = None,
        **kwargs,
    ) -> str:

        authorization_url_with_state: dict[str, str] = (
            await self._client.create_authorization_url(
                redirect_uri,
                prompt,
                **kwargs,
            )
        )

        authorization_url = authorization_url_with_state["url"]

        return authorization_url

    async def get_user_with_account(
        self,
        redirect_uri: str,
        code: str,
        state: Optional[str] = None,
        **kwargs,
    ) -> tuple[User, Account]:

        access_token_response: dict[str, str] = await self._client.fetch_access_token(
            redirect_uri,
            code=code,
            state=state,
            **kwargs,
        )

        # Get the ID token
        id_token = access_token_response["id_token"]

        # Decode the ID token
        encoded_header, encoded_payload, encoded_signature = id_token.split(".")

        # Decode the payload
        payload = json.loads(base64.b64decode(encoded_payload).decode("utf-8"))

        # Construct the user entity
        user = User(
            display_name=payload["name"],
            email=payload["email"],
            avatar_url=payload["picture"],
        )

        # Construct the account entity
        account = Account(
            email=payload["email"],
            provider=AccountProvider.GOOGLE,
            avatar_url=payload["picture"],
        )

        return user, account

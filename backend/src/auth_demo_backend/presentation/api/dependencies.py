from auth_demo_backend.container import container
from auth_demo_backend.config import Config


def get_config():
    return Config.model_validate(container.config())


def get_auth_service():
    return container.auth_service()


def get_oauth():
    return container.oauth()

from auth_demo_backend.container import container


def get_auth_service():
    return container.auth_service()


def get_oauth():
    return container.oauth()

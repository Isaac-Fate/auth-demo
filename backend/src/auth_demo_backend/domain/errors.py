class EntityIdNotSetError(Exception):

    def __str__(self):
        return "Entity ID is not set"


class EntityIdAlreadySetError(Exception):

    def __str__(self):
        return "Entity ID is already set"

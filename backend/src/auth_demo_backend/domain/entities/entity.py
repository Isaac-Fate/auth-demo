from typing import Any, Optional

from ..errors import EntityIdNotSetError, EntityIdAlreadySetError


class Entity:

    def __init__(self, id: Optional[int] = None) -> None:

        if id is not None:
            self._id = id
        else:
            self._id = None

        # A flag to check if the ID is set
        self._is_id_set = id is not None

    def __repr__(self) -> str:

        display_attributes: list[tuple[str, Any]] = []
        for attribute_name, attribute_value in self.__dict__.items():

            if attribute_name.startswith("_"):
                continue

            display_attributes.append((attribute_name, attribute_value))

        # Include the ID in it is set
        if self.is_id_set():
            display_attributes.insert(0, ("id", self._id))

        # Format the attributes
        display_attributes_str = ", ".join(
            [f"{key}={value}" for key, value in display_attributes]
        )

        return f"{self.__class__.__name__}({display_attributes_str})"

    @property
    def id(self) -> int:

        if self._id is None:
            raise EntityIdNotSetError()

        return self._id

    @id.setter
    def id(self, id: int):

        if self._is_id_set:
            raise EntityIdAlreadySetError()

        # Set the ID
        self._id = id

        # Mark that the ID is set
        self._is_id_set = True

    def is_id_set(self) -> bool:
        return self._is_id_set

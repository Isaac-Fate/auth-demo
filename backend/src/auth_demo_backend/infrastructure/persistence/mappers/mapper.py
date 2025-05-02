from typing import Protocol, Any
from abc import abstractmethod


class IMapper(Protocol):

    @staticmethod
    @abstractmethod
    def to_domain_model(db_model: Any) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def to_db_model(domain_model: Any) -> Any:
        pass

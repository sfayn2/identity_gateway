from abc import ABC, abstractmethod

class IdPAdapter(ABC):
    @abstractmethod
    def decode_token(self, token: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def normalize_claims(self, claims: dict, token_type: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method")
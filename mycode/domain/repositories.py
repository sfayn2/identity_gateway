from abc import ABC, abstractmethod
from mycode.domain import models

class TenantRepositoryAbstract(ABC):
    @abstractmethod
    def get_tenant(self, tenant_id: str) -> models.Tenant:
        raise NotImplementedError("Subclasses must implement this method")


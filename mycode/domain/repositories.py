from abc import ABC, abstractmethod
from mycode.domain.models.tenant import Tenant

class TenantRepositoryAbstract(ABC):
    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Tenant:
        raise NotImplementedError("Subclasses must implement this method")


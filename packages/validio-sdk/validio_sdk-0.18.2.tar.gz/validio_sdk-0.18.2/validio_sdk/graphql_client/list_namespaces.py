from typing import Any, List

from .base_model import BaseModel


class ListNamespaces(BaseModel):
    namespaces: List["ListNamespacesNamespaces"]


class ListNamespacesNamespaces(BaseModel):
    id: Any


ListNamespaces.model_rebuild()

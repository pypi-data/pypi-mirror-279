from collections.abc import Container
from dataclasses import dataclass
from typing import Any


@dataclass
class SpiceObject:
    type: str
    id: str

    @classmethod
    def from_obj(cls, obj):
        def _hasitem(obj, name: str):
            return isinstance(obj, Container) and name in obj

        if hasattr(obj, "get_spicedb_type"):
            type = obj.get_spicedb_type()  # pyright: ignore [reportAttributeAccessIssue]
        elif hasattr(obj, "spicedb_type"):
            type = obj.spicedb_type  # pyright: ignore [reportAttributeAccessIssue]
        elif _hasitem(obj, "type"):
            type = obj["type"]
        elif hasattr(obj, "__tablename__"):
            type = obj.__tablename__  # pyright: ignore [reportAttributeAccessIssue]
        else:
            raise ValueError(f"{obj!r} has no spicedb_type specified")

        if hasattr(obj, "get_spicedb_id"):
            id = obj.get_spicedb_id()  # pyright: ignore [reportAttributeAccessIssue]
        elif hasattr(obj, "spicedb_id"):
            id = obj.spicedb_id  # pyright: ignore [reportAttributeAccessIssue]
        elif _hasitem(obj, "id"):
            id = obj["id"]
        elif hasattr(obj, "id"):
            id = obj.id  # pyright: ignore [reportAttributeAccessIssue]
        else:
            raise ValueError(f"{obj!r} has no ID")

        return cls(type=type, id=id)

    def __str__(self) -> str:
        return f"{self.type}:{self.id}"

    def to_spicedb_dict(self):
        return {
            "objectType": self.type,
            "objectId": self.id,
        }


class SpiceRelationship:
    actor: SpiceObject
    role: str
    resource: SpiceObject

    def __init__(self, actor: Any, role: str, resource: Any):
        self.actor = (
            actor
            if isinstance(actor, SpiceObject)
            else SpiceObject.from_obj(actor)
        )
        self.role = role
        self.resource = (
            resource
            if isinstance(resource, SpiceObject)
            else SpiceObject.from_obj(resource)
        )

    def __str__(self) -> str:
        """
        Returns a Zanzibar-like string representation (``resource#role@actor``).
        """
        return f"{self.resource}#{self.role}@{self.actor}"

    def __repr__(self) -> str:
        return f"<@{self.actor} #{self.role} on {self.resource}>"

    def to_spicedb_dict(self):
        return {
            "resource": self.resource.to_spicedb_dict(),
            "relation": self.role,
            "subject": {"object": self.actor.to_spicedb_dict()},
        }

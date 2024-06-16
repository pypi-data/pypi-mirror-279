import json
import importlib.metadata
from typing import Iterable
from httpx import AsyncClient

from spicedb.types import SpiceObject, SpiceRelationship


class SpiceDB:
    def __init__(
        self,
        api_root: str,
        api_key: str,
        *,
        minimize_latency: bool = False,
    ) -> None:
        self.client = AsyncClient(
            base_url=api_root,
            headers={
                "User-Agent": self._get_user_agent(),
                "Authorization": "Bearer {0}".format(api_key),
            }
        )

        if minimize_latency:
            self._default_consistency = {"minimizeLatency": True}
        else:
            self._default_consistency = {"fullyConsistent": True}
    
    @classmethod
    def _get_user_agent(cls):
        meta = importlib.metadata.distribution("spicedb").metadata
        return "python-httpx/{httpx_version} spicedb/{version} ({url})".format(
            httpx_version=importlib.metadata.version("httpx"),
            version=meta["Version"],
            url=meta["Home-page"],
        )

    async def bulk(
        self,
        *,
        create: Iterable[SpiceRelationship] | None = None,
        delete: Iterable[SpiceRelationship] | None = None,
        exist_ok: bool = True,
    ) -> str:
        """
        Deletes and adds many relationships in one atomic transaction. The
        deletions are performed before the adds. This does not support
        wildcards. Does not throw an error when the relationships to delete are
        not found.
        """

        create_op = "OPERATION_TOUCH" if exist_ok else "OPERATION_CREATE"
        updates = [
            {
                "operation": create_op,
                "relationship": rel.to_spicedb_dict(),
            } for rel in create or ()
        ] + [
            {
                "operation": "OPERATION_DELETE",
                "relationship": rel.to_spicedb_dict(),
            } for rel in delete or ()
        ]

        res = await self.client.post(
            "v1/relationships/write",
            json={"updates": updates}
        )
        res.raise_for_status()
        return res.json()["writtenAt"]["token"]
    
    async def bulk_delete(
        self,
        *,
        actor: SpiceObject | object | str | None,
        role: str | None = None,
        resource: SpiceObject | object | str,
    ):
        """
        Deletes many realtionships at once.

        If actor or resource is a string, will delete all relationships with a
        given subject or resource type. If actor or role is None, it will be
        treated as wildcard.

        Example:
            spice.bulk_delete(actor="user", resource=my_project)
            # Remove all users from a repo
        """

        filter = {}

        if isinstance(actor, str):
            filter["optionalSubjectFilter"] = {"subjectType": actor}
        elif actor:
            if not isinstance(actor, SpiceObject):
                actor = SpiceObject.from_obj(actor)

            filter["optionalSubjectFilter"] = {
                "subjectType": actor.type,
                "optionalSubjectId": actor.id,
            }
        
        if role:
            filter["optionalRelation"] = role
        
        if isinstance(resource, str):
            filter["resourceType"] = resource
        else:
            if not isinstance(resource, SpiceObject):
                resource = SpiceObject.from_obj(resource)

            filter["resourceType"] = resource.type
            filter["optionalResourceId"] = resource.id

        res = await self.client.post(
            "v1/relationships/delete",
            json={"relationshipFilter": filter}
        )
        res.raise_for_status()
        return res.json()["deletedAt"]["token"]

    async def set_schema(self, schema: str):
        """
        Updates the schema in SpiceDB.
        """

        await self.client.post(
            "v1/schema/write",
            json={"schema": schema}
        )

    async def read_schema(self) -> str:
        """
        Returns the current schema used by SpiceDB.
        """

        res = await self.client.post(
            "v1/schema/read"
        )
        res.raise_for_status()
        return res.json()["schemaText"]

    def _consistency_to_dict(
        self,
        *,
        minimize_latency: bool = False,
        at_least_as_fresh: str | None = None,
        at_exact_snapshot: str | None = None,
        fully_consistent: bool = False,
    ) -> dict:
        if minimize_latency:
            return {"minimizeLatency": True}
        if at_least_as_fresh:
            return {"atLeastAsFresh": {"token": at_least_as_fresh}}
        if at_exact_snapshot:
            return {"atExactSnapshot": {"token": at_least_as_fresh}}
        if fully_consistent:
            return {"fullyConsistent": True}
        
        return self._default_consistency

    async def authorize(
        self,
        actor: SpiceObject | object,
        action: str,
        resource: SpiceObject | object,
        *,
        minimize_latency: bool = False,
        at_least_as_fresh: str | None = None,
        at_exact_snapshot: str | None = None,
        fully_consistent: bool = False,
    ) -> bool:
        """
        Determines whether or not an action is allowed, based on a combination
        of authorization data and policy logic.
        """

        if not isinstance(actor, SpiceObject):
            actor = SpiceObject.from_obj(actor)
        if not isinstance(resource, SpiceObject):
            resource = SpiceObject.from_obj(resource)

        consistency = self._consistency_to_dict(
            minimize_latency=minimize_latency,
            at_least_as_fresh=at_least_as_fresh,
            at_exact_snapshot=at_exact_snapshot,
            fully_consistent=fully_consistent,
        )

        res = await self.client.post(
            "v1/permissions/check",
            json={
                "consistency": consistency,
                "resource": resource.to_spicedb_dict(),
                "permission": action,
                "subject": {"object": actor.to_spicedb_dict()},
            }
        )
        res.raise_for_status()
        return res.json().get("permissionship") == "PERMISSIONSHIP_HAS_PERMISSION"
    
    async def list(
        self,
        actor: SpiceObject | object,
        action: str,
        resource_type: str,
        *,
        minimize_latency: bool = False,
        at_least_as_fresh: str | None = None,
        at_exact_snapshot: str | None = None,
        fully_consistent: bool = False,
    ):
        """
        Fetches a list of resources on which an actor can perform a particular
        action.
        """

        if not isinstance(actor, SpiceObject):
            actor = SpiceObject.from_obj(actor)

        consistency = self._consistency_to_dict(
            minimize_latency=minimize_latency,
            at_least_as_fresh=at_least_as_fresh,
            at_exact_snapshot=at_exact_snapshot,
            fully_consistent=fully_consistent,
        )

        res_ctx = self.client.stream(
            "POST",
            "v1/permissions/resources",
            json={
                "consistency": consistency,
                "resourceObjectType": resource_type,
                "permission": action,
                "subject": {"object": actor.to_spicedb_dict()},
            },
        )

        async with res_ctx as res:
            async for line in res.aiter_lines():
                data = json.loads(line)
                object_id: str = data["result"]["resourceObjectId"]
                yield object_id

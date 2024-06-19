from __future__ import annotations

from typing import Optional

from marshmallow import fields
from s4.platform.changeset.changeset import Changeset, ChangesetSchema
from s4.platform.connection import Connection
from s4.platform.environment.environment_configuration import (
    EnvironmentConfiguration,
    EnvironmentConfigurationSchema,
)
from s4.platform.internal.base_model import ConnectedModel
from s4.platform.internal.base_schema import ConnectedModelSchema
from s4.platform.internal.lazy_property_list import LazyProperty


class Environment(ConnectedModel):
    current_changeset: LazyProperty[ConnectedModel, Changeset] = LazyProperty(
        ChangesetSchema, "current_changeset_iri"
    )

    def __init__(
        self,
        *,
        connection: Connection = None,
        iri: Optional[str],
        short_name: str,
        label: str,
        # @deprecated. This parameter will always be None in objects returned from the Labbit backend and will
        # be ignored by endpoints that expect objects of this type as a payload
        was_generated_by: Optional[str] = None,
        current_changeset_iri: Optional[str] = None,
        configuration: Optional[EnvironmentConfiguration] = None,
    ):
        super().__init__(connection)
        self.iri = iri
        self.short_name = short_name
        self.label = label
        self.current_changeset_iri = current_changeset_iri
        self.was_generated_by = was_generated_by
        self.configuration = configuration

    @staticmethod
    def by_name(connection: Connection, name: str) -> Environment:
        json = connection.fetch_json(f"environment/{name}/withConfig")
        return Environment._from_json(connection, json)

    @staticmethod
    def _from_json(connection: Connection, json: dict) -> Environment:
        task_schema = EnvironmentSchema()
        task_schema.context["connection"] = connection
        return task_schema.load(json)


class EnvironmentSchema(ConnectedModelSchema):
    def __init__(self, **kwargs):
        super().__init__(Environment, **kwargs)

    iri = fields.Str(load_only=True, allow_none=True)
    short_name = fields.Str()
    label = fields.Str()
    was_generated_by = fields.Str(load_only=True, allow_none=True, load_default=None)
    current_changeset_iri = fields.Str(load_only=True, allow_none=True)
    configuration = fields.Nested(EnvironmentConfigurationSchema(), allow_none=True)

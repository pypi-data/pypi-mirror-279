from __future__ import annotations

from typing import List, Optional, Any, TypeVar, Union

from pydantic import BaseModel

from bigeye_sdk.bigconfig_validation.yaml_model_base import (
    YamlModelWithValidatorContext,
)
from bigeye_sdk.generated.com.bigeye.models.generated import Schema, Table, TableColumn, DataNodeType
from bigeye_sdk.serializable import File
from bigeye_sdk.log import get_logger

log = get_logger(__file__)

LINEAGE_CONFIGURATION_FILE = TypeVar(
    "LINEAGE_CONFIGURATION_FILE", bound="LineageConfigurationFile"
)


class SimpleLineageEdgeRequest(BaseModel):
    upstream: Union[Table, TableColumn]
    downstream: Union[Table, TableColumn]
    node_type: DataNodeType


class LineageConfigurationFile(File):
    pass


class LineageColumnOverride(YamlModelWithValidatorContext):
    upstream_column_name: str
    downstream_column_name: str


class LineageTableOverride(YamlModelWithValidatorContext):
    upstream_table_name: str
    downstream_table_name: str
    column_overrides: Optional[List[LineageColumnOverride]] = None
    column_name_exclusions: Optional[List[str]] = None


class LineageConfiguration(YamlModelWithValidatorContext):
    """
    The Simple Lineage Configuration is a Yaml serializable configuration file used to configure and version lineage as
    a file.

    Attributes:
        upstream_schema_name: The fq schema name of upstream entity.
        downstream_schema_name: The fq schema name of downstream entity.
        table_overrides: Optional list of tables where names do not match and will need to be mapped.
    """
    upstream_schema_name: str
    downstream_schema_name: str
    table_overrides: Optional[List[LineageTableOverride]] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.__verify_config()

    def __verify_config(self):
        pass


class SimpleLineageConfigurationFile(
    LineageConfigurationFile, type="LINEAGE_CONFIGURATION_FILE"
):
    relations: Optional[List[LineageConfiguration]] = None

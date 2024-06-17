from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    CredentialId,
    CronExpression,
    JsonTypeDefinition,
    SegmentationId,
    SourceId,
    WindowId,
)

from .base_model import BaseModel
from .enums import FileFormat, SourceState, StreamingSourceMessageFormat


class GetSourceByResourceNameDeprecated(BaseModel):
    source_by_resource_name: Optional[
        Annotated[
            Union[
                "GetSourceByResourceNameDeprecatedSourceByResourceNameSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3Source",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSource",
                "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceByResourceName")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCredential"
    windows: List["GetSourceByResourceNameDeprecatedSourceByResourceNameSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceByResourceNameDeprecatedSourceByResourceNameSourceTags"]


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSourceTags(BaseModel):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceTags"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSourceConfig(
    BaseModel
):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfig(
    BaseModel
):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSourceConfig(
    BaseModel
):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceTags"]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceTags(BaseModel):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfigCsv"
    ]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfigCsv(
    BaseModel
):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSource(
    BaseModel
):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSourceConfig(
    BaseModel
):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSourceConfig(
    BaseModel
):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSourceConfig(
    BaseModel
):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSourceConfig(
    BaseModel
):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSource(
    BaseModel
):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSourceConfig(
    BaseModel
):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySourceConfig(
    BaseModel
):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSource(
    BaseModel
):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfig(
    BaseModel
):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceTags"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfig(
    BaseModel
):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfig(
    BaseModel
):
    project: str
    bucket: str
    folder: str
    csv: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfigCsv"
    ]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfigCsv(
    BaseModel
):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceTags"]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceTags(BaseModel):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCredential"
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceTags"
    ]
    config: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceConfig"
    )


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSourceConfig(
    BaseModel
):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: (
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCredential"
    )
    windows: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List[
        "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceTags"
    ]
    config: "GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceConfig"


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceCredential(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceWindows(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceSegmentations(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceTags(
    BaseModel
):
    key: str
    value: str


class GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSourceConfig(
    BaseModel
):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


GetSourceByResourceNameDeprecated.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsAthenaSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsKinesisSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsRedshiftSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3Source.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAwsS3SourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameAzureSynapseSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameClickHouseSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDatabricksSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtModelRunSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameDbtTestResultSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpBigQuerySource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubLiteSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpPubSubSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameGcpStorageSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameKafkaSourceConfig.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNamePostgreSqlSource.model_rebuild()
GetSourceByResourceNameDeprecatedSourceByResourceNameSnowflakeSource.model_rebuild()

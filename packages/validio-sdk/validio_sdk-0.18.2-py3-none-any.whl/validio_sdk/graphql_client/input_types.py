from datetime import datetime
from typing import Annotated, Any, List, Optional

from pydantic import Field, PlainSerializer

from validio_sdk.scalars import (
    CredentialId,
    CronExpression,
    JsonFilterExpression,
    JsonPointer,
    JsonTypeDefinition,
    SegmentationId,
    SourceId,
    ValidatorId,
    WindowId,
    serialize_json_filter_expression,
    serialize_rfc3339_datetime,
)

from .base_model import BaseModel
from .enums import (
    AzureSynapseBackendType,
    CategoricalDistributionMetric,
    ClickHouseProtocol,
    ComparisonOperator,
    DecisionBoundsType,
    DifferenceOperator,
    DifferenceType,
    FileFormat,
    IncidentSeverity,
    IncidentStatus,
    IssueTypename,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    Role,
    SortOrder,
    StreamingSourceMessageFormat,
    UserStatus,
    VolumeMetric,
    WindowTimeUnit,
)


class AwsAthenaCredentialCreateInput(BaseModel):
    access_key: str = Field(alias="accessKey")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    query_result_location: str = Field(alias="queryResultLocation")
    region: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    secret_key: str = Field(alias="secretKey")


class AwsAthenaCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    secret_key: str = Field(alias="secretKey")


class AwsAthenaCredentialUpdateInput(BaseModel):
    access_key: Optional[str] = Field(alias="accessKey", default=None)
    id: CredentialId
    name: Optional[str] = None
    query_result_location: Optional[str] = Field(
        alias="queryResultLocation", default=None
    )
    region: Optional[str] = None
    secret_key: Optional[str] = Field(alias="secretKey", default=None)


class AwsAthenaInferSchemaInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    database: str
    table: str


class AwsAthenaSourceCreateInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    table: str


class AwsAthenaSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class AwsCredentialCreateInput(BaseModel):
    access_key: str = Field(alias="accessKey")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    secret_key: str = Field(alias="secretKey")


class AwsCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    secret_key: str = Field(alias="secretKey")


class AwsCredentialUpdateInput(BaseModel):
    access_key: Optional[str] = Field(alias="accessKey", default=None)
    id: CredentialId
    name: Optional[str] = None
    secret_key: Optional[str] = Field(alias="secretKey", default=None)


class AwsKinesisInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    region: str
    stream_name: str = Field(alias="streamName")


class AwsKinesisSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    region: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    stream_name: str = Field(alias="streamName")


class AwsKinesisSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: Optional[str] = None


class AwsRedshiftCredentialCreateInput(BaseModel):
    default_database: str = Field(alias="defaultDatabase")
    host: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    password: str
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    user: str


class AwsRedshiftCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class AwsRedshiftCredentialUpdateInput(BaseModel):
    default_database: Optional[str] = Field(alias="defaultDatabase", default=None)
    host: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None


class AwsRedshiftInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: Optional[str] = None
    db_schema: str = Field(alias="schema")
    table: str


class AwsRedshiftSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: Optional[str] = None
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str


class AwsRedshiftSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class AwsS3InferSchemaInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    prefix: str


class AwsS3SourceCreateInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    prefix: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None


class AwsS3SourceUpdateInput(BaseModel):
    csv: Optional["CsvParserInput"] = None
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class AzureSynapseEntraIdCredentialCreateInput(BaseModel):
    backend_type: AzureSynapseBackendType = Field(alias="backendType")
    client_id: str = Field(alias="clientId")
    client_secret: str = Field(alias="clientSecret")
    database: Optional[str] = None
    host: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class AzureSynapseEntraIdCredentialSecretChangedInput(BaseModel):
    client_secret: str = Field(alias="clientSecret")
    id: CredentialId


class AzureSynapseEntraIdCredentialUpdateInput(BaseModel):
    backend_type: Optional[AzureSynapseBackendType] = Field(
        alias="backendType", default=None
    )
    client_id: Optional[str] = Field(alias="clientId", default=None)
    client_secret: Optional[str] = Field(alias="clientSecret", default=None)
    database: Optional[str] = None
    host: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    port: Optional[int] = None


class AzureSynapseInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: str
    db_schema: str = Field(alias="schema")
    table: str


class AzureSynapseSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str


class AzureSynapseSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class AzureSynapseSqlCredentialCreateInput(BaseModel):
    backend_type: AzureSynapseBackendType = Field(alias="backendType")
    database: Optional[str] = None
    host: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    password: str
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    username: str


class AzureSynapseSqlCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class AzureSynapseSqlCredentialUpdateInput(BaseModel):
    backend_type: Optional[AzureSynapseBackendType] = Field(
        alias="backendType", default=None
    )
    database: Optional[str] = None
    host: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None


class CategoricalDistributionValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: CategoricalDistributionMetric
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class CategoricalDistributionValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: Optional["ReferenceSourceConfigUpdateInput"] = Field(
        alias="referenceSourceConfig", default=None
    )
    source_config: Optional["SourceConfigUpdateInput"] = Field(
        alias="sourceConfig", default=None
    )


class ChannelDeleteInput(BaseModel):
    id: Any


class ClickHouseCredentialCreateInput(BaseModel):
    default_database: str = Field(alias="defaultDatabase")
    host: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    password: str
    port: int
    protocol: ClickHouseProtocol
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    username: str


class ClickHouseCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class ClickHouseCredentialUpdateInput(BaseModel):
    default_database: Optional[str] = Field(alias="defaultDatabase", default=None)
    host: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[ClickHouseProtocol] = None
    username: Optional[str] = None


class ClickHouseInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: Optional[str] = None
    table: str


class ClickHouseSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: Optional[str] = None
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    table: str


class ClickHouseSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class CsvParserInput(BaseModel):
    delimiter: str
    null_marker: Optional[str] = Field(alias="nullMarker", default=None)


class DatabricksCredentialCreateInput(BaseModel):
    access_token: str = Field(alias="accessToken")
    host: str
    http_path: str = Field(alias="httpPath")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class DatabricksCredentialSecretChangedInput(BaseModel):
    access_token: str = Field(alias="accessToken")
    id: CredentialId


class DatabricksCredentialUpdateInput(BaseModel):
    access_token: Optional[str] = Field(alias="accessToken", default=None)
    host: Optional[str] = None
    http_path: Optional[str] = Field(alias="httpPath", default=None)
    id: CredentialId
    name: Optional[str] = None
    port: Optional[int] = None


class DatabricksInferSchemaInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    db_schema: str = Field(alias="schema")
    table: str


class DatabricksSourceCreateInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str


class DatabricksSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class DatabricksStartWarehouseInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")


class DatabricksWarehouseInfoInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")


class DbtArtifactMultipartUploadAppendPartInput(BaseModel):
    id: Any
    part: str


class DbtArtifactMultipartUploadCompleteInput(BaseModel):
    id: Any


class DbtArtifactMultipartUploadCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    job_name: str = Field(alias="jobName")


class DbtArtifactUploadInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    job_name: str = Field(alias="jobName")
    manifest: Any
    run_results: Optional[Any] = Field(alias="runResults", default=None)


class DbtCloudCredentialCreateInput(BaseModel):
    account_id: str = Field(alias="accountId")
    api_base_url: Optional[str] = Field(alias="apiBaseUrl", default=None)
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    token: str
    warehouse_credential_id: CredentialId = Field(alias="warehouseCredentialId")


class DbtCloudCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    token: str


class DbtCloudCredentialUpdateInput(BaseModel):
    account_id: Optional[str] = Field(alias="accountId", default=None)
    api_base_url: Optional[str] = Field(alias="apiBaseUrl", default=None)
    id: CredentialId
    name: Optional[str] = None
    token: Optional[str] = None
    warehouse_credential_id: Optional[CredentialId] = Field(
        alias="warehouseCredentialId", default=None
    )


class DbtCoreCredentialCreateInput(BaseModel):
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    warehouse_credential_id: CredentialId = Field(alias="warehouseCredentialId")


class DbtCoreCredentialUpdateInput(BaseModel):
    id: CredentialId
    name: Optional[str] = None
    warehouse_credential_id: Optional[CredentialId] = Field(
        alias="warehouseCredentialId", default=None
    )


class DbtModelRunSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    job_name: str = Field(alias="jobName")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    project_name: str = Field(alias="projectName")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None


class DbtModelRunSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class DbtTestResultSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    job_name: str = Field(alias="jobName")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    project_name: str = Field(alias="projectName")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None


class DbtTestResultSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class DemoCredentialCreateInput(BaseModel):
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class DemoSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class DifferenceThresholdCreateInput(BaseModel):
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    operator: DifferenceOperator
    value: float


class DynamicThresholdCreateInput(BaseModel):
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType", default=None
    )
    sensitivity: float


class EnumQueryFilter(BaseModel):
    values: List[str]


class FileWindowCreateInput(BaseModel):
    data_time_field: JsonPointer = Field(alias="dataTimeField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")


class FixedBatchWindowCreateInput(BaseModel):
    batch_size: int = Field(alias="batchSize")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs", default=None)
    data_time_field: JsonPointer = Field(alias="dataTimeField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    segmented_batching: bool = Field(alias="segmentedBatching")
    source_id: SourceId = Field(alias="sourceId")


class FixedBatchWindowUpdateInput(BaseModel):
    batch_size: Optional[int] = Field(alias="batchSize", default=None)
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs", default=None)
    id: WindowId
    segmented_batching: Optional[bool] = Field(alias="segmentedBatching", default=None)


class FixedThresholdCreateInput(BaseModel):
    operator: ComparisonOperator
    value: float


class FreshnessValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: Optional[JsonPointer] = Field(alias="sourceField", default=None)


class FreshnessValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class GcpBigQueryInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    dataset: str
    project: str
    table: str


class GcpBigQuerySourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    dataset: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    table: str


class GcpBigQuerySourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class GcpCredentialCreateInput(BaseModel):
    credential: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class GcpCredentialSecretChangedInput(BaseModel):
    credential: str
    id: CredentialId


class GcpCredentialUpdateInput(BaseModel):
    credential: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None


class GcpPubSubInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    project: str
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubLiteInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    location: str
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    project: str
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubLiteSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    location: str
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubLiteSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: Optional[str] = None


class GcpPubSubSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: Optional[str] = None


class GcpStorageInferSchemaInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    folder: str
    project: str


class GcpStorageSourceCreateInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    folder: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None


class GcpStorageSourceUpdateInput(BaseModel):
    csv: Optional["CsvParserInput"] = None
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class GlobalWindowCreateInput(BaseModel):
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")


class IdentityDeleteInput(BaseModel):
    id: str


class IdentityProviderDeleteInput(BaseModel):
    id: str


class IncidentGroupOwnerUpdateInput(BaseModel):
    ids: List[Any]
    owner_id: Optional[Any] = Field(alias="ownerId", default=None)


class IncidentGroupStatusUpdateInput(BaseModel):
    ids: List[Any]
    status: IncidentStatus


class IncidentGroupsFilter(BaseModel):
    owner: Optional["EnumQueryFilter"] = None
    priority: Optional["EnumQueryFilter"] = None
    range: Optional["TimeRangeInput"] = None
    source: Optional["EnumQueryFilter"] = None
    status: Optional["EnumQueryFilter"] = None
    validator: Optional["EnumQueryFilter"] = None


class IncidentGroupsSort(BaseModel):
    first_seen_at: Optional["SortIndex"] = Field(alias="firstSeenAt", default=None)
    last_seen_at: Optional["SortIndex"] = Field(alias="lastSeenAt", default=None)
    priority: Optional["SortIndex"] = None
    status: Optional["SortIndex"] = None


class IncidentStatusUpdateInput(BaseModel):
    ids: List[Any]
    status: IncidentStatus


class IncidentsFilter(BaseModel):
    range: Optional["TimeRangeInput"] = None
    severity: Optional["EnumQueryFilter"] = None
    status: Optional["EnumQueryFilter"] = None


class IncidentsSort(BaseModel):
    created_at: Optional["SortIndex"] = Field(alias="createdAt", default=None)
    end_time: Optional["SortIndex"] = Field(alias="endTime", default=None)


class KafkaInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    topic: str


class KafkaSaslSslPlainCredentialCreateInput(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: Optional[str] = Field(alias="caCertificate", default=None)
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    password: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    username: str


class KafkaSaslSslPlainCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class KafkaSaslSslPlainCredentialUpdateInput(BaseModel):
    bootstrap_servers: Optional[List[str]] = Field(
        alias="bootstrapServers", default=None
    )
    ca_certificate: Optional[str] = Field(alias="caCertificate", default=None)
    id: CredentialId
    name: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None


class KafkaSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    topic: str


class KafkaSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: Optional[str] = None


class KafkaSslCredentialCreateInput(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")
    client_certificate: str = Field(alias="clientCertificate")
    client_private_key: str = Field(alias="clientPrivateKey")
    client_private_key_password: str = Field(alias="clientPrivateKeyPassword")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class KafkaSslCredentialSecretChangedInput(BaseModel):
    ca_certificate: str = Field(alias="caCertificate")
    client_certificate: str = Field(alias="clientCertificate")
    client_private_key: str = Field(alias="clientPrivateKey")
    client_private_key_password: str = Field(alias="clientPrivateKeyPassword")
    id: CredentialId


class KafkaSslCredentialUpdateInput(BaseModel):
    bootstrap_servers: Optional[List[str]] = Field(
        alias="bootstrapServers", default=None
    )
    ca_certificate: Optional[str] = Field(alias="caCertificate", default=None)
    client_certificate: Optional[str] = Field(alias="clientCertificate", default=None)
    client_private_key: Optional[str] = Field(alias="clientPrivateKey", default=None)
    client_private_key_password: Optional[str] = Field(
        alias="clientPrivateKeyPassword", default=None
    )
    id: CredentialId
    name: Optional[str] = None


class LineageEdgeCreateInput(BaseModel):
    downstream_field: Optional[JsonPointer] = Field(
        alias="downstreamField", default=None
    )
    downstream_id: Any = Field(alias="downstreamId")
    upstream_field: Optional[JsonPointer] = Field(alias="upstreamField", default=None)
    upstream_id: Any = Field(alias="upstreamId")


class LineageGraphInput(BaseModel):
    catalog_asset_id: Any = Field(alias="catalogAssetId")
    field: Optional[JsonPointer] = None
    limit: int


class LocalIdentityProviderUpdateInput(BaseModel):
    disabled: bool
    id: str
    name: str


class LookerCredentialCreateInput(BaseModel):
    base_url: str = Field(alias="baseUrl")
    client_id: str = Field(alias="clientId")
    client_secret: str = Field(alias="clientSecret")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class LookerCredentialSecretChangedInput(BaseModel):
    client_secret: str = Field(alias="clientSecret")
    id: CredentialId


class LookerCredentialUpdateInput(BaseModel):
    base_url: Optional[str] = Field(alias="baseUrl", default=None)
    client_id: Optional[str] = Field(alias="clientId", default=None)
    client_secret: Optional[str] = Field(alias="clientSecret", default=None)
    id: CredentialId
    name: Optional[str] = None


class MsTeamsChannelCreateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    timezone: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


class MsTeamsChannelUpdateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    id: Any
    name: Optional[str] = None
    timezone: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


class NotificationRuleConditionCreateInput(BaseModel):
    owner_condition: Optional["OwnerNotificationRuleConditionCreateInput"] = Field(
        alias="ownerCondition", default=None
    )
    segment_conditions: Optional[
        List["SegmentNotificationRuleConditionCreateInput"]
    ] = Field(alias="segmentConditions", default=None)
    severity_condition: Optional["SeverityNotificationRuleConditionCreateInput"] = (
        Field(alias="severityCondition", default=None)
    )
    source_condition: Optional["SourceNotificationRuleConditionCreateInput"] = Field(
        alias="sourceCondition", default=None
    )
    tag_conditions: Optional[List["TagNotificationRuleConditionCreateInput"]] = Field(
        alias="tagConditions", default=None
    )
    type_condition: Optional["TypeNotificationRuleConditionCreateInput"] = Field(
        alias="typeCondition", default=None
    )


class NotificationRuleCreateInput(BaseModel):
    channel_id: Any = Field(alias="channelId")
    conditions: Optional["NotificationRuleConditionCreateInput"] = None
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class NotificationRuleDeleteInput(BaseModel):
    id: Any


class NotificationRuleUpdateInput(BaseModel):
    channel_id: Optional[Any] = Field(alias="channelId", default=None)
    conditions: Optional["NotificationRuleConditionCreateInput"] = None
    id: Any
    name: Optional[str] = None


class NumericAnomalyValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: NumericAnomalyMetric
    minimum_absolute_difference: float = Field(alias="minimumAbsoluteDifference")
    minimum_reference_datapoints: Optional[float] = Field(
        alias="minimumReferenceDatapoints", default=None
    )
    minimum_relative_difference_percent: float = Field(
        alias="minimumRelativeDifferencePercent"
    )
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    sensitivity: float
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class NumericAnomalyValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: Optional["ReferenceSourceConfigUpdateInput"] = Field(
        alias="referenceSourceConfig", default=None
    )
    source_config: Optional["SourceConfigUpdateInput"] = Field(
        alias="sourceConfig", default=None
    )


class NumericDistributionValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: NumericDistributionMetric
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class NumericDistributionValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: Optional["ReferenceSourceConfigUpdateInput"] = Field(
        alias="referenceSourceConfig", default=None
    )
    source_config: Optional["SourceConfigUpdateInput"] = Field(
        alias="sourceConfig", default=None
    )


class NumericValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: NumericMetric
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class NumericValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class OwnerNotificationRuleConditionCreateInput(BaseModel):
    notification_rule_id: Optional[Any] = Field(
        alias="notificationRuleId", default=None
    )
    owners: List[str]


class OwnerNotificationRuleConditionUpdateInput(BaseModel):
    id: str
    owners: List[str]


class PaginationInput(BaseModel):
    after: Optional[str] = None
    before: Optional[str] = None
    limit: Optional[int] = None


class PastIncidentGroupsFilter(BaseModel):
    owner: Optional["EnumQueryFilter"] = None
    priority: Optional["EnumQueryFilter"] = None
    source: Optional["EnumQueryFilter"] = None
    status: Optional["EnumQueryFilter"] = None
    validator: Optional["EnumQueryFilter"] = None


class PostgreSqlCredentialCreateInput(BaseModel):
    default_database: str = Field(alias="defaultDatabase")
    host: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    password: str
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    user: str


class PostgreSqlCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class PostgreSqlCredentialUpdateInput(BaseModel):
    default_database: Optional[str] = Field(alias="defaultDatabase", default=None)
    host: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None


class PostgreSqlInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: Optional[str] = None
    db_schema: str = Field(alias="schema")
    table: str


class PostgreSqlSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: Optional[str] = None
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str


class PostgreSqlSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class ReferenceSourceConfigCreateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None
    history: int
    offset: int
    source_id: SourceId = Field(alias="sourceId")
    window_id: WindowId = Field(alias="windowId")


class ReferenceSourceConfigUpdateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None
    history: int
    offset: int


class RelativeTimeValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: RelativeTimeMetric
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")


class RelativeTimeValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class RelativeVolumeValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: RelativeVolumeMetric
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: Optional[JsonPointer] = Field(
        alias="referenceSourceField", default=None
    )
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: Optional[JsonPointer] = Field(alias="sourceField", default=None)


class RelativeVolumeValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: Optional["ReferenceSourceConfigUpdateInput"] = Field(
        alias="referenceSourceConfig", default=None
    )
    source_config: Optional["SourceConfigUpdateInput"] = Field(
        alias="sourceConfig", default=None
    )


class ResourceFilter(BaseModel):
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class ResourceNamespaceUpdateInput(BaseModel):
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    new_namespace_id: Optional[str] = Field(alias="newNamespaceId", default=None)
    new_resource_namespace: Optional[str] = Field(
        alias="newResourceNamespace", default=None
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class SamlIdentityProviderCreateInput(BaseModel):
    cert: str
    disabled: bool
    entity_id: str = Field(alias="entityId")
    entry_point: str = Field(alias="entryPoint")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class SamlIdentityProviderUpdateInput(BaseModel):
    cert: str
    disabled: bool
    entity_id: str = Field(alias="entityId")
    entry_point: str = Field(alias="entryPoint")
    id: str
    name: str


class SegmentFieldInput(BaseModel):
    field: JsonPointer
    value: str


class SegmentNotificationRuleConditionCreateInput(BaseModel):
    notification_rule_id: Optional[Any] = Field(
        alias="notificationRuleId", default=None
    )
    segments: List["SegmentFieldInput"]


class SegmentNotificationRuleConditionUpdateInput(BaseModel):
    id: str
    segments: List["SegmentFieldInput"]


class SegmentationCreateInput(BaseModel):
    fields: List[str]
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")


class SeverityNotificationRuleConditionCreateInput(BaseModel):
    notification_rule_id: Optional[Any] = Field(
        alias="notificationRuleId", default=None
    )
    severities: List[IncidentSeverity]


class SeverityNotificationRuleConditionUpdateInput(BaseModel):
    id: str
    severities: List[IncidentSeverity]


class SlackChannelCreateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    timezone: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


class SlackChannelUpdateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    id: Any
    name: Optional[str] = None
    timezone: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


class SnowflakeCredentialCreateInput(BaseModel):
    account: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    password: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    role: Optional[str] = None
    user: str
    warehouse: Optional[str] = None


class SnowflakeCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class SnowflakeCredentialUpdateInput(BaseModel):
    account: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    user: Optional[str] = None
    warehouse: Optional[str] = None


class SnowflakeInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: str
    role: Optional[str] = None
    db_schema: str = Field(alias="schema")
    table: str
    warehouse: Optional[str] = None


class SnowflakeSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    role: Optional[str] = None
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str
    warehouse: Optional[str] = None


class SnowflakeSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: Optional[JsonTypeDefinition] = Field(alias="jtdSchema", default=None)
    lookback_days: Optional[int] = Field(alias="lookbackDays", default=None)
    name: Optional[str] = None
    schedule: Optional[CronExpression] = None


class SortIndex(BaseModel):
    index: int
    order: SortOrder


class SourceConfigCreateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None
    segmentation_id: SegmentationId = Field(alias="segmentationId")
    source_id: SourceId = Field(alias="sourceId")
    window_id: WindowId = Field(alias="windowId")


class SourceConfigUpdateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None


class SourceNotificationRuleConditionCreateInput(BaseModel):
    notification_rule_id: Optional[Any] = Field(
        alias="notificationRuleId", default=None
    )
    sources: List[SourceId]


class SourceNotificationRuleConditionUpdateInput(BaseModel):
    id: str
    sources: List[SourceId]


class SourceOwnerUpdateInput(BaseModel):
    id: SourceId
    user_id: Optional[str] = Field(alias="userId", default=None)


class SqlValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    name: str
    query: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")


class StreamingSourceMessageFormatConfigInput(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema", default=None)


class TableauConnectedAppCredentialCreateInput(BaseModel):
    client_id: str = Field(alias="clientId")
    host: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    secret_id: str = Field(alias="secretId")
    secret_value: str = Field(alias="secretValue")
    site: str
    user: str


class TableauConnectedAppCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    secret_value: str = Field(alias="secretValue")


class TableauConnectedAppCredentialUpdateInput(BaseModel):
    client_id: Optional[str] = Field(alias="clientId", default=None)
    host: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    secret_id: Optional[str] = Field(alias="secretId", default=None)
    secret_value: Optional[str] = Field(alias="secretValue", default=None)
    site: Optional[str] = None
    user: Optional[str] = None


class TableauPersonalAccessTokenCredentialCreateInput(BaseModel):
    host: str
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    site: str
    token_name: str = Field(alias="tokenName")
    token_value: str = Field(alias="tokenValue")


class TableauPersonalAccessTokenCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    token_value: str = Field(alias="tokenValue")


class TableauPersonalAccessTokenCredentialUpdateInput(BaseModel):
    host: Optional[str] = None
    id: CredentialId
    name: Optional[str] = None
    site: Optional[str] = None
    token_name: Optional[str] = Field(alias="tokenName", default=None)
    token_value: Optional[str] = Field(alias="tokenValue", default=None)


class TagCreateInput(BaseModel):
    key: str
    value: str


class TagNotificationRuleConditionCreateInput(BaseModel):
    notification_rule_id: Optional[Any] = Field(
        alias="notificationRuleId", default=None
    )
    tags: List["TagCreateInput"]


class TagNotificationRuleConditionUpdateInput(BaseModel):
    id: str
    tags: List["TagCreateInput"]


class TimeRangeInput(BaseModel):
    end: Annotated[datetime, PlainSerializer(serialize_rfc3339_datetime)]
    start: Annotated[datetime, PlainSerializer(serialize_rfc3339_datetime)]


class TumblingWindowCreateInput(BaseModel):
    data_time_field: JsonPointer = Field(alias="dataTimeField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_size: int = Field(alias="windowSize")
    window_timeout_disabled: Optional[bool] = Field(
        alias="windowTimeoutDisabled", default=None
    )


class TumblingWindowUpdateInput(BaseModel):
    id: WindowId
    time_unit: Optional[WindowTimeUnit] = Field(alias="timeUnit", default=None)
    window_size: Optional[int] = Field(alias="windowSize", default=None)
    window_timeout_disabled: Optional[bool] = Field(
        alias="windowTimeoutDisabled", default=None
    )


class TypeNotificationRuleConditionCreateInput(BaseModel):
    notification_rule_id: Optional[Any] = Field(
        alias="notificationRuleId", default=None
    )
    types: List[IssueTypename]


class TypeNotificationRuleConditionUpdateInput(BaseModel):
    id: str
    types: List[IssueTypename]


class UserCreateInput(BaseModel):
    display_name: str = Field(alias="displayName")
    email: str
    full_name: Optional[str] = Field(alias="fullName", default=None)
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    password: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    role: Role
    status: UserStatus
    username: Optional[str] = None


class UserDeleteInput(BaseModel):
    id: str


class UserUpdateInput(BaseModel):
    display_name: str = Field(alias="displayName")
    email: Optional[str] = None
    full_name: Optional[str] = Field(alias="fullName", default=None)
    id: str
    password: Optional[str] = None
    role: Role
    status: UserStatus
    username: Optional[str] = None


class ValidatorMetricDebugInfoInput(BaseModel):
    incident_id: Any = Field(alias="incidentId")


class ValidatorRecommendationApplyInput(BaseModel):
    ids: List[Any]
    initialize_with_backfill: Optional[bool] = Field(
        alias="initializeWithBackfill", default=None
    )
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class ValidatorRecommendationDismissInput(BaseModel):
    ids: List[Any]


class ValidatorSegmentMetricsInput(BaseModel):
    segment_id: Any = Field(alias="segmentId")
    time_range: "TimeRangeInput" = Field(alias="timeRange")
    validator_id: ValidatorId = Field(alias="validatorId")


class ValidatorWithDifferenceThresholdUpdateInput(BaseModel):
    difference_type: Optional[DifferenceType] = Field(
        alias="differenceType", default=None
    )
    number_of_windows: Optional[int] = Field(alias="numberOfWindows", default=None)
    operator: Optional[DifferenceOperator] = None
    validator_id: ValidatorId = Field(alias="validatorId")
    value: Optional[float] = None


class ValidatorWithDynamicThresholdUpdateInput(BaseModel):
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType", default=None
    )
    sensitivity: float
    validator_id: ValidatorId = Field(alias="validatorId")


class ValidatorWithFixedThresholdUpdateInput(BaseModel):
    operator: ComparisonOperator
    validator_id: ValidatorId = Field(alias="validatorId")
    value: float


class VolumeValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: VolumeMetric
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: Optional[JsonPointer] = Field(alias="sourceField", default=None)
    source_fields: List[JsonPointer] = Field(alias="sourceFields")


class VolumeValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class WebhookChannelCreateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader", default=None)
    name: str
    namespace_id: Optional[str] = Field(alias="namespaceId", default=None)
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    webhook_url: str = Field(alias="webhookUrl")


class WebhookChannelUpdateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader", default=None)
    id: Any
    name: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


AwsKinesisInferSchemaInput.model_rebuild()
AwsKinesisSourceCreateInput.model_rebuild()
AwsKinesisSourceUpdateInput.model_rebuild()
AwsS3InferSchemaInput.model_rebuild()
AwsS3SourceCreateInput.model_rebuild()
AwsS3SourceUpdateInput.model_rebuild()
CategoricalDistributionValidatorCreateInput.model_rebuild()
CategoricalDistributionValidatorUpdateInput.model_rebuild()
FreshnessValidatorCreateInput.model_rebuild()
FreshnessValidatorUpdateInput.model_rebuild()
GcpPubSubInferSchemaInput.model_rebuild()
GcpPubSubLiteInferSchemaInput.model_rebuild()
GcpPubSubLiteSourceCreateInput.model_rebuild()
GcpPubSubLiteSourceUpdateInput.model_rebuild()
GcpPubSubSourceCreateInput.model_rebuild()
GcpPubSubSourceUpdateInput.model_rebuild()
GcpStorageInferSchemaInput.model_rebuild()
GcpStorageSourceCreateInput.model_rebuild()
GcpStorageSourceUpdateInput.model_rebuild()
IncidentGroupsFilter.model_rebuild()
IncidentGroupsSort.model_rebuild()
IncidentsFilter.model_rebuild()
IncidentsSort.model_rebuild()
KafkaInferSchemaInput.model_rebuild()
KafkaSourceCreateInput.model_rebuild()
KafkaSourceUpdateInput.model_rebuild()
NotificationRuleConditionCreateInput.model_rebuild()
NotificationRuleCreateInput.model_rebuild()
NotificationRuleUpdateInput.model_rebuild()
NumericAnomalyValidatorCreateInput.model_rebuild()
NumericAnomalyValidatorUpdateInput.model_rebuild()
NumericDistributionValidatorCreateInput.model_rebuild()
NumericDistributionValidatorUpdateInput.model_rebuild()
NumericValidatorCreateInput.model_rebuild()
NumericValidatorUpdateInput.model_rebuild()
PastIncidentGroupsFilter.model_rebuild()
RelativeTimeValidatorCreateInput.model_rebuild()
RelativeTimeValidatorUpdateInput.model_rebuild()
RelativeVolumeValidatorCreateInput.model_rebuild()
RelativeVolumeValidatorUpdateInput.model_rebuild()
SegmentNotificationRuleConditionCreateInput.model_rebuild()
SegmentNotificationRuleConditionUpdateInput.model_rebuild()
SqlValidatorCreateInput.model_rebuild()
TagNotificationRuleConditionCreateInput.model_rebuild()
TagNotificationRuleConditionUpdateInput.model_rebuild()
ValidatorSegmentMetricsInput.model_rebuild()
VolumeValidatorCreateInput.model_rebuild()
VolumeValidatorUpdateInput.model_rebuild()

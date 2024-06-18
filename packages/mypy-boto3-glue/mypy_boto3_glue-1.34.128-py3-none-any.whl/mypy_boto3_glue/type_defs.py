"""
Type annotations for glue service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/type_defs/)

Usage::

    ```python
    from mypy_boto3_glue.type_defs import NotificationPropertyTypeDef

    data: NotificationPropertyTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AdditionalOptionKeysType,
    AggFunctionType,
    AuthenticationTypeType,
    BackfillErrorCodeType,
    BlueprintRunStateType,
    BlueprintStatusType,
    CatalogEncryptionModeType,
    CloudWatchEncryptionModeType,
    ColumnStatisticsStateType,
    ColumnStatisticsTypeType,
    ComparatorType,
    CompatibilityType,
    CompressionTypeType,
    ConnectionPropertyKeyType,
    ConnectionStatusType,
    ConnectionTypeType,
    CrawlerHistoryStateType,
    CrawlerLineageSettingsType,
    CrawlerStateType,
    CrawlStateType,
    CsvHeaderOptionType,
    CsvSerdeOptionType,
    DataFormatType,
    DataQualityRuleResultStatusType,
    DeleteBehaviorType,
    DeltaTargetCompressionTypeType,
    DQCompositeRuleEvaluationMethodType,
    DQStopJobOnFailureTimingType,
    DQTransformOutputType,
    EnableHybridValuesType,
    ExecutionClassType,
    ExistConditionType,
    FieldNameType,
    FilterLogicalOperatorType,
    FilterOperationType,
    FilterOperatorType,
    FilterValueTypeType,
    GlueRecordTypeType,
    HudiTargetCompressionTypeType,
    JDBCConnectionTypeType,
    JDBCDataTypeType,
    JdbcMetadataEntryType,
    JobBookmarksEncryptionModeType,
    JobModeType,
    JobRunStateType,
    JoinTypeType,
    LanguageType,
    LastCrawlStatusType,
    LogicalType,
    MLUserDataEncryptionModeStringType,
    NodeTypeType,
    OAuth2GrantTypeType,
    ParamTypeType,
    ParquetCompressionTypeType,
    PartitionIndexStatusType,
    PermissionType,
    PermissionTypeType,
    PiiTypeType,
    PrincipalTypeType,
    QuoteCharType,
    RecrawlBehaviorType,
    RegistryStatusType,
    ResourceShareTypeType,
    ResourceTypeType,
    S3EncryptionModeType,
    ScheduleStateType,
    SchemaStatusType,
    SchemaVersionStatusType,
    SeparatorType,
    SessionStatusType,
    SortDirectionTypeType,
    SortType,
    SourceControlAuthStrategyType,
    SourceControlProviderType,
    StartingPositionType,
    StatementStateType,
    TableOptimizerEventTypeType,
    TargetFormatType,
    TaskRunSortColumnTypeType,
    TaskStatusTypeType,
    TaskTypeType,
    TransformSortColumnTypeType,
    TransformStatusTypeType,
    TriggerStateType,
    TriggerTypeType,
    UnionTypeType,
    UpdateBehaviorType,
    UpdateCatalogBehaviorType,
    ViewDialectType,
    ViewUpdateActionType,
    WorkerTypeType,
    WorkflowRunStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "NotificationPropertyTypeDef",
    "AggregateOperationExtraOutputTypeDef",
    "AggregateOperationOutputTypeDef",
    "AggregateOperationTypeDef",
    "AmazonRedshiftAdvancedOptionTypeDef",
    "OptionTypeDef",
    "ApplyMappingExtraOutputTypeDef",
    "ApplyMappingOutputTypeDef",
    "ApplyMappingTypeDef",
    "AuditContextTypeDef",
    "AuthorizationCodePropertiesTypeDef",
    "PartitionValueListOutputTypeDef",
    "BasicCatalogTargetExtraOutputTypeDef",
    "BasicCatalogTargetOutputTypeDef",
    "BasicCatalogTargetTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDeleteConnectionRequestRequestTypeDef",
    "ErrorDetailTypeDef",
    "BatchDeleteTableRequestRequestTypeDef",
    "BatchDeleteTableVersionRequestRequestTypeDef",
    "BatchGetBlueprintsRequestRequestTypeDef",
    "BatchGetCrawlersRequestRequestTypeDef",
    "BatchGetCustomEntityTypesRequestRequestTypeDef",
    "CustomEntityTypeTypeDef",
    "BatchGetDataQualityResultRequestRequestTypeDef",
    "BatchGetDevEndpointsRequestRequestTypeDef",
    "DevEndpointTypeDef",
    "BatchGetJobsRequestRequestTypeDef",
    "BatchGetTableOptimizerEntryTypeDef",
    "BatchGetTriggersRequestRequestTypeDef",
    "BatchGetWorkflowsRequestRequestTypeDef",
    "BatchStopJobRunRequestRequestTypeDef",
    "BatchStopJobRunSuccessfulSubmissionTypeDef",
    "BinaryColumnStatisticsDataTypeDef",
    "BlobTypeDef",
    "BlueprintDetailsTypeDef",
    "BlueprintRunTypeDef",
    "LastActiveDefinitionTypeDef",
    "BooleanColumnStatisticsDataTypeDef",
    "CancelDataQualityRuleRecommendationRunRequestRequestTypeDef",
    "CancelDataQualityRulesetEvaluationRunRequestRequestTypeDef",
    "CancelMLTaskRunRequestRequestTypeDef",
    "CancelStatementRequestRequestTypeDef",
    "CatalogEntryTypeDef",
    "CatalogImportStatusTypeDef",
    "KafkaStreamingSourceOptionsExtraOutputTypeDef",
    "StreamingDataPreviewOptionsTypeDef",
    "KafkaStreamingSourceOptionsOutputTypeDef",
    "KinesisStreamingSourceOptionsExtraOutputTypeDef",
    "KinesisStreamingSourceOptionsOutputTypeDef",
    "CatalogSchemaChangePolicyTypeDef",
    "CatalogSourceTypeDef",
    "CatalogTargetExtraOutputTypeDef",
    "CatalogTargetOutputTypeDef",
    "CatalogTargetTypeDef",
    "CheckSchemaVersionValidityInputRequestTypeDef",
    "CsvClassifierTypeDef",
    "GrokClassifierTypeDef",
    "JsonClassifierTypeDef",
    "XMLClassifierTypeDef",
    "CloudWatchEncryptionTypeDef",
    "ConnectorDataTargetExtraOutputTypeDef",
    "DirectJDBCSourceTypeDef",
    "DropDuplicatesExtraOutputTypeDef",
    "DropFieldsExtraOutputTypeDef",
    "DynamoDBCatalogSourceTypeDef",
    "FillMissingValuesExtraOutputTypeDef",
    "MergeExtraOutputTypeDef",
    "MicrosoftSQLServerCatalogSourceTypeDef",
    "MicrosoftSQLServerCatalogTargetExtraOutputTypeDef",
    "MySQLCatalogSourceTypeDef",
    "MySQLCatalogTargetExtraOutputTypeDef",
    "OracleSQLCatalogSourceTypeDef",
    "OracleSQLCatalogTargetExtraOutputTypeDef",
    "PIIDetectionExtraOutputTypeDef",
    "PostgreSQLCatalogSourceTypeDef",
    "PostgreSQLCatalogTargetExtraOutputTypeDef",
    "RedshiftSourceTypeDef",
    "RelationalCatalogSourceTypeDef",
    "RenameFieldExtraOutputTypeDef",
    "SelectFieldsExtraOutputTypeDef",
    "SelectFromCollectionExtraOutputTypeDef",
    "SpigotExtraOutputTypeDef",
    "SplitFieldsExtraOutputTypeDef",
    "UnionExtraOutputTypeDef",
    "ConnectorDataTargetOutputTypeDef",
    "DropDuplicatesOutputTypeDef",
    "DropFieldsOutputTypeDef",
    "FillMissingValuesOutputTypeDef",
    "MergeOutputTypeDef",
    "MicrosoftSQLServerCatalogTargetOutputTypeDef",
    "MySQLCatalogTargetOutputTypeDef",
    "OracleSQLCatalogTargetOutputTypeDef",
    "PIIDetectionOutputTypeDef",
    "PostgreSQLCatalogTargetOutputTypeDef",
    "RenameFieldOutputTypeDef",
    "SelectFieldsOutputTypeDef",
    "SelectFromCollectionOutputTypeDef",
    "SpigotOutputTypeDef",
    "SplitFieldsOutputTypeDef",
    "UnionOutputTypeDef",
    "ConnectorDataTargetTypeDef",
    "DropDuplicatesTypeDef",
    "DropFieldsTypeDef",
    "FillMissingValuesTypeDef",
    "MergeTypeDef",
    "MicrosoftSQLServerCatalogTargetTypeDef",
    "MySQLCatalogTargetTypeDef",
    "OracleSQLCatalogTargetTypeDef",
    "PIIDetectionTypeDef",
    "PostgreSQLCatalogTargetTypeDef",
    "RenameFieldTypeDef",
    "SelectFieldsTypeDef",
    "SelectFromCollectionTypeDef",
    "SpigotTypeDef",
    "SplitFieldsTypeDef",
    "UnionTypeDef",
    "CodeGenEdgeTypeDef",
    "CodeGenNodeArgTypeDef",
    "ColumnImportanceTypeDef",
    "ColumnOutputTypeDef",
    "ColumnRowFilterTypeDef",
    "DateColumnStatisticsDataOutputTypeDef",
    "DoubleColumnStatisticsDataTypeDef",
    "LongColumnStatisticsDataTypeDef",
    "StringColumnStatisticsDataTypeDef",
    "ColumnStatisticsTaskRunTypeDef",
    "TimestampTypeDef",
    "ColumnTypeDef",
    "ConditionTypeDef",
    "ConfigurationObjectOutputTypeDef",
    "ConfigurationObjectTypeDef",
    "ConfusionMatrixTypeDef",
    "PhysicalConnectionRequirementsTypeDef",
    "ConnectionPasswordEncryptionTypeDef",
    "PhysicalConnectionRequirementsOutputTypeDef",
    "ConnectionsListExtraOutputTypeDef",
    "ConnectionsListOutputTypeDef",
    "ConnectionsListTypeDef",
    "CrawlTypeDef",
    "CrawlerHistoryTypeDef",
    "CrawlerMetricsTypeDef",
    "DeltaTargetExtraOutputTypeDef",
    "DynamoDBTargetTypeDef",
    "HudiTargetExtraOutputTypeDef",
    "IcebergTargetExtraOutputTypeDef",
    "JdbcTargetExtraOutputTypeDef",
    "MongoDBTargetTypeDef",
    "S3TargetExtraOutputTypeDef",
    "DeltaTargetOutputTypeDef",
    "HudiTargetOutputTypeDef",
    "IcebergTargetOutputTypeDef",
    "JdbcTargetOutputTypeDef",
    "S3TargetOutputTypeDef",
    "DeltaTargetTypeDef",
    "HudiTargetTypeDef",
    "IcebergTargetTypeDef",
    "JdbcTargetTypeDef",
    "S3TargetTypeDef",
    "LakeFormationConfigurationTypeDef",
    "LastCrawlInfoTypeDef",
    "LineageConfigurationTypeDef",
    "RecrawlPolicyTypeDef",
    "ScheduleTypeDef",
    "SchemaChangePolicyTypeDef",
    "CrawlsFilterTypeDef",
    "CreateBlueprintRequestRequestTypeDef",
    "CreateCsvClassifierRequestTypeDef",
    "CreateGrokClassifierRequestTypeDef",
    "CreateJsonClassifierRequestTypeDef",
    "CreateXMLClassifierRequestTypeDef",
    "CreateCustomEntityTypeRequestRequestTypeDef",
    "DataQualityTargetTableTypeDef",
    "CreateDevEndpointRequestRequestTypeDef",
    "ExecutionPropertyTypeDef",
    "JobCommandTypeDef",
    "SourceControlDetailsTypeDef",
    "PartitionIndexTypeDef",
    "CreateRegistryInputRequestTypeDef",
    "RegistryIdTypeDef",
    "SessionCommandTypeDef",
    "TableOptimizerConfigurationTypeDef",
    "EventBatchingConditionTypeDef",
    "CreateWorkflowRequestRequestTypeDef",
    "DQResultsPublishingOptionsTypeDef",
    "DQStopJobOnFailureOptionsTypeDef",
    "EncryptionAtRestTypeDef",
    "DataLakePrincipalTypeDef",
    "DataQualityAnalyzerResultTypeDef",
    "DataQualityEvaluationRunAdditionalRunOptionsTypeDef",
    "DataQualityMetricValuesTypeDef",
    "DataQualityRuleResultTypeDef",
    "GlueTableOutputTypeDef",
    "GlueTableTypeDef",
    "DatabaseIdentifierTypeDef",
    "FederatedDatabaseTypeDef",
    "DatatypeTypeDef",
    "DecimalNumberOutputTypeDef",
    "DeleteBlueprintRequestRequestTypeDef",
    "DeleteClassifierRequestRequestTypeDef",
    "DeleteColumnStatisticsForPartitionRequestRequestTypeDef",
    "DeleteColumnStatisticsForTableRequestRequestTypeDef",
    "DeleteConnectionRequestRequestTypeDef",
    "DeleteCrawlerRequestRequestTypeDef",
    "DeleteCustomEntityTypeRequestRequestTypeDef",
    "DeleteDataQualityRulesetRequestRequestTypeDef",
    "DeleteDatabaseRequestRequestTypeDef",
    "DeleteDevEndpointRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteMLTransformRequestRequestTypeDef",
    "DeletePartitionIndexRequestRequestTypeDef",
    "DeletePartitionRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "SchemaIdTypeDef",
    "DeleteSecurityConfigurationRequestRequestTypeDef",
    "DeleteSessionRequestRequestTypeDef",
    "DeleteTableOptimizerRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "DeleteTableVersionRequestRequestTypeDef",
    "DeleteTriggerRequestRequestTypeDef",
    "DeleteUsageProfileRequestRequestTypeDef",
    "DeleteUserDefinedFunctionRequestRequestTypeDef",
    "DeleteWorkflowRequestRequestTypeDef",
    "DevEndpointCustomLibrariesTypeDef",
    "DirectSchemaChangePolicyTypeDef",
    "NullCheckBoxListTypeDef",
    "TransformConfigParameterExtraOutputTypeDef",
    "TransformConfigParameterOutputTypeDef",
    "TransformConfigParameterTypeDef",
    "EdgeTypeDef",
    "JobBookmarksEncryptionTypeDef",
    "S3EncryptionTypeDef",
    "ErrorDetailsTypeDef",
    "ExportLabelsTaskRunPropertiesTypeDef",
    "FederatedTableTypeDef",
    "FilterValueExtraOutputTypeDef",
    "FilterValueOutputTypeDef",
    "FilterValueTypeDef",
    "FindMatchesParametersTypeDef",
    "FindMatchesTaskRunPropertiesTypeDef",
    "GetBlueprintRequestRequestTypeDef",
    "GetBlueprintRunRequestRequestTypeDef",
    "GetBlueprintRunsRequestRequestTypeDef",
    "GetCatalogImportStatusRequestRequestTypeDef",
    "GetClassifierRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetClassifiersRequestRequestTypeDef",
    "GetColumnStatisticsForPartitionRequestRequestTypeDef",
    "GetColumnStatisticsForTableRequestRequestTypeDef",
    "GetColumnStatisticsTaskRunRequestRequestTypeDef",
    "GetColumnStatisticsTaskRunsRequestRequestTypeDef",
    "GetConnectionRequestRequestTypeDef",
    "GetConnectionsFilterTypeDef",
    "GetCrawlerMetricsRequestRequestTypeDef",
    "GetCrawlerRequestRequestTypeDef",
    "GetCrawlersRequestRequestTypeDef",
    "GetCustomEntityTypeRequestRequestTypeDef",
    "GetDataCatalogEncryptionSettingsRequestRequestTypeDef",
    "GetDataQualityResultRequestRequestTypeDef",
    "GetDataQualityRuleRecommendationRunRequestRequestTypeDef",
    "GetDataQualityRulesetEvaluationRunRequestRequestTypeDef",
    "GetDataQualityRulesetRequestRequestTypeDef",
    "GetDatabaseRequestRequestTypeDef",
    "GetDatabasesRequestRequestTypeDef",
    "GetDataflowGraphRequestRequestTypeDef",
    "GetDevEndpointRequestRequestTypeDef",
    "GetDevEndpointsRequestRequestTypeDef",
    "GetJobBookmarkRequestRequestTypeDef",
    "JobBookmarkEntryTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobRunRequestRequestTypeDef",
    "GetJobRunsRequestRequestTypeDef",
    "GetJobsRequestRequestTypeDef",
    "GetMLTaskRunRequestRequestTypeDef",
    "TaskRunSortCriteriaTypeDef",
    "GetMLTransformRequestRequestTypeDef",
    "SchemaColumnTypeDef",
    "TransformSortCriteriaTypeDef",
    "MappingEntryTypeDef",
    "GetPartitionIndexesRequestRequestTypeDef",
    "GetPartitionRequestRequestTypeDef",
    "SegmentTypeDef",
    "GetResourcePoliciesRequestRequestTypeDef",
    "GluePolicyTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "SchemaVersionNumberTypeDef",
    "GetSecurityConfigurationRequestRequestTypeDef",
    "GetSecurityConfigurationsRequestRequestTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetStatementRequestRequestTypeDef",
    "GetTableOptimizerRequestRequestTypeDef",
    "GetTableVersionRequestRequestTypeDef",
    "GetTableVersionsRequestRequestTypeDef",
    "GetTagsRequestRequestTypeDef",
    "GetTriggerRequestRequestTypeDef",
    "GetTriggersRequestRequestTypeDef",
    "SupportedDialectTypeDef",
    "GetUsageProfileRequestRequestTypeDef",
    "GetUserDefinedFunctionRequestRequestTypeDef",
    "GetUserDefinedFunctionsRequestRequestTypeDef",
    "GetWorkflowRequestRequestTypeDef",
    "GetWorkflowRunPropertiesRequestRequestTypeDef",
    "GetWorkflowRunRequestRequestTypeDef",
    "GetWorkflowRunsRequestRequestTypeDef",
    "GlueStudioSchemaColumnTypeDef",
    "S3SourceAdditionalOptionsTypeDef",
    "IcebergInputTypeDef",
    "ImportCatalogToGlueRequestRequestTypeDef",
    "ImportLabelsTaskRunPropertiesTypeDef",
    "JDBCConnectorOptionsExtraOutputTypeDef",
    "JDBCConnectorOptionsOutputTypeDef",
    "JDBCConnectorOptionsTypeDef",
    "PredecessorTypeDef",
    "JoinColumnExtraOutputTypeDef",
    "JoinColumnOutputTypeDef",
    "JoinColumnTypeDef",
    "KeySchemaElementTypeDef",
    "LabelingSetGenerationTaskRunPropertiesTypeDef",
    "ListBlueprintsRequestRequestTypeDef",
    "ListColumnStatisticsTaskRunsRequestRequestTypeDef",
    "ListCrawlersRequestRequestTypeDef",
    "ListCustomEntityTypesRequestRequestTypeDef",
    "ListDevEndpointsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListRegistriesInputRequestTypeDef",
    "RegistryListItemTypeDef",
    "SchemaVersionListItemTypeDef",
    "SchemaListItemTypeDef",
    "ListSessionsRequestRequestTypeDef",
    "ListStatementsRequestRequestTypeDef",
    "ListTableOptimizerRunsRequestRequestTypeDef",
    "ListTriggersRequestRequestTypeDef",
    "ListUsageProfilesRequestRequestTypeDef",
    "UsageProfileDefinitionTypeDef",
    "ListWorkflowsRequestRequestTypeDef",
    "MLUserDataEncryptionTypeDef",
    "MappingExtraOutputTypeDef",
    "MappingOutputTypeDef",
    "MappingTypeDef",
    "OtherMetadataValueListItemTypeDef",
    "MetadataKeyValuePairTypeDef",
    "OAuth2ClientApplicationTypeDef",
    "OrderTypeDef",
    "PartitionValueListExtraOutputTypeDef",
    "PartitionValueListTypeDef",
    "PropertyPredicateTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutWorkflowRunPropertiesRequestRequestTypeDef",
    "RecipeReferenceTypeDef",
    "UpsertRedshiftTargetOptionsExtraOutputTypeDef",
    "UpsertRedshiftTargetOptionsOutputTypeDef",
    "UpsertRedshiftTargetOptionsTypeDef",
    "ResetJobBookmarkRequestRequestTypeDef",
    "ResourceUriTypeDef",
    "ResumeWorkflowRunRequestRequestTypeDef",
    "RunMetricsTypeDef",
    "RunStatementRequestRequestTypeDef",
    "S3DirectSourceAdditionalOptionsTypeDef",
    "SortCriterionTypeDef",
    "SerDeInfoOutputTypeDef",
    "SerDeInfoTypeDef",
    "SkewedInfoOutputTypeDef",
    "SkewedInfoTypeDef",
    "SqlAliasTypeDef",
    "StartBlueprintRunRequestRequestTypeDef",
    "StartColumnStatisticsTaskRunRequestRequestTypeDef",
    "StartCrawlerRequestRequestTypeDef",
    "StartCrawlerScheduleRequestRequestTypeDef",
    "StartExportLabelsTaskRunRequestRequestTypeDef",
    "StartImportLabelsTaskRunRequestRequestTypeDef",
    "StartMLEvaluationTaskRunRequestRequestTypeDef",
    "StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef",
    "StartTriggerRequestRequestTypeDef",
    "StartWorkflowRunRequestRequestTypeDef",
    "StartingEventBatchConditionTypeDef",
    "StatementOutputDataTypeDef",
    "StopColumnStatisticsTaskRunRequestRequestTypeDef",
    "StopCrawlerRequestRequestTypeDef",
    "StopCrawlerScheduleRequestRequestTypeDef",
    "StopSessionRequestRequestTypeDef",
    "StopTriggerRequestRequestTypeDef",
    "StopWorkflowRunRequestRequestTypeDef",
    "TableIdentifierTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBlueprintRequestRequestTypeDef",
    "UpdateCsvClassifierRequestTypeDef",
    "UpdateGrokClassifierRequestTypeDef",
    "UpdateJsonClassifierRequestTypeDef",
    "UpdateXMLClassifierRequestTypeDef",
    "UpdateCrawlerScheduleRequestRequestTypeDef",
    "UpdateDataQualityRulesetRequestRequestTypeDef",
    "UpdateJobFromSourceControlRequestRequestTypeDef",
    "UpdateSourceControlFromJobRequestRequestTypeDef",
    "UpdateWorkflowRequestRequestTypeDef",
    "ViewRepresentationInputTypeDef",
    "ViewRepresentationTypeDef",
    "WorkflowRunStatisticsTypeDef",
    "ActionExtraOutputTypeDef",
    "ActionOutputTypeDef",
    "ActionTypeDef",
    "StartJobRunRequestRequestTypeDef",
    "AggregateExtraOutputTypeDef",
    "AggregateOutputTypeDef",
    "AggregateTypeDef",
    "AmazonRedshiftNodeDataExtraOutputTypeDef",
    "AmazonRedshiftNodeDataOutputTypeDef",
    "AmazonRedshiftNodeDataTypeDef",
    "SnowflakeNodeDataExtraOutputTypeDef",
    "SnowflakeNodeDataOutputTypeDef",
    "SnowflakeNodeDataTypeDef",
    "BackfillErrorTypeDef",
    "CancelMLTaskRunResponseTypeDef",
    "CheckSchemaVersionValidityResponseTypeDef",
    "CreateBlueprintResponseTypeDef",
    "CreateConnectionResponseTypeDef",
    "CreateCustomEntityTypeResponseTypeDef",
    "CreateDataQualityRulesetResponseTypeDef",
    "CreateDevEndpointResponseTypeDef",
    "CreateJobResponseTypeDef",
    "CreateMLTransformResponseTypeDef",
    "CreateRegistryResponseTypeDef",
    "CreateSchemaResponseTypeDef",
    "CreateScriptResponseTypeDef",
    "CreateSecurityConfigurationResponseTypeDef",
    "CreateTriggerResponseTypeDef",
    "CreateUsageProfileResponseTypeDef",
    "CreateWorkflowResponseTypeDef",
    "DeleteBlueprintResponseTypeDef",
    "DeleteCustomEntityTypeResponseTypeDef",
    "DeleteJobResponseTypeDef",
    "DeleteMLTransformResponseTypeDef",
    "DeleteRegistryResponseTypeDef",
    "DeleteSchemaResponseTypeDef",
    "DeleteSessionResponseTypeDef",
    "DeleteTriggerResponseTypeDef",
    "DeleteWorkflowResponseTypeDef",
    "GetCustomEntityTypeResponseTypeDef",
    "GetPlanResponseTypeDef",
    "GetRegistryResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetSchemaByDefinitionResponseTypeDef",
    "GetSchemaResponseTypeDef",
    "GetSchemaVersionResponseTypeDef",
    "GetSchemaVersionsDiffResponseTypeDef",
    "GetTagsResponseTypeDef",
    "GetWorkflowRunPropertiesResponseTypeDef",
    "ListBlueprintsResponseTypeDef",
    "ListColumnStatisticsTaskRunsResponseTypeDef",
    "ListCrawlersResponseTypeDef",
    "ListDevEndpointsResponseTypeDef",
    "ListJobsResponseTypeDef",
    "ListMLTransformsResponseTypeDef",
    "ListTriggersResponseTypeDef",
    "ListWorkflowsResponseTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "PutSchemaVersionMetadataResponseTypeDef",
    "RegisterSchemaVersionResponseTypeDef",
    "RemoveSchemaVersionMetadataResponseTypeDef",
    "ResumeWorkflowRunResponseTypeDef",
    "RunStatementResponseTypeDef",
    "StartBlueprintRunResponseTypeDef",
    "StartColumnStatisticsTaskRunResponseTypeDef",
    "StartDataQualityRuleRecommendationRunResponseTypeDef",
    "StartDataQualityRulesetEvaluationRunResponseTypeDef",
    "StartExportLabelsTaskRunResponseTypeDef",
    "StartImportLabelsTaskRunResponseTypeDef",
    "StartJobRunResponseTypeDef",
    "StartMLEvaluationTaskRunResponseTypeDef",
    "StartMLLabelingSetGenerationTaskRunResponseTypeDef",
    "StartTriggerResponseTypeDef",
    "StartWorkflowRunResponseTypeDef",
    "StopSessionResponseTypeDef",
    "StopTriggerResponseTypeDef",
    "UpdateBlueprintResponseTypeDef",
    "UpdateDataQualityRulesetResponseTypeDef",
    "UpdateJobFromSourceControlResponseTypeDef",
    "UpdateJobResponseTypeDef",
    "UpdateMLTransformResponseTypeDef",
    "UpdateRegistryResponseTypeDef",
    "UpdateSchemaResponseTypeDef",
    "UpdateSourceControlFromJobResponseTypeDef",
    "UpdateUsageProfileResponseTypeDef",
    "UpdateWorkflowResponseTypeDef",
    "BatchDeleteConnectionResponseTypeDef",
    "BatchGetTableOptimizerErrorTypeDef",
    "BatchStopJobRunErrorTypeDef",
    "BatchUpdatePartitionFailureEntryTypeDef",
    "ColumnErrorTypeDef",
    "PartitionErrorTypeDef",
    "TableErrorTypeDef",
    "TableVersionErrorTypeDef",
    "BatchGetCustomEntityTypesResponseTypeDef",
    "ListCustomEntityTypesResponseTypeDef",
    "BatchGetDevEndpointsResponseTypeDef",
    "GetDevEndpointResponseTypeDef",
    "GetDevEndpointsResponseTypeDef",
    "BatchGetTableOptimizerRequestRequestTypeDef",
    "DecimalNumberTypeDef",
    "GetBlueprintRunResponseTypeDef",
    "GetBlueprintRunsResponseTypeDef",
    "BlueprintTypeDef",
    "GetCatalogImportStatusResponseTypeDef",
    "CatalogKafkaSourceExtraOutputTypeDef",
    "DirectKafkaSourceExtraOutputTypeDef",
    "CatalogKafkaSourceOutputTypeDef",
    "DirectKafkaSourceOutputTypeDef",
    "CatalogKinesisSourceExtraOutputTypeDef",
    "DirectKinesisSourceExtraOutputTypeDef",
    "CatalogKinesisSourceOutputTypeDef",
    "DirectKinesisSourceOutputTypeDef",
    "GovernedCatalogTargetExtraOutputTypeDef",
    "GovernedCatalogTargetOutputTypeDef",
    "GovernedCatalogTargetTypeDef",
    "S3CatalogTargetExtraOutputTypeDef",
    "S3CatalogTargetOutputTypeDef",
    "S3CatalogTargetTypeDef",
    "S3DeltaCatalogTargetExtraOutputTypeDef",
    "S3DeltaCatalogTargetOutputTypeDef",
    "S3DeltaCatalogTargetTypeDef",
    "S3HudiCatalogTargetExtraOutputTypeDef",
    "S3HudiCatalogTargetOutputTypeDef",
    "S3HudiCatalogTargetTypeDef",
    "ClassifierTypeDef",
    "CodeGenNodeOutputTypeDef",
    "CodeGenNodeTypeDef",
    "LocationTypeDef",
    "GetColumnStatisticsTaskRunResponseTypeDef",
    "GetColumnStatisticsTaskRunsResponseTypeDef",
    "DateColumnStatisticsDataTypeDef",
    "GetTableRequestRequestTypeDef",
    "GetTablesRequestRequestTypeDef",
    "KafkaStreamingSourceOptionsTypeDef",
    "KinesisStreamingSourceOptionsTypeDef",
    "QuerySessionContextTypeDef",
    "TaskRunFilterCriteriaTypeDef",
    "PredicateExtraOutputTypeDef",
    "PredicateOutputTypeDef",
    "PredicateTypeDef",
    "ProfileConfigurationOutputTypeDef",
    "ProfileConfigurationTypeDef",
    "FindMatchesMetricsTypeDef",
    "ConnectionsListUnionTypeDef",
    "CrawlerNodeDetailsTypeDef",
    "ListCrawlsResponseTypeDef",
    "GetCrawlerMetricsResponseTypeDef",
    "CrawlerTargetsExtraOutputTypeDef",
    "CrawlerTargetsOutputTypeDef",
    "CrawlerTargetsTypeDef",
    "ListCrawlsRequestRequestTypeDef",
    "CreateClassifierRequestRequestTypeDef",
    "CreateDataQualityRulesetRequestRequestTypeDef",
    "DataQualityRulesetFilterCriteriaTypeDef",
    "DataQualityRulesetListDetailsTypeDef",
    "GetDataQualityRulesetResponseTypeDef",
    "CreatePartitionIndexRequestRequestTypeDef",
    "CreateSchemaInputRequestTypeDef",
    "DeleteRegistryInputRequestTypeDef",
    "GetRegistryInputRequestTypeDef",
    "ListSchemasInputRequestTypeDef",
    "UpdateRegistryInputRequestTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "SessionTypeDef",
    "CreateTableOptimizerRequestRequestTypeDef",
    "UpdateTableOptimizerRequestRequestTypeDef",
    "EvaluateDataQualityExtraOutputTypeDef",
    "EvaluateDataQualityMultiFrameExtraOutputTypeDef",
    "EvaluateDataQualityMultiFrameOutputTypeDef",
    "EvaluateDataQualityMultiFrameTypeDef",
    "EvaluateDataQualityOutputTypeDef",
    "EvaluateDataQualityTypeDef",
    "DataCatalogEncryptionSettingsTypeDef",
    "PrincipalPermissionsOutputTypeDef",
    "PrincipalPermissionsTypeDef",
    "MetricBasedObservationTypeDef",
    "DataSourceOutputTypeDef",
    "DataSourceTypeDef",
    "GlueTableUnionTypeDef",
    "NullValueFieldTypeDef",
    "DecimalColumnStatisticsDataOutputTypeDef",
    "DeleteSchemaInputRequestTypeDef",
    "DeleteSchemaVersionsInputRequestTypeDef",
    "GetSchemaByDefinitionInputRequestTypeDef",
    "GetSchemaInputRequestTypeDef",
    "ListSchemaVersionsInputRequestTypeDef",
    "RegisterSchemaVersionInputRequestTypeDef",
    "SchemaReferenceTypeDef",
    "UpdateDevEndpointRequestRequestTypeDef",
    "S3DeltaDirectTargetExtraOutputTypeDef",
    "S3DeltaDirectTargetOutputTypeDef",
    "S3DeltaDirectTargetTypeDef",
    "S3DirectTargetExtraOutputTypeDef",
    "S3DirectTargetOutputTypeDef",
    "S3DirectTargetTypeDef",
    "S3GlueParquetTargetExtraOutputTypeDef",
    "S3GlueParquetTargetOutputTypeDef",
    "S3GlueParquetTargetTypeDef",
    "S3HudiDirectTargetExtraOutputTypeDef",
    "S3HudiDirectTargetOutputTypeDef",
    "S3HudiDirectTargetTypeDef",
    "EncryptionConfigurationExtraOutputTypeDef",
    "EncryptionConfigurationOutputTypeDef",
    "EncryptionConfigurationTypeDef",
    "SchemaVersionErrorItemTypeDef",
    "FilterExpressionExtraOutputTypeDef",
    "FilterExpressionOutputTypeDef",
    "FilterExpressionTypeDef",
    "TransformParametersTypeDef",
    "GetClassifiersRequestGetClassifiersPaginateTypeDef",
    "GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef",
    "GetCrawlersRequestGetCrawlersPaginateTypeDef",
    "GetDatabasesRequestGetDatabasesPaginateTypeDef",
    "GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef",
    "GetJobRunsRequestGetJobRunsPaginateTypeDef",
    "GetJobsRequestGetJobsPaginateTypeDef",
    "GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef",
    "GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    "GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef",
    "GetTableVersionsRequestGetTableVersionsPaginateTypeDef",
    "GetTablesRequestGetTablesPaginateTypeDef",
    "GetTriggersRequestGetTriggersPaginateTypeDef",
    "GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef",
    "ListRegistriesInputListRegistriesPaginateTypeDef",
    "ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef",
    "ListSchemasInputListSchemasPaginateTypeDef",
    "ListUsageProfilesRequestListUsageProfilesPaginateTypeDef",
    "GetConnectionsRequestGetConnectionsPaginateTypeDef",
    "GetConnectionsRequestRequestTypeDef",
    "GetJobBookmarkResponseTypeDef",
    "ResetJobBookmarkResponseTypeDef",
    "TransformFilterCriteriaTypeDef",
    "GetMappingResponseTypeDef",
    "GetPartitionsRequestGetPartitionsPaginateTypeDef",
    "GetPartitionsRequestRequestTypeDef",
    "GetResourcePoliciesResponseTypeDef",
    "GetSchemaVersionInputRequestTypeDef",
    "GetSchemaVersionsDiffInputRequestTypeDef",
    "UpdateSchemaInputRequestTypeDef",
    "GlueSchemaExtraOutputTypeDef",
    "GlueSchemaOutputTypeDef",
    "GlueSchemaTypeDef",
    "GovernedCatalogSourceTypeDef",
    "S3CatalogSourceTypeDef",
    "OpenTableFormatInputTypeDef",
    "JobRunTypeDef",
    "JoinExtraOutputTypeDef",
    "JoinOutputTypeDef",
    "JoinTypeDef",
    "TaskRunPropertiesTypeDef",
    "ListRegistriesResponseTypeDef",
    "ListSchemaVersionsResponseTypeDef",
    "ListSchemasResponseTypeDef",
    "ListUsageProfilesResponseTypeDef",
    "TransformEncryptionTypeDef",
    "MetadataInfoTypeDef",
    "PutSchemaVersionMetadataInputRequestTypeDef",
    "QuerySchemaVersionMetadataInputRequestTypeDef",
    "RemoveSchemaVersionMetadataInputRequestTypeDef",
    "OAuth2PropertiesInputTypeDef",
    "OAuth2PropertiesTypeDef",
    "PartitionValueListUnionTypeDef",
    "RecipeExtraOutputTypeDef",
    "RecipeOutputTypeDef",
    "RecipeTypeDef",
    "RedshiftTargetExtraOutputTypeDef",
    "RedshiftTargetOutputTypeDef",
    "RedshiftTargetTypeDef",
    "UserDefinedFunctionInputTypeDef",
    "UserDefinedFunctionTypeDef",
    "TableOptimizerRunTypeDef",
    "SearchTablesRequestRequestTypeDef",
    "StatementOutputTypeDef",
    "UpdateClassifierRequestRequestTypeDef",
    "ViewDefinitionInputTypeDef",
    "ViewDefinitionTypeDef",
    "ActionUnionTypeDef",
    "AmazonRedshiftSourceExtraOutputTypeDef",
    "AmazonRedshiftTargetExtraOutputTypeDef",
    "AmazonRedshiftSourceOutputTypeDef",
    "AmazonRedshiftTargetOutputTypeDef",
    "AmazonRedshiftSourceTypeDef",
    "AmazonRedshiftTargetTypeDef",
    "SnowflakeTargetExtraOutputTypeDef",
    "SnowflakeTargetOutputTypeDef",
    "SnowflakeTargetTypeDef",
    "PartitionIndexDescriptorTypeDef",
    "BatchStopJobRunResponseTypeDef",
    "BatchUpdatePartitionResponseTypeDef",
    "BatchCreatePartitionResponseTypeDef",
    "BatchDeletePartitionResponseTypeDef",
    "BatchDeleteTableResponseTypeDef",
    "BatchDeleteTableVersionResponseTypeDef",
    "DecimalColumnStatisticsDataTypeDef",
    "BatchGetBlueprintsResponseTypeDef",
    "GetBlueprintResponseTypeDef",
    "GetClassifierResponseTypeDef",
    "GetClassifiersResponseTypeDef",
    "GetDataflowGraphResponseTypeDef",
    "CodeGenNodeUnionTypeDef",
    "GetMappingRequestRequestTypeDef",
    "GetPlanRequestRequestTypeDef",
    "CatalogKafkaSourceTypeDef",
    "DirectKafkaSourceTypeDef",
    "CatalogKinesisSourceTypeDef",
    "DirectKinesisSourceTypeDef",
    "GetUnfilteredPartitionMetadataRequestRequestTypeDef",
    "GetUnfilteredPartitionsMetadataRequestRequestTypeDef",
    "GetUnfilteredTableMetadataRequestRequestTypeDef",
    "GetMLTaskRunsRequestRequestTypeDef",
    "TriggerTypeDef",
    "PredicateUnionTypeDef",
    "TriggerUpdateTypeDef",
    "GetUsageProfileResponseTypeDef",
    "CreateUsageProfileRequestRequestTypeDef",
    "ProfileConfigurationUnionTypeDef",
    "UpdateUsageProfileRequestRequestTypeDef",
    "EvaluationMetricsTypeDef",
    "CrawlerTypeDef",
    "CrawlerTargetsUnionTypeDef",
    "CreateCrawlerRequestRequestTypeDef",
    "UpdateCrawlerRequestRequestTypeDef",
    "ListDataQualityRulesetsRequestRequestTypeDef",
    "ListDataQualityRulesetsResponseTypeDef",
    "CreateSessionResponseTypeDef",
    "GetSessionResponseTypeDef",
    "ListSessionsResponseTypeDef",
    "GetDataCatalogEncryptionSettingsResponseTypeDef",
    "PutDataCatalogEncryptionSettingsRequestRequestTypeDef",
    "DatabaseTypeDef",
    "DatabaseInputTypeDef",
    "DataQualityObservationTypeDef",
    "DataQualityResultDescriptionTypeDef",
    "DataQualityRuleRecommendationRunDescriptionTypeDef",
    "DataQualityRulesetEvaluationRunDescriptionTypeDef",
    "GetDataQualityRuleRecommendationRunResponseTypeDef",
    "GetDataQualityRulesetEvaluationRunResponseTypeDef",
    "DataQualityResultFilterCriteriaTypeDef",
    "DataQualityRuleRecommendationRunFilterTypeDef",
    "DataQualityRulesetEvaluationRunFilterTypeDef",
    "DataSourceUnionTypeDef",
    "StartDataQualityRuleRecommendationRunRequestRequestTypeDef",
    "DropNullFieldsExtraOutputTypeDef",
    "DropNullFieldsOutputTypeDef",
    "DropNullFieldsTypeDef",
    "ColumnStatisticsDataOutputTypeDef",
    "StorageDescriptorOutputTypeDef",
    "StorageDescriptorTypeDef",
    "SecurityConfigurationTypeDef",
    "CreateSecurityConfigurationRequestRequestTypeDef",
    "EncryptionConfigurationUnionTypeDef",
    "DeleteSchemaVersionsResponseTypeDef",
    "FilterExtraOutputTypeDef",
    "FilterOutputTypeDef",
    "FilterTypeDef",
    "UpdateMLTransformRequestRequestTypeDef",
    "GetMLTransformsRequestRequestTypeDef",
    "ListMLTransformsRequestRequestTypeDef",
    "AthenaConnectorSourceExtraOutputTypeDef",
    "CatalogDeltaSourceExtraOutputTypeDef",
    "CatalogHudiSourceExtraOutputTypeDef",
    "ConnectorDataSourceExtraOutputTypeDef",
    "CustomCodeExtraOutputTypeDef",
    "DynamicTransformExtraOutputTypeDef",
    "JDBCConnectorSourceExtraOutputTypeDef",
    "JDBCConnectorTargetExtraOutputTypeDef",
    "S3CatalogDeltaSourceExtraOutputTypeDef",
    "S3CatalogHudiSourceExtraOutputTypeDef",
    "S3CsvSourceExtraOutputTypeDef",
    "S3DeltaSourceExtraOutputTypeDef",
    "S3HudiSourceExtraOutputTypeDef",
    "S3JsonSourceExtraOutputTypeDef",
    "S3ParquetSourceExtraOutputTypeDef",
    "SnowflakeSourceExtraOutputTypeDef",
    "SparkConnectorSourceExtraOutputTypeDef",
    "SparkConnectorTargetExtraOutputTypeDef",
    "SparkSQLExtraOutputTypeDef",
    "AthenaConnectorSourceOutputTypeDef",
    "CatalogDeltaSourceOutputTypeDef",
    "CatalogHudiSourceOutputTypeDef",
    "ConnectorDataSourceOutputTypeDef",
    "CustomCodeOutputTypeDef",
    "DynamicTransformOutputTypeDef",
    "JDBCConnectorSourceOutputTypeDef",
    "JDBCConnectorTargetOutputTypeDef",
    "S3CatalogDeltaSourceOutputTypeDef",
    "S3CatalogHudiSourceOutputTypeDef",
    "S3CsvSourceOutputTypeDef",
    "S3DeltaSourceOutputTypeDef",
    "S3HudiSourceOutputTypeDef",
    "S3JsonSourceOutputTypeDef",
    "S3ParquetSourceOutputTypeDef",
    "SnowflakeSourceOutputTypeDef",
    "SparkConnectorSourceOutputTypeDef",
    "SparkConnectorTargetOutputTypeDef",
    "SparkSQLOutputTypeDef",
    "AthenaConnectorSourceTypeDef",
    "CatalogDeltaSourceTypeDef",
    "CatalogHudiSourceTypeDef",
    "ConnectorDataSourceTypeDef",
    "CustomCodeTypeDef",
    "DynamicTransformTypeDef",
    "JDBCConnectorSourceTypeDef",
    "JDBCConnectorTargetTypeDef",
    "S3CatalogDeltaSourceTypeDef",
    "S3CatalogHudiSourceTypeDef",
    "S3CsvSourceTypeDef",
    "S3DeltaSourceTypeDef",
    "S3HudiSourceTypeDef",
    "S3JsonSourceTypeDef",
    "S3ParquetSourceTypeDef",
    "SnowflakeSourceTypeDef",
    "SparkConnectorSourceTypeDef",
    "SparkConnectorTargetTypeDef",
    "SparkSQLTypeDef",
    "GetJobRunResponseTypeDef",
    "GetJobRunsResponseTypeDef",
    "JobNodeDetailsTypeDef",
    "GetMLTaskRunResponseTypeDef",
    "TaskRunTypeDef",
    "CreateMLTransformRequestRequestTypeDef",
    "QuerySchemaVersionMetadataResponseTypeDef",
    "AuthenticationConfigurationInputTypeDef",
    "AuthenticationConfigurationTypeDef",
    "BatchDeletePartitionRequestRequestTypeDef",
    "BatchGetPartitionRequestRequestTypeDef",
    "CreateUserDefinedFunctionRequestRequestTypeDef",
    "UpdateUserDefinedFunctionRequestRequestTypeDef",
    "GetUserDefinedFunctionResponseTypeDef",
    "GetUserDefinedFunctionsResponseTypeDef",
    "ListTableOptimizerRunsResponseTypeDef",
    "TableOptimizerTypeDef",
    "StatementTypeDef",
    "CreateTriggerRequestRequestTypeDef",
    "GetPartitionIndexesResponseTypeDef",
    "ColumnStatisticsDataTypeDef",
    "CreateScriptRequestRequestTypeDef",
    "BatchGetTriggersResponseTypeDef",
    "GetTriggerResponseTypeDef",
    "GetTriggersResponseTypeDef",
    "TriggerNodeDetailsTypeDef",
    "UpdateTriggerResponseTypeDef",
    "UpdateTriggerRequestRequestTypeDef",
    "GetMLTransformResponseTypeDef",
    "MLTransformTypeDef",
    "BatchGetCrawlersResponseTypeDef",
    "GetCrawlerResponseTypeDef",
    "GetCrawlersResponseTypeDef",
    "GetDatabaseResponseTypeDef",
    "GetDatabasesResponseTypeDef",
    "CreateDatabaseRequestRequestTypeDef",
    "UpdateDatabaseRequestRequestTypeDef",
    "DataQualityResultTypeDef",
    "GetDataQualityResultResponseTypeDef",
    "ListDataQualityResultsResponseTypeDef",
    "ListDataQualityRuleRecommendationRunsResponseTypeDef",
    "ListDataQualityRulesetEvaluationRunsResponseTypeDef",
    "ListDataQualityResultsRequestRequestTypeDef",
    "ListDataQualityRuleRecommendationRunsRequestRequestTypeDef",
    "ListDataQualityRulesetEvaluationRunsRequestRequestTypeDef",
    "StartDataQualityRulesetEvaluationRunRequestRequestTypeDef",
    "ColumnStatisticsOutputTypeDef",
    "PartitionTypeDef",
    "TableTypeDef",
    "PartitionInputTypeDef",
    "TableInputTypeDef",
    "GetSecurityConfigurationResponseTypeDef",
    "GetSecurityConfigurationsResponseTypeDef",
    "CodeGenConfigurationNodeExtraOutputTypeDef",
    "CodeGenConfigurationNodeOutputTypeDef",
    "CodeGenConfigurationNodeTypeDef",
    "GetMLTaskRunsResponseTypeDef",
    "ConnectionInputTypeDef",
    "ConnectionTypeDef",
    "BatchTableOptimizerTypeDef",
    "GetTableOptimizerResponseTypeDef",
    "GetStatementResponseTypeDef",
    "ListStatementsResponseTypeDef",
    "ColumnStatisticsTypeDef",
    "NodeTypeDef",
    "GetMLTransformsResponseTypeDef",
    "BatchGetDataQualityResultResponseTypeDef",
    "ColumnStatisticsErrorTypeDef",
    "GetColumnStatisticsForPartitionResponseTypeDef",
    "GetColumnStatisticsForTableResponseTypeDef",
    "BatchGetPartitionResponseTypeDef",
    "GetPartitionResponseTypeDef",
    "GetPartitionsResponseTypeDef",
    "GetUnfilteredPartitionMetadataResponseTypeDef",
    "UnfilteredPartitionTypeDef",
    "GetTableResponseTypeDef",
    "GetTablesResponseTypeDef",
    "GetUnfilteredTableMetadataResponseTypeDef",
    "SearchTablesResponseTypeDef",
    "TableVersionTypeDef",
    "BatchCreatePartitionRequestRequestTypeDef",
    "BatchUpdatePartitionRequestEntryTypeDef",
    "CreatePartitionRequestRequestTypeDef",
    "UpdatePartitionRequestRequestTypeDef",
    "CreateTableRequestRequestTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "JobTypeDef",
    "CodeGenConfigurationNodeUnionTypeDef",
    "JobUpdateTypeDef",
    "CreateConnectionRequestRequestTypeDef",
    "UpdateConnectionRequestRequestTypeDef",
    "GetConnectionResponseTypeDef",
    "GetConnectionsResponseTypeDef",
    "BatchGetTableOptimizerResponseTypeDef",
    "ColumnStatisticsUnionTypeDef",
    "WorkflowGraphTypeDef",
    "UpdateColumnStatisticsForPartitionResponseTypeDef",
    "UpdateColumnStatisticsForTableResponseTypeDef",
    "GetUnfilteredPartitionsMetadataResponseTypeDef",
    "GetTableVersionResponseTypeDef",
    "GetTableVersionsResponseTypeDef",
    "BatchUpdatePartitionRequestRequestTypeDef",
    "BatchGetJobsResponseTypeDef",
    "GetJobResponseTypeDef",
    "GetJobsResponseTypeDef",
    "CreateJobRequestRequestTypeDef",
    "UpdateJobRequestRequestTypeDef",
    "UpdateColumnStatisticsForPartitionRequestRequestTypeDef",
    "UpdateColumnStatisticsForTableRequestRequestTypeDef",
    "WorkflowRunTypeDef",
    "GetWorkflowRunResponseTypeDef",
    "GetWorkflowRunsResponseTypeDef",
    "WorkflowTypeDef",
    "BatchGetWorkflowsResponseTypeDef",
    "GetWorkflowResponseTypeDef",
)

NotificationPropertyTypeDef = TypedDict(
    "NotificationPropertyTypeDef",
    {
        "NotifyDelayAfter": NotRequired[int],
    },
)
AggregateOperationExtraOutputTypeDef = TypedDict(
    "AggregateOperationExtraOutputTypeDef",
    {
        "Column": List[str],
        "AggFunc": AggFunctionType,
    },
)
AggregateOperationOutputTypeDef = TypedDict(
    "AggregateOperationOutputTypeDef",
    {
        "Column": List[str],
        "AggFunc": AggFunctionType,
    },
)
AggregateOperationTypeDef = TypedDict(
    "AggregateOperationTypeDef",
    {
        "Column": Sequence[str],
        "AggFunc": AggFunctionType,
    },
)
AmazonRedshiftAdvancedOptionTypeDef = TypedDict(
    "AmazonRedshiftAdvancedOptionTypeDef",
    {
        "Key": NotRequired[str],
        "Value": NotRequired[str],
    },
)
OptionTypeDef = TypedDict(
    "OptionTypeDef",
    {
        "Value": NotRequired[str],
        "Label": NotRequired[str],
        "Description": NotRequired[str],
    },
)
ApplyMappingExtraOutputTypeDef = TypedDict(
    "ApplyMappingExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Mapping": List["MappingExtraOutputTypeDef"],
    },
)
ApplyMappingOutputTypeDef = TypedDict(
    "ApplyMappingOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Mapping": List["MappingOutputTypeDef"],
    },
)
ApplyMappingTypeDef = TypedDict(
    "ApplyMappingTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Mapping": Sequence["MappingTypeDef"],
    },
)
AuditContextTypeDef = TypedDict(
    "AuditContextTypeDef",
    {
        "AdditionalAuditContext": NotRequired[str],
        "RequestedColumns": NotRequired[Sequence[str]],
        "AllColumnsRequested": NotRequired[bool],
    },
)
AuthorizationCodePropertiesTypeDef = TypedDict(
    "AuthorizationCodePropertiesTypeDef",
    {
        "AuthorizationCode": NotRequired[str],
        "RedirectUri": NotRequired[str],
    },
)
PartitionValueListOutputTypeDef = TypedDict(
    "PartitionValueListOutputTypeDef",
    {
        "Values": List[str],
    },
)
BasicCatalogTargetExtraOutputTypeDef = TypedDict(
    "BasicCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
BasicCatalogTargetOutputTypeDef = TypedDict(
    "BasicCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
BasicCatalogTargetTypeDef = TypedDict(
    "BasicCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Database": str,
        "Table": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
BatchDeleteConnectionRequestRequestTypeDef = TypedDict(
    "BatchDeleteConnectionRequestRequestTypeDef",
    {
        "ConnectionNameList": Sequence[str],
        "CatalogId": NotRequired[str],
    },
)
ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "ErrorCode": NotRequired[str],
        "ErrorMessage": NotRequired[str],
    },
)
BatchDeleteTableRequestRequestTypeDef = TypedDict(
    "BatchDeleteTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TablesToDelete": Sequence[str],
        "CatalogId": NotRequired[str],
        "TransactionId": NotRequired[str],
    },
)
BatchDeleteTableVersionRequestRequestTypeDef = TypedDict(
    "BatchDeleteTableVersionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "VersionIds": Sequence[str],
        "CatalogId": NotRequired[str],
    },
)
BatchGetBlueprintsRequestRequestTypeDef = TypedDict(
    "BatchGetBlueprintsRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "IncludeBlueprint": NotRequired[bool],
        "IncludeParameterSpec": NotRequired[bool],
    },
)
BatchGetCrawlersRequestRequestTypeDef = TypedDict(
    "BatchGetCrawlersRequestRequestTypeDef",
    {
        "CrawlerNames": Sequence[str],
    },
)
BatchGetCustomEntityTypesRequestRequestTypeDef = TypedDict(
    "BatchGetCustomEntityTypesRequestRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)
CustomEntityTypeTypeDef = TypedDict(
    "CustomEntityTypeTypeDef",
    {
        "Name": str,
        "RegexString": str,
        "ContextWords": NotRequired[List[str]],
    },
)
BatchGetDataQualityResultRequestRequestTypeDef = TypedDict(
    "BatchGetDataQualityResultRequestRequestTypeDef",
    {
        "ResultIds": Sequence[str],
    },
)
BatchGetDevEndpointsRequestRequestTypeDef = TypedDict(
    "BatchGetDevEndpointsRequestRequestTypeDef",
    {
        "DevEndpointNames": Sequence[str],
    },
)
DevEndpointTypeDef = TypedDict(
    "DevEndpointTypeDef",
    {
        "EndpointName": NotRequired[str],
        "RoleArn": NotRequired[str],
        "SecurityGroupIds": NotRequired[List[str]],
        "SubnetId": NotRequired[str],
        "YarnEndpointAddress": NotRequired[str],
        "PrivateAddress": NotRequired[str],
        "ZeppelinRemoteSparkInterpreterPort": NotRequired[int],
        "PublicAddress": NotRequired[str],
        "Status": NotRequired[str],
        "WorkerType": NotRequired[WorkerTypeType],
        "GlueVersion": NotRequired[str],
        "NumberOfWorkers": NotRequired[int],
        "NumberOfNodes": NotRequired[int],
        "AvailabilityZone": NotRequired[str],
        "VpcId": NotRequired[str],
        "ExtraPythonLibsS3Path": NotRequired[str],
        "ExtraJarsS3Path": NotRequired[str],
        "FailureReason": NotRequired[str],
        "LastUpdateStatus": NotRequired[str],
        "CreatedTimestamp": NotRequired[datetime],
        "LastModifiedTimestamp": NotRequired[datetime],
        "PublicKey": NotRequired[str],
        "PublicKeys": NotRequired[List[str]],
        "SecurityConfiguration": NotRequired[str],
        "Arguments": NotRequired[Dict[str, str]],
    },
)
BatchGetJobsRequestRequestTypeDef = TypedDict(
    "BatchGetJobsRequestRequestTypeDef",
    {
        "JobNames": Sequence[str],
    },
)
BatchGetTableOptimizerEntryTypeDef = TypedDict(
    "BatchGetTableOptimizerEntryTypeDef",
    {
        "catalogId": NotRequired[str],
        "databaseName": NotRequired[str],
        "tableName": NotRequired[str],
        "type": NotRequired[Literal["compaction"]],
    },
)
BatchGetTriggersRequestRequestTypeDef = TypedDict(
    "BatchGetTriggersRequestRequestTypeDef",
    {
        "TriggerNames": Sequence[str],
    },
)
BatchGetWorkflowsRequestRequestTypeDef = TypedDict(
    "BatchGetWorkflowsRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "IncludeGraph": NotRequired[bool],
    },
)
BatchStopJobRunRequestRequestTypeDef = TypedDict(
    "BatchStopJobRunRequestRequestTypeDef",
    {
        "JobName": str,
        "JobRunIds": Sequence[str],
    },
)
BatchStopJobRunSuccessfulSubmissionTypeDef = TypedDict(
    "BatchStopJobRunSuccessfulSubmissionTypeDef",
    {
        "JobName": NotRequired[str],
        "JobRunId": NotRequired[str],
    },
)
BinaryColumnStatisticsDataTypeDef = TypedDict(
    "BinaryColumnStatisticsDataTypeDef",
    {
        "MaximumLength": int,
        "AverageLength": float,
        "NumberOfNulls": int,
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
BlueprintDetailsTypeDef = TypedDict(
    "BlueprintDetailsTypeDef",
    {
        "BlueprintName": NotRequired[str],
        "RunId": NotRequired[str],
    },
)
BlueprintRunTypeDef = TypedDict(
    "BlueprintRunTypeDef",
    {
        "BlueprintName": NotRequired[str],
        "RunId": NotRequired[str],
        "WorkflowName": NotRequired[str],
        "State": NotRequired[BlueprintRunStateType],
        "StartedOn": NotRequired[datetime],
        "CompletedOn": NotRequired[datetime],
        "ErrorMessage": NotRequired[str],
        "RollbackErrorMessage": NotRequired[str],
        "Parameters": NotRequired[str],
        "RoleArn": NotRequired[str],
    },
)
LastActiveDefinitionTypeDef = TypedDict(
    "LastActiveDefinitionTypeDef",
    {
        "Description": NotRequired[str],
        "LastModifiedOn": NotRequired[datetime],
        "ParameterSpec": NotRequired[str],
        "BlueprintLocation": NotRequired[str],
        "BlueprintServiceLocation": NotRequired[str],
    },
)
BooleanColumnStatisticsDataTypeDef = TypedDict(
    "BooleanColumnStatisticsDataTypeDef",
    {
        "NumberOfTrues": int,
        "NumberOfFalses": int,
        "NumberOfNulls": int,
    },
)
CancelDataQualityRuleRecommendationRunRequestRequestTypeDef = TypedDict(
    "CancelDataQualityRuleRecommendationRunRequestRequestTypeDef",
    {
        "RunId": str,
    },
)
CancelDataQualityRulesetEvaluationRunRequestRequestTypeDef = TypedDict(
    "CancelDataQualityRulesetEvaluationRunRequestRequestTypeDef",
    {
        "RunId": str,
    },
)
CancelMLTaskRunRequestRequestTypeDef = TypedDict(
    "CancelMLTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
    },
)
CancelStatementRequestRequestTypeDef = TypedDict(
    "CancelStatementRequestRequestTypeDef",
    {
        "SessionId": str,
        "Id": int,
        "RequestOrigin": NotRequired[str],
    },
)
CatalogEntryTypeDef = TypedDict(
    "CatalogEntryTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
CatalogImportStatusTypeDef = TypedDict(
    "CatalogImportStatusTypeDef",
    {
        "ImportCompleted": NotRequired[bool],
        "ImportTime": NotRequired[datetime],
        "ImportedBy": NotRequired[str],
    },
)
KafkaStreamingSourceOptionsExtraOutputTypeDef = TypedDict(
    "KafkaStreamingSourceOptionsExtraOutputTypeDef",
    {
        "BootstrapServers": NotRequired[str],
        "SecurityProtocol": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "TopicName": NotRequired[str],
        "Assign": NotRequired[str],
        "SubscribePattern": NotRequired[str],
        "Classification": NotRequired[str],
        "Delimiter": NotRequired[str],
        "StartingOffsets": NotRequired[str],
        "EndingOffsets": NotRequired[str],
        "PollTimeoutMs": NotRequired[int],
        "NumRetries": NotRequired[int],
        "RetryIntervalMs": NotRequired[int],
        "MaxOffsetsPerTrigger": NotRequired[int],
        "MinPartitions": NotRequired[int],
        "IncludeHeaders": NotRequired[bool],
        "AddRecordTimestamp": NotRequired[str],
        "EmitConsumerLagMetrics": NotRequired[str],
        "StartingTimestamp": NotRequired[datetime],
    },
)
StreamingDataPreviewOptionsTypeDef = TypedDict(
    "StreamingDataPreviewOptionsTypeDef",
    {
        "PollingTime": NotRequired[int],
        "RecordPollingLimit": NotRequired[int],
    },
)
KafkaStreamingSourceOptionsOutputTypeDef = TypedDict(
    "KafkaStreamingSourceOptionsOutputTypeDef",
    {
        "BootstrapServers": NotRequired[str],
        "SecurityProtocol": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "TopicName": NotRequired[str],
        "Assign": NotRequired[str],
        "SubscribePattern": NotRequired[str],
        "Classification": NotRequired[str],
        "Delimiter": NotRequired[str],
        "StartingOffsets": NotRequired[str],
        "EndingOffsets": NotRequired[str],
        "PollTimeoutMs": NotRequired[int],
        "NumRetries": NotRequired[int],
        "RetryIntervalMs": NotRequired[int],
        "MaxOffsetsPerTrigger": NotRequired[int],
        "MinPartitions": NotRequired[int],
        "IncludeHeaders": NotRequired[bool],
        "AddRecordTimestamp": NotRequired[str],
        "EmitConsumerLagMetrics": NotRequired[str],
        "StartingTimestamp": NotRequired[datetime],
    },
)
KinesisStreamingSourceOptionsExtraOutputTypeDef = TypedDict(
    "KinesisStreamingSourceOptionsExtraOutputTypeDef",
    {
        "EndpointUrl": NotRequired[str],
        "StreamName": NotRequired[str],
        "Classification": NotRequired[str],
        "Delimiter": NotRequired[str],
        "StartingPosition": NotRequired[StartingPositionType],
        "MaxFetchTimeInMs": NotRequired[int],
        "MaxFetchRecordsPerShard": NotRequired[int],
        "MaxRecordPerRead": NotRequired[int],
        "AddIdleTimeBetweenReads": NotRequired[bool],
        "IdleTimeBetweenReadsInMs": NotRequired[int],
        "DescribeShardInterval": NotRequired[int],
        "NumRetries": NotRequired[int],
        "RetryIntervalMs": NotRequired[int],
        "MaxRetryIntervalMs": NotRequired[int],
        "AvoidEmptyBatches": NotRequired[bool],
        "StreamArn": NotRequired[str],
        "RoleArn": NotRequired[str],
        "RoleSessionName": NotRequired[str],
        "AddRecordTimestamp": NotRequired[str],
        "EmitConsumerLagMetrics": NotRequired[str],
        "StartingTimestamp": NotRequired[datetime],
    },
)
KinesisStreamingSourceOptionsOutputTypeDef = TypedDict(
    "KinesisStreamingSourceOptionsOutputTypeDef",
    {
        "EndpointUrl": NotRequired[str],
        "StreamName": NotRequired[str],
        "Classification": NotRequired[str],
        "Delimiter": NotRequired[str],
        "StartingPosition": NotRequired[StartingPositionType],
        "MaxFetchTimeInMs": NotRequired[int],
        "MaxFetchRecordsPerShard": NotRequired[int],
        "MaxRecordPerRead": NotRequired[int],
        "AddIdleTimeBetweenReads": NotRequired[bool],
        "IdleTimeBetweenReadsInMs": NotRequired[int],
        "DescribeShardInterval": NotRequired[int],
        "NumRetries": NotRequired[int],
        "RetryIntervalMs": NotRequired[int],
        "MaxRetryIntervalMs": NotRequired[int],
        "AvoidEmptyBatches": NotRequired[bool],
        "StreamArn": NotRequired[str],
        "RoleArn": NotRequired[str],
        "RoleSessionName": NotRequired[str],
        "AddRecordTimestamp": NotRequired[str],
        "EmitConsumerLagMetrics": NotRequired[str],
        "StartingTimestamp": NotRequired[datetime],
    },
)
CatalogSchemaChangePolicyTypeDef = TypedDict(
    "CatalogSchemaChangePolicyTypeDef",
    {
        "EnableUpdateCatalog": NotRequired[bool],
        "UpdateBehavior": NotRequired[UpdateCatalogBehaviorType],
    },
)
CatalogSourceTypeDef = TypedDict(
    "CatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
CatalogTargetExtraOutputTypeDef = TypedDict(
    "CatalogTargetExtraOutputTypeDef",
    {
        "DatabaseName": str,
        "Tables": List[str],
        "ConnectionName": NotRequired[str],
        "EventQueueArn": NotRequired[str],
        "DlqEventQueueArn": NotRequired[str],
    },
)
CatalogTargetOutputTypeDef = TypedDict(
    "CatalogTargetOutputTypeDef",
    {
        "DatabaseName": str,
        "Tables": List[str],
        "ConnectionName": NotRequired[str],
        "EventQueueArn": NotRequired[str],
        "DlqEventQueueArn": NotRequired[str],
    },
)
CatalogTargetTypeDef = TypedDict(
    "CatalogTargetTypeDef",
    {
        "DatabaseName": str,
        "Tables": Sequence[str],
        "ConnectionName": NotRequired[str],
        "EventQueueArn": NotRequired[str],
        "DlqEventQueueArn": NotRequired[str],
    },
)
CheckSchemaVersionValidityInputRequestTypeDef = TypedDict(
    "CheckSchemaVersionValidityInputRequestTypeDef",
    {
        "DataFormat": DataFormatType,
        "SchemaDefinition": str,
    },
)
CsvClassifierTypeDef = TypedDict(
    "CsvClassifierTypeDef",
    {
        "Name": str,
        "CreationTime": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "Version": NotRequired[int],
        "Delimiter": NotRequired[str],
        "QuoteSymbol": NotRequired[str],
        "ContainsHeader": NotRequired[CsvHeaderOptionType],
        "Header": NotRequired[List[str]],
        "DisableValueTrimming": NotRequired[bool],
        "AllowSingleColumn": NotRequired[bool],
        "CustomDatatypeConfigured": NotRequired[bool],
        "CustomDatatypes": NotRequired[List[str]],
        "Serde": NotRequired[CsvSerdeOptionType],
    },
)
GrokClassifierTypeDef = TypedDict(
    "GrokClassifierTypeDef",
    {
        "Name": str,
        "Classification": str,
        "GrokPattern": str,
        "CreationTime": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "Version": NotRequired[int],
        "CustomPatterns": NotRequired[str],
    },
)
JsonClassifierTypeDef = TypedDict(
    "JsonClassifierTypeDef",
    {
        "Name": str,
        "JsonPath": str,
        "CreationTime": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "Version": NotRequired[int],
    },
)
XMLClassifierTypeDef = TypedDict(
    "XMLClassifierTypeDef",
    {
        "Name": str,
        "Classification": str,
        "CreationTime": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "Version": NotRequired[int],
        "RowTag": NotRequired[str],
    },
)
CloudWatchEncryptionTypeDef = TypedDict(
    "CloudWatchEncryptionTypeDef",
    {
        "CloudWatchEncryptionMode": NotRequired[CloudWatchEncryptionModeType],
        "KmsKeyArn": NotRequired[str],
    },
)
ConnectorDataTargetExtraOutputTypeDef = TypedDict(
    "ConnectorDataTargetExtraOutputTypeDef",
    {
        "Name": str,
        "ConnectionType": str,
        "Data": Dict[str, str],
        "Inputs": NotRequired[List[str]],
    },
)
DirectJDBCSourceTypeDef = TypedDict(
    "DirectJDBCSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "ConnectionName": str,
        "ConnectionType": JDBCConnectionTypeType,
        "RedshiftTmpDir": NotRequired[str],
    },
)
DropDuplicatesExtraOutputTypeDef = TypedDict(
    "DropDuplicatesExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Columns": NotRequired[List[List[str]]],
    },
)
DropFieldsExtraOutputTypeDef = TypedDict(
    "DropFieldsExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)
DynamoDBCatalogSourceTypeDef = TypedDict(
    "DynamoDBCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
FillMissingValuesExtraOutputTypeDef = TypedDict(
    "FillMissingValuesExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ImputedPath": str,
        "FilledPath": NotRequired[str],
    },
)
MergeExtraOutputTypeDef = TypedDict(
    "MergeExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Source": str,
        "PrimaryKeys": List[List[str]],
    },
)
MicrosoftSQLServerCatalogSourceTypeDef = TypedDict(
    "MicrosoftSQLServerCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
MicrosoftSQLServerCatalogTargetExtraOutputTypeDef = TypedDict(
    "MicrosoftSQLServerCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
MySQLCatalogSourceTypeDef = TypedDict(
    "MySQLCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
MySQLCatalogTargetExtraOutputTypeDef = TypedDict(
    "MySQLCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
OracleSQLCatalogSourceTypeDef = TypedDict(
    "OracleSQLCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
OracleSQLCatalogTargetExtraOutputTypeDef = TypedDict(
    "OracleSQLCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
PIIDetectionExtraOutputTypeDef = TypedDict(
    "PIIDetectionExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "PiiType": PiiTypeType,
        "EntityTypesToDetect": List[str],
        "OutputColumnName": NotRequired[str],
        "SampleFraction": NotRequired[float],
        "ThresholdFraction": NotRequired[float],
        "MaskValue": NotRequired[str],
    },
)
PostgreSQLCatalogSourceTypeDef = TypedDict(
    "PostgreSQLCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
PostgreSQLCatalogTargetExtraOutputTypeDef = TypedDict(
    "PostgreSQLCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
RedshiftSourceTypeDef = TypedDict(
    "RedshiftSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "RedshiftTmpDir": NotRequired[str],
        "TmpDirIAMRole": NotRequired[str],
    },
)
RelationalCatalogSourceTypeDef = TypedDict(
    "RelationalCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
    },
)
RenameFieldExtraOutputTypeDef = TypedDict(
    "RenameFieldExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "SourcePath": List[str],
        "TargetPath": List[str],
    },
)
SelectFieldsExtraOutputTypeDef = TypedDict(
    "SelectFieldsExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)
SelectFromCollectionExtraOutputTypeDef = TypedDict(
    "SelectFromCollectionExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Index": int,
    },
)
SpigotExtraOutputTypeDef = TypedDict(
    "SpigotExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Topk": NotRequired[int],
        "Prob": NotRequired[float],
    },
)
SplitFieldsExtraOutputTypeDef = TypedDict(
    "SplitFieldsExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)
UnionExtraOutputTypeDef = TypedDict(
    "UnionExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "UnionType": UnionTypeType,
    },
)
ConnectorDataTargetOutputTypeDef = TypedDict(
    "ConnectorDataTargetOutputTypeDef",
    {
        "Name": str,
        "ConnectionType": str,
        "Data": Dict[str, str],
        "Inputs": NotRequired[List[str]],
    },
)
DropDuplicatesOutputTypeDef = TypedDict(
    "DropDuplicatesOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Columns": NotRequired[List[List[str]]],
    },
)
DropFieldsOutputTypeDef = TypedDict(
    "DropFieldsOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)
FillMissingValuesOutputTypeDef = TypedDict(
    "FillMissingValuesOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ImputedPath": str,
        "FilledPath": NotRequired[str],
    },
)
MergeOutputTypeDef = TypedDict(
    "MergeOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Source": str,
        "PrimaryKeys": List[List[str]],
    },
)
MicrosoftSQLServerCatalogTargetOutputTypeDef = TypedDict(
    "MicrosoftSQLServerCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
MySQLCatalogTargetOutputTypeDef = TypedDict(
    "MySQLCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
OracleSQLCatalogTargetOutputTypeDef = TypedDict(
    "OracleSQLCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
PIIDetectionOutputTypeDef = TypedDict(
    "PIIDetectionOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "PiiType": PiiTypeType,
        "EntityTypesToDetect": List[str],
        "OutputColumnName": NotRequired[str],
        "SampleFraction": NotRequired[float],
        "ThresholdFraction": NotRequired[float],
        "MaskValue": NotRequired[str],
    },
)
PostgreSQLCatalogTargetOutputTypeDef = TypedDict(
    "PostgreSQLCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
    },
)
RenameFieldOutputTypeDef = TypedDict(
    "RenameFieldOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "SourcePath": List[str],
        "TargetPath": List[str],
    },
)
SelectFieldsOutputTypeDef = TypedDict(
    "SelectFieldsOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)
SelectFromCollectionOutputTypeDef = TypedDict(
    "SelectFromCollectionOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Index": int,
    },
)
SpigotOutputTypeDef = TypedDict(
    "SpigotOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Topk": NotRequired[int],
        "Prob": NotRequired[float],
    },
)
SplitFieldsOutputTypeDef = TypedDict(
    "SplitFieldsOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Paths": List[List[str]],
    },
)
UnionOutputTypeDef = TypedDict(
    "UnionOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "UnionType": UnionTypeType,
    },
)
ConnectorDataTargetTypeDef = TypedDict(
    "ConnectorDataTargetTypeDef",
    {
        "Name": str,
        "ConnectionType": str,
        "Data": Mapping[str, str],
        "Inputs": NotRequired[Sequence[str]],
    },
)
DropDuplicatesTypeDef = TypedDict(
    "DropDuplicatesTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Columns": NotRequired[Sequence[Sequence[str]]],
    },
)
DropFieldsTypeDef = TypedDict(
    "DropFieldsTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Paths": Sequence[Sequence[str]],
    },
)
FillMissingValuesTypeDef = TypedDict(
    "FillMissingValuesTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "ImputedPath": str,
        "FilledPath": NotRequired[str],
    },
)
MergeTypeDef = TypedDict(
    "MergeTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Source": str,
        "PrimaryKeys": Sequence[Sequence[str]],
    },
)
MicrosoftSQLServerCatalogTargetTypeDef = TypedDict(
    "MicrosoftSQLServerCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Database": str,
        "Table": str,
    },
)
MySQLCatalogTargetTypeDef = TypedDict(
    "MySQLCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Database": str,
        "Table": str,
    },
)
OracleSQLCatalogTargetTypeDef = TypedDict(
    "OracleSQLCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Database": str,
        "Table": str,
    },
)
PIIDetectionTypeDef = TypedDict(
    "PIIDetectionTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "PiiType": PiiTypeType,
        "EntityTypesToDetect": Sequence[str],
        "OutputColumnName": NotRequired[str],
        "SampleFraction": NotRequired[float],
        "ThresholdFraction": NotRequired[float],
        "MaskValue": NotRequired[str],
    },
)
PostgreSQLCatalogTargetTypeDef = TypedDict(
    "PostgreSQLCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Database": str,
        "Table": str,
    },
)
RenameFieldTypeDef = TypedDict(
    "RenameFieldTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "SourcePath": Sequence[str],
        "TargetPath": Sequence[str],
    },
)
SelectFieldsTypeDef = TypedDict(
    "SelectFieldsTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Paths": Sequence[Sequence[str]],
    },
)
SelectFromCollectionTypeDef = TypedDict(
    "SelectFromCollectionTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Index": int,
    },
)
SpigotTypeDef = TypedDict(
    "SpigotTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Path": str,
        "Topk": NotRequired[int],
        "Prob": NotRequired[float],
    },
)
SplitFieldsTypeDef = TypedDict(
    "SplitFieldsTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Paths": Sequence[Sequence[str]],
    },
)
UnionTypeDef = TypedDict(
    "UnionTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "UnionType": UnionTypeType,
    },
)
CodeGenEdgeTypeDef = TypedDict(
    "CodeGenEdgeTypeDef",
    {
        "Source": str,
        "Target": str,
        "TargetParameter": NotRequired[str],
    },
)
CodeGenNodeArgTypeDef = TypedDict(
    "CodeGenNodeArgTypeDef",
    {
        "Name": str,
        "Value": str,
        "Param": NotRequired[bool],
    },
)
ColumnImportanceTypeDef = TypedDict(
    "ColumnImportanceTypeDef",
    {
        "ColumnName": NotRequired[str],
        "Importance": NotRequired[float],
    },
)
ColumnOutputTypeDef = TypedDict(
    "ColumnOutputTypeDef",
    {
        "Name": str,
        "Type": NotRequired[str],
        "Comment": NotRequired[str],
        "Parameters": NotRequired[Dict[str, str]],
    },
)
ColumnRowFilterTypeDef = TypedDict(
    "ColumnRowFilterTypeDef",
    {
        "ColumnName": NotRequired[str],
        "RowFilterExpression": NotRequired[str],
    },
)
DateColumnStatisticsDataOutputTypeDef = TypedDict(
    "DateColumnStatisticsDataOutputTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
        "MinimumValue": NotRequired[datetime],
        "MaximumValue": NotRequired[datetime],
    },
)
DoubleColumnStatisticsDataTypeDef = TypedDict(
    "DoubleColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
        "MinimumValue": NotRequired[float],
        "MaximumValue": NotRequired[float],
    },
)
LongColumnStatisticsDataTypeDef = TypedDict(
    "LongColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
        "MinimumValue": NotRequired[int],
        "MaximumValue": NotRequired[int],
    },
)
StringColumnStatisticsDataTypeDef = TypedDict(
    "StringColumnStatisticsDataTypeDef",
    {
        "MaximumLength": int,
        "AverageLength": float,
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
    },
)
ColumnStatisticsTaskRunTypeDef = TypedDict(
    "ColumnStatisticsTaskRunTypeDef",
    {
        "CustomerId": NotRequired[str],
        "ColumnStatisticsTaskRunId": NotRequired[str],
        "DatabaseName": NotRequired[str],
        "TableName": NotRequired[str],
        "ColumnNameList": NotRequired[List[str]],
        "CatalogID": NotRequired[str],
        "Role": NotRequired[str],
        "SampleSize": NotRequired[float],
        "SecurityConfiguration": NotRequired[str],
        "NumberOfWorkers": NotRequired[int],
        "WorkerType": NotRequired[str],
        "Status": NotRequired[ColumnStatisticsStateType],
        "CreationTime": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "ErrorMessage": NotRequired[str],
        "DPUSeconds": NotRequired[float],
    },
)
TimestampTypeDef = Union[datetime, str]
ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "Name": str,
        "Type": NotRequired[str],
        "Comment": NotRequired[str],
        "Parameters": NotRequired[Mapping[str, str]],
    },
)
ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "LogicalOperator": NotRequired[Literal["EQUALS"]],
        "JobName": NotRequired[str],
        "State": NotRequired[JobRunStateType],
        "CrawlerName": NotRequired[str],
        "CrawlState": NotRequired[CrawlStateType],
    },
)
ConfigurationObjectOutputTypeDef = TypedDict(
    "ConfigurationObjectOutputTypeDef",
    {
        "DefaultValue": NotRequired[str],
        "AllowedValues": NotRequired[List[str]],
        "MinValue": NotRequired[str],
        "MaxValue": NotRequired[str],
    },
)
ConfigurationObjectTypeDef = TypedDict(
    "ConfigurationObjectTypeDef",
    {
        "DefaultValue": NotRequired[str],
        "AllowedValues": NotRequired[Sequence[str]],
        "MinValue": NotRequired[str],
        "MaxValue": NotRequired[str],
    },
)
ConfusionMatrixTypeDef = TypedDict(
    "ConfusionMatrixTypeDef",
    {
        "NumTruePositives": NotRequired[int],
        "NumFalsePositives": NotRequired[int],
        "NumTrueNegatives": NotRequired[int],
        "NumFalseNegatives": NotRequired[int],
    },
)
PhysicalConnectionRequirementsTypeDef = TypedDict(
    "PhysicalConnectionRequirementsTypeDef",
    {
        "SubnetId": NotRequired[str],
        "SecurityGroupIdList": NotRequired[Sequence[str]],
        "AvailabilityZone": NotRequired[str],
    },
)
ConnectionPasswordEncryptionTypeDef = TypedDict(
    "ConnectionPasswordEncryptionTypeDef",
    {
        "ReturnConnectionPasswordEncrypted": bool,
        "AwsKmsKeyId": NotRequired[str],
    },
)
PhysicalConnectionRequirementsOutputTypeDef = TypedDict(
    "PhysicalConnectionRequirementsOutputTypeDef",
    {
        "SubnetId": NotRequired[str],
        "SecurityGroupIdList": NotRequired[List[str]],
        "AvailabilityZone": NotRequired[str],
    },
)
ConnectionsListExtraOutputTypeDef = TypedDict(
    "ConnectionsListExtraOutputTypeDef",
    {
        "Connections": NotRequired[List[str]],
    },
)
ConnectionsListOutputTypeDef = TypedDict(
    "ConnectionsListOutputTypeDef",
    {
        "Connections": NotRequired[List[str]],
    },
)
ConnectionsListTypeDef = TypedDict(
    "ConnectionsListTypeDef",
    {
        "Connections": NotRequired[Sequence[str]],
    },
)
CrawlTypeDef = TypedDict(
    "CrawlTypeDef",
    {
        "State": NotRequired[CrawlStateType],
        "StartedOn": NotRequired[datetime],
        "CompletedOn": NotRequired[datetime],
        "ErrorMessage": NotRequired[str],
        "LogGroup": NotRequired[str],
        "LogStream": NotRequired[str],
    },
)
CrawlerHistoryTypeDef = TypedDict(
    "CrawlerHistoryTypeDef",
    {
        "CrawlId": NotRequired[str],
        "State": NotRequired[CrawlerHistoryStateType],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "Summary": NotRequired[str],
        "ErrorMessage": NotRequired[str],
        "LogGroup": NotRequired[str],
        "LogStream": NotRequired[str],
        "MessagePrefix": NotRequired[str],
        "DPUHour": NotRequired[float],
    },
)
CrawlerMetricsTypeDef = TypedDict(
    "CrawlerMetricsTypeDef",
    {
        "CrawlerName": NotRequired[str],
        "TimeLeftSeconds": NotRequired[float],
        "StillEstimating": NotRequired[bool],
        "LastRuntimeSeconds": NotRequired[float],
        "MedianRuntimeSeconds": NotRequired[float],
        "TablesCreated": NotRequired[int],
        "TablesUpdated": NotRequired[int],
        "TablesDeleted": NotRequired[int],
    },
)
DeltaTargetExtraOutputTypeDef = TypedDict(
    "DeltaTargetExtraOutputTypeDef",
    {
        "DeltaTables": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "WriteManifest": NotRequired[bool],
        "CreateNativeDeltaTable": NotRequired[bool],
    },
)
DynamoDBTargetTypeDef = TypedDict(
    "DynamoDBTargetTypeDef",
    {
        "Path": NotRequired[str],
        "scanAll": NotRequired[bool],
        "scanRate": NotRequired[float],
    },
)
HudiTargetExtraOutputTypeDef = TypedDict(
    "HudiTargetExtraOutputTypeDef",
    {
        "Paths": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "MaximumTraversalDepth": NotRequired[int],
    },
)
IcebergTargetExtraOutputTypeDef = TypedDict(
    "IcebergTargetExtraOutputTypeDef",
    {
        "Paths": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "MaximumTraversalDepth": NotRequired[int],
    },
)
JdbcTargetExtraOutputTypeDef = TypedDict(
    "JdbcTargetExtraOutputTypeDef",
    {
        "ConnectionName": NotRequired[str],
        "Path": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "EnableAdditionalMetadata": NotRequired[List[JdbcMetadataEntryType]],
    },
)
MongoDBTargetTypeDef = TypedDict(
    "MongoDBTargetTypeDef",
    {
        "ConnectionName": NotRequired[str],
        "Path": NotRequired[str],
        "ScanAll": NotRequired[bool],
    },
)
S3TargetExtraOutputTypeDef = TypedDict(
    "S3TargetExtraOutputTypeDef",
    {
        "Path": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "SampleSize": NotRequired[int],
        "EventQueueArn": NotRequired[str],
        "DlqEventQueueArn": NotRequired[str],
    },
)
DeltaTargetOutputTypeDef = TypedDict(
    "DeltaTargetOutputTypeDef",
    {
        "DeltaTables": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "WriteManifest": NotRequired[bool],
        "CreateNativeDeltaTable": NotRequired[bool],
    },
)
HudiTargetOutputTypeDef = TypedDict(
    "HudiTargetOutputTypeDef",
    {
        "Paths": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "MaximumTraversalDepth": NotRequired[int],
    },
)
IcebergTargetOutputTypeDef = TypedDict(
    "IcebergTargetOutputTypeDef",
    {
        "Paths": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "MaximumTraversalDepth": NotRequired[int],
    },
)
JdbcTargetOutputTypeDef = TypedDict(
    "JdbcTargetOutputTypeDef",
    {
        "ConnectionName": NotRequired[str],
        "Path": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "EnableAdditionalMetadata": NotRequired[List[JdbcMetadataEntryType]],
    },
)
S3TargetOutputTypeDef = TypedDict(
    "S3TargetOutputTypeDef",
    {
        "Path": NotRequired[str],
        "Exclusions": NotRequired[List[str]],
        "ConnectionName": NotRequired[str],
        "SampleSize": NotRequired[int],
        "EventQueueArn": NotRequired[str],
        "DlqEventQueueArn": NotRequired[str],
    },
)
DeltaTargetTypeDef = TypedDict(
    "DeltaTargetTypeDef",
    {
        "DeltaTables": NotRequired[Sequence[str]],
        "ConnectionName": NotRequired[str],
        "WriteManifest": NotRequired[bool],
        "CreateNativeDeltaTable": NotRequired[bool],
    },
)
HudiTargetTypeDef = TypedDict(
    "HudiTargetTypeDef",
    {
        "Paths": NotRequired[Sequence[str]],
        "ConnectionName": NotRequired[str],
        "Exclusions": NotRequired[Sequence[str]],
        "MaximumTraversalDepth": NotRequired[int],
    },
)
IcebergTargetTypeDef = TypedDict(
    "IcebergTargetTypeDef",
    {
        "Paths": NotRequired[Sequence[str]],
        "ConnectionName": NotRequired[str],
        "Exclusions": NotRequired[Sequence[str]],
        "MaximumTraversalDepth": NotRequired[int],
    },
)
JdbcTargetTypeDef = TypedDict(
    "JdbcTargetTypeDef",
    {
        "ConnectionName": NotRequired[str],
        "Path": NotRequired[str],
        "Exclusions": NotRequired[Sequence[str]],
        "EnableAdditionalMetadata": NotRequired[Sequence[JdbcMetadataEntryType]],
    },
)
S3TargetTypeDef = TypedDict(
    "S3TargetTypeDef",
    {
        "Path": NotRequired[str],
        "Exclusions": NotRequired[Sequence[str]],
        "ConnectionName": NotRequired[str],
        "SampleSize": NotRequired[int],
        "EventQueueArn": NotRequired[str],
        "DlqEventQueueArn": NotRequired[str],
    },
)
LakeFormationConfigurationTypeDef = TypedDict(
    "LakeFormationConfigurationTypeDef",
    {
        "UseLakeFormationCredentials": NotRequired[bool],
        "AccountId": NotRequired[str],
    },
)
LastCrawlInfoTypeDef = TypedDict(
    "LastCrawlInfoTypeDef",
    {
        "Status": NotRequired[LastCrawlStatusType],
        "ErrorMessage": NotRequired[str],
        "LogGroup": NotRequired[str],
        "LogStream": NotRequired[str],
        "MessagePrefix": NotRequired[str],
        "StartTime": NotRequired[datetime],
    },
)
LineageConfigurationTypeDef = TypedDict(
    "LineageConfigurationTypeDef",
    {
        "CrawlerLineageSettings": NotRequired[CrawlerLineageSettingsType],
    },
)
RecrawlPolicyTypeDef = TypedDict(
    "RecrawlPolicyTypeDef",
    {
        "RecrawlBehavior": NotRequired[RecrawlBehaviorType],
    },
)
ScheduleTypeDef = TypedDict(
    "ScheduleTypeDef",
    {
        "ScheduleExpression": NotRequired[str],
        "State": NotRequired[ScheduleStateType],
    },
)
SchemaChangePolicyTypeDef = TypedDict(
    "SchemaChangePolicyTypeDef",
    {
        "UpdateBehavior": NotRequired[UpdateBehaviorType],
        "DeleteBehavior": NotRequired[DeleteBehaviorType],
    },
)
CrawlsFilterTypeDef = TypedDict(
    "CrawlsFilterTypeDef",
    {
        "FieldName": NotRequired[FieldNameType],
        "FilterOperator": NotRequired[FilterOperatorType],
        "FieldValue": NotRequired[str],
    },
)
CreateBlueprintRequestRequestTypeDef = TypedDict(
    "CreateBlueprintRequestRequestTypeDef",
    {
        "Name": str,
        "BlueprintLocation": str,
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
CreateCsvClassifierRequestTypeDef = TypedDict(
    "CreateCsvClassifierRequestTypeDef",
    {
        "Name": str,
        "Delimiter": NotRequired[str],
        "QuoteSymbol": NotRequired[str],
        "ContainsHeader": NotRequired[CsvHeaderOptionType],
        "Header": NotRequired[Sequence[str]],
        "DisableValueTrimming": NotRequired[bool],
        "AllowSingleColumn": NotRequired[bool],
        "CustomDatatypeConfigured": NotRequired[bool],
        "CustomDatatypes": NotRequired[Sequence[str]],
        "Serde": NotRequired[CsvSerdeOptionType],
    },
)
CreateGrokClassifierRequestTypeDef = TypedDict(
    "CreateGrokClassifierRequestTypeDef",
    {
        "Classification": str,
        "Name": str,
        "GrokPattern": str,
        "CustomPatterns": NotRequired[str],
    },
)
CreateJsonClassifierRequestTypeDef = TypedDict(
    "CreateJsonClassifierRequestTypeDef",
    {
        "Name": str,
        "JsonPath": str,
    },
)
CreateXMLClassifierRequestTypeDef = TypedDict(
    "CreateXMLClassifierRequestTypeDef",
    {
        "Classification": str,
        "Name": str,
        "RowTag": NotRequired[str],
    },
)
CreateCustomEntityTypeRequestRequestTypeDef = TypedDict(
    "CreateCustomEntityTypeRequestRequestTypeDef",
    {
        "Name": str,
        "RegexString": str,
        "ContextWords": NotRequired[Sequence[str]],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
DataQualityTargetTableTypeDef = TypedDict(
    "DataQualityTargetTableTypeDef",
    {
        "TableName": str,
        "DatabaseName": str,
        "CatalogId": NotRequired[str],
    },
)
CreateDevEndpointRequestRequestTypeDef = TypedDict(
    "CreateDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
        "RoleArn": str,
        "SecurityGroupIds": NotRequired[Sequence[str]],
        "SubnetId": NotRequired[str],
        "PublicKey": NotRequired[str],
        "PublicKeys": NotRequired[Sequence[str]],
        "NumberOfNodes": NotRequired[int],
        "WorkerType": NotRequired[WorkerTypeType],
        "GlueVersion": NotRequired[str],
        "NumberOfWorkers": NotRequired[int],
        "ExtraPythonLibsS3Path": NotRequired[str],
        "ExtraJarsS3Path": NotRequired[str],
        "SecurityConfiguration": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
        "Arguments": NotRequired[Mapping[str, str]],
    },
)
ExecutionPropertyTypeDef = TypedDict(
    "ExecutionPropertyTypeDef",
    {
        "MaxConcurrentRuns": NotRequired[int],
    },
)
JobCommandTypeDef = TypedDict(
    "JobCommandTypeDef",
    {
        "Name": NotRequired[str],
        "ScriptLocation": NotRequired[str],
        "PythonVersion": NotRequired[str],
        "Runtime": NotRequired[str],
    },
)
SourceControlDetailsTypeDef = TypedDict(
    "SourceControlDetailsTypeDef",
    {
        "Provider": NotRequired[SourceControlProviderType],
        "Repository": NotRequired[str],
        "Owner": NotRequired[str],
        "Branch": NotRequired[str],
        "Folder": NotRequired[str],
        "LastCommitId": NotRequired[str],
        "AuthStrategy": NotRequired[SourceControlAuthStrategyType],
        "AuthToken": NotRequired[str],
    },
)
PartitionIndexTypeDef = TypedDict(
    "PartitionIndexTypeDef",
    {
        "Keys": Sequence[str],
        "IndexName": str,
    },
)
CreateRegistryInputRequestTypeDef = TypedDict(
    "CreateRegistryInputRequestTypeDef",
    {
        "RegistryName": str,
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
RegistryIdTypeDef = TypedDict(
    "RegistryIdTypeDef",
    {
        "RegistryName": NotRequired[str],
        "RegistryArn": NotRequired[str],
    },
)
SessionCommandTypeDef = TypedDict(
    "SessionCommandTypeDef",
    {
        "Name": NotRequired[str],
        "PythonVersion": NotRequired[str],
    },
)
TableOptimizerConfigurationTypeDef = TypedDict(
    "TableOptimizerConfigurationTypeDef",
    {
        "roleArn": NotRequired[str],
        "enabled": NotRequired[bool],
    },
)
EventBatchingConditionTypeDef = TypedDict(
    "EventBatchingConditionTypeDef",
    {
        "BatchSize": int,
        "BatchWindow": NotRequired[int],
    },
)
CreateWorkflowRequestRequestTypeDef = TypedDict(
    "CreateWorkflowRequestRequestTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "DefaultRunProperties": NotRequired[Mapping[str, str]],
        "Tags": NotRequired[Mapping[str, str]],
        "MaxConcurrentRuns": NotRequired[int],
    },
)
DQResultsPublishingOptionsTypeDef = TypedDict(
    "DQResultsPublishingOptionsTypeDef",
    {
        "EvaluationContext": NotRequired[str],
        "ResultsS3Prefix": NotRequired[str],
        "CloudWatchMetricsEnabled": NotRequired[bool],
        "ResultsPublishingEnabled": NotRequired[bool],
    },
)
DQStopJobOnFailureOptionsTypeDef = TypedDict(
    "DQStopJobOnFailureOptionsTypeDef",
    {
        "StopJobOnFailureTiming": NotRequired[DQStopJobOnFailureTimingType],
    },
)
EncryptionAtRestTypeDef = TypedDict(
    "EncryptionAtRestTypeDef",
    {
        "CatalogEncryptionMode": CatalogEncryptionModeType,
        "SseAwsKmsKeyId": NotRequired[str],
        "CatalogEncryptionServiceRole": NotRequired[str],
    },
)
DataLakePrincipalTypeDef = TypedDict(
    "DataLakePrincipalTypeDef",
    {
        "DataLakePrincipalIdentifier": NotRequired[str],
    },
)
DataQualityAnalyzerResultTypeDef = TypedDict(
    "DataQualityAnalyzerResultTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "EvaluationMessage": NotRequired[str],
        "EvaluatedMetrics": NotRequired[Dict[str, float]],
    },
)
DataQualityEvaluationRunAdditionalRunOptionsTypeDef = TypedDict(
    "DataQualityEvaluationRunAdditionalRunOptionsTypeDef",
    {
        "CloudWatchMetricsEnabled": NotRequired[bool],
        "ResultsS3Prefix": NotRequired[str],
        "CompositeRuleEvaluationMethod": NotRequired[DQCompositeRuleEvaluationMethodType],
    },
)
DataQualityMetricValuesTypeDef = TypedDict(
    "DataQualityMetricValuesTypeDef",
    {
        "ActualValue": NotRequired[float],
        "ExpectedValue": NotRequired[float],
        "LowerLimit": NotRequired[float],
        "UpperLimit": NotRequired[float],
    },
)
DataQualityRuleResultTypeDef = TypedDict(
    "DataQualityRuleResultTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "EvaluationMessage": NotRequired[str],
        "Result": NotRequired[DataQualityRuleResultStatusType],
        "EvaluatedMetrics": NotRequired[Dict[str, float]],
    },
)
GlueTableOutputTypeDef = TypedDict(
    "GlueTableOutputTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "AdditionalOptions": NotRequired[Dict[str, str]],
    },
)
GlueTableTypeDef = TypedDict(
    "GlueTableTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "AdditionalOptions": NotRequired[Mapping[str, str]],
    },
)
DatabaseIdentifierTypeDef = TypedDict(
    "DatabaseIdentifierTypeDef",
    {
        "CatalogId": NotRequired[str],
        "DatabaseName": NotRequired[str],
        "Region": NotRequired[str],
    },
)
FederatedDatabaseTypeDef = TypedDict(
    "FederatedDatabaseTypeDef",
    {
        "Identifier": NotRequired[str],
        "ConnectionName": NotRequired[str],
    },
)
DatatypeTypeDef = TypedDict(
    "DatatypeTypeDef",
    {
        "Id": str,
        "Label": str,
    },
)
DecimalNumberOutputTypeDef = TypedDict(
    "DecimalNumberOutputTypeDef",
    {
        "UnscaledValue": bytes,
        "Scale": int,
    },
)
DeleteBlueprintRequestRequestTypeDef = TypedDict(
    "DeleteBlueprintRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteClassifierRequestRequestTypeDef = TypedDict(
    "DeleteClassifierRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "DeleteColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "ColumnName": str,
        "CatalogId": NotRequired[str],
    },
)
DeleteColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "DeleteColumnStatisticsForTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "ColumnName": str,
        "CatalogId": NotRequired[str],
    },
)
DeleteConnectionRequestRequestTypeDef = TypedDict(
    "DeleteConnectionRequestRequestTypeDef",
    {
        "ConnectionName": str,
        "CatalogId": NotRequired[str],
    },
)
DeleteCrawlerRequestRequestTypeDef = TypedDict(
    "DeleteCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteCustomEntityTypeRequestRequestTypeDef = TypedDict(
    "DeleteCustomEntityTypeRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteDataQualityRulesetRequestRequestTypeDef = TypedDict(
    "DeleteDataQualityRulesetRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteDatabaseRequestRequestTypeDef = TypedDict(
    "DeleteDatabaseRequestRequestTypeDef",
    {
        "Name": str,
        "CatalogId": NotRequired[str],
    },
)
DeleteDevEndpointRequestRequestTypeDef = TypedDict(
    "DeleteDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
    },
)
DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
)
DeleteMLTransformRequestRequestTypeDef = TypedDict(
    "DeleteMLTransformRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)
DeletePartitionIndexRequestRequestTypeDef = TypedDict(
    "DeletePartitionIndexRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "IndexName": str,
        "CatalogId": NotRequired[str],
    },
)
DeletePartitionRequestRequestTypeDef = TypedDict(
    "DeletePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "CatalogId": NotRequired[str],
    },
)
DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "PolicyHashCondition": NotRequired[str],
        "ResourceArn": NotRequired[str],
    },
)
SchemaIdTypeDef = TypedDict(
    "SchemaIdTypeDef",
    {
        "SchemaArn": NotRequired[str],
        "SchemaName": NotRequired[str],
        "RegistryName": NotRequired[str],
    },
)
DeleteSecurityConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteSecurityConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteSessionRequestRequestTypeDef = TypedDict(
    "DeleteSessionRequestRequestTypeDef",
    {
        "Id": str,
        "RequestOrigin": NotRequired[str],
    },
)
DeleteTableOptimizerRequestRequestTypeDef = TypedDict(
    "DeleteTableOptimizerRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Type": Literal["compaction"],
    },
)
DeleteTableRequestRequestTypeDef = TypedDict(
    "DeleteTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "Name": str,
        "CatalogId": NotRequired[str],
        "TransactionId": NotRequired[str],
    },
)
DeleteTableVersionRequestRequestTypeDef = TypedDict(
    "DeleteTableVersionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "VersionId": str,
        "CatalogId": NotRequired[str],
    },
)
DeleteTriggerRequestRequestTypeDef = TypedDict(
    "DeleteTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteUsageProfileRequestRequestTypeDef = TypedDict(
    "DeleteUsageProfileRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DeleteUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "DeleteUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionName": str,
        "CatalogId": NotRequired[str],
    },
)
DeleteWorkflowRequestRequestTypeDef = TypedDict(
    "DeleteWorkflowRequestRequestTypeDef",
    {
        "Name": str,
    },
)
DevEndpointCustomLibrariesTypeDef = TypedDict(
    "DevEndpointCustomLibrariesTypeDef",
    {
        "ExtraPythonLibsS3Path": NotRequired[str],
        "ExtraJarsS3Path": NotRequired[str],
    },
)
DirectSchemaChangePolicyTypeDef = TypedDict(
    "DirectSchemaChangePolicyTypeDef",
    {
        "EnableUpdateCatalog": NotRequired[bool],
        "UpdateBehavior": NotRequired[UpdateCatalogBehaviorType],
        "Table": NotRequired[str],
        "Database": NotRequired[str],
    },
)
NullCheckBoxListTypeDef = TypedDict(
    "NullCheckBoxListTypeDef",
    {
        "IsEmpty": NotRequired[bool],
        "IsNullString": NotRequired[bool],
        "IsNegOne": NotRequired[bool],
    },
)
TransformConfigParameterExtraOutputTypeDef = TypedDict(
    "TransformConfigParameterExtraOutputTypeDef",
    {
        "Name": str,
        "Type": ParamTypeType,
        "ValidationRule": NotRequired[str],
        "ValidationMessage": NotRequired[str],
        "Value": NotRequired[List[str]],
        "ListType": NotRequired[ParamTypeType],
        "IsOptional": NotRequired[bool],
    },
)
TransformConfigParameterOutputTypeDef = TypedDict(
    "TransformConfigParameterOutputTypeDef",
    {
        "Name": str,
        "Type": ParamTypeType,
        "ValidationRule": NotRequired[str],
        "ValidationMessage": NotRequired[str],
        "Value": NotRequired[List[str]],
        "ListType": NotRequired[ParamTypeType],
        "IsOptional": NotRequired[bool],
    },
)
TransformConfigParameterTypeDef = TypedDict(
    "TransformConfigParameterTypeDef",
    {
        "Name": str,
        "Type": ParamTypeType,
        "ValidationRule": NotRequired[str],
        "ValidationMessage": NotRequired[str],
        "Value": NotRequired[Sequence[str]],
        "ListType": NotRequired[ParamTypeType],
        "IsOptional": NotRequired[bool],
    },
)
EdgeTypeDef = TypedDict(
    "EdgeTypeDef",
    {
        "SourceId": NotRequired[str],
        "DestinationId": NotRequired[str],
    },
)
JobBookmarksEncryptionTypeDef = TypedDict(
    "JobBookmarksEncryptionTypeDef",
    {
        "JobBookmarksEncryptionMode": NotRequired[JobBookmarksEncryptionModeType],
        "KmsKeyArn": NotRequired[str],
    },
)
S3EncryptionTypeDef = TypedDict(
    "S3EncryptionTypeDef",
    {
        "S3EncryptionMode": NotRequired[S3EncryptionModeType],
        "KmsKeyArn": NotRequired[str],
    },
)
ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "ErrorCode": NotRequired[str],
        "ErrorMessage": NotRequired[str],
    },
)
ExportLabelsTaskRunPropertiesTypeDef = TypedDict(
    "ExportLabelsTaskRunPropertiesTypeDef",
    {
        "OutputS3Path": NotRequired[str],
    },
)
FederatedTableTypeDef = TypedDict(
    "FederatedTableTypeDef",
    {
        "Identifier": NotRequired[str],
        "DatabaseIdentifier": NotRequired[str],
        "ConnectionName": NotRequired[str],
    },
)
FilterValueExtraOutputTypeDef = TypedDict(
    "FilterValueExtraOutputTypeDef",
    {
        "Type": FilterValueTypeType,
        "Value": List[str],
    },
)
FilterValueOutputTypeDef = TypedDict(
    "FilterValueOutputTypeDef",
    {
        "Type": FilterValueTypeType,
        "Value": List[str],
    },
)
FilterValueTypeDef = TypedDict(
    "FilterValueTypeDef",
    {
        "Type": FilterValueTypeType,
        "Value": Sequence[str],
    },
)
FindMatchesParametersTypeDef = TypedDict(
    "FindMatchesParametersTypeDef",
    {
        "PrimaryKeyColumnName": NotRequired[str],
        "PrecisionRecallTradeoff": NotRequired[float],
        "AccuracyCostTradeoff": NotRequired[float],
        "EnforceProvidedLabels": NotRequired[bool],
    },
)
FindMatchesTaskRunPropertiesTypeDef = TypedDict(
    "FindMatchesTaskRunPropertiesTypeDef",
    {
        "JobId": NotRequired[str],
        "JobName": NotRequired[str],
        "JobRunId": NotRequired[str],
    },
)
GetBlueprintRequestRequestTypeDef = TypedDict(
    "GetBlueprintRequestRequestTypeDef",
    {
        "Name": str,
        "IncludeBlueprint": NotRequired[bool],
        "IncludeParameterSpec": NotRequired[bool],
    },
)
GetBlueprintRunRequestRequestTypeDef = TypedDict(
    "GetBlueprintRunRequestRequestTypeDef",
    {
        "BlueprintName": str,
        "RunId": str,
    },
)
GetBlueprintRunsRequestRequestTypeDef = TypedDict(
    "GetBlueprintRunsRequestRequestTypeDef",
    {
        "BlueprintName": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GetCatalogImportStatusRequestRequestTypeDef = TypedDict(
    "GetCatalogImportStatusRequestRequestTypeDef",
    {
        "CatalogId": NotRequired[str],
    },
)
GetClassifierRequestRequestTypeDef = TypedDict(
    "GetClassifierRequestRequestTypeDef",
    {
        "Name": str,
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
GetClassifiersRequestRequestTypeDef = TypedDict(
    "GetClassifiersRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
GetColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "GetColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "ColumnNames": Sequence[str],
        "CatalogId": NotRequired[str],
    },
)
GetColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "GetColumnStatisticsForTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "ColumnNames": Sequence[str],
        "CatalogId": NotRequired[str],
    },
)
GetColumnStatisticsTaskRunRequestRequestTypeDef = TypedDict(
    "GetColumnStatisticsTaskRunRequestRequestTypeDef",
    {
        "ColumnStatisticsTaskRunId": str,
    },
)
GetColumnStatisticsTaskRunsRequestRequestTypeDef = TypedDict(
    "GetColumnStatisticsTaskRunsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
GetConnectionRequestRequestTypeDef = TypedDict(
    "GetConnectionRequestRequestTypeDef",
    {
        "Name": str,
        "CatalogId": NotRequired[str],
        "HidePassword": NotRequired[bool],
    },
)
GetConnectionsFilterTypeDef = TypedDict(
    "GetConnectionsFilterTypeDef",
    {
        "MatchCriteria": NotRequired[Sequence[str]],
        "ConnectionType": NotRequired[ConnectionTypeType],
    },
)
GetCrawlerMetricsRequestRequestTypeDef = TypedDict(
    "GetCrawlerMetricsRequestRequestTypeDef",
    {
        "CrawlerNameList": NotRequired[Sequence[str]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
GetCrawlerRequestRequestTypeDef = TypedDict(
    "GetCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
GetCrawlersRequestRequestTypeDef = TypedDict(
    "GetCrawlersRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
GetCustomEntityTypeRequestRequestTypeDef = TypedDict(
    "GetCustomEntityTypeRequestRequestTypeDef",
    {
        "Name": str,
    },
)
GetDataCatalogEncryptionSettingsRequestRequestTypeDef = TypedDict(
    "GetDataCatalogEncryptionSettingsRequestRequestTypeDef",
    {
        "CatalogId": NotRequired[str],
    },
)
GetDataQualityResultRequestRequestTypeDef = TypedDict(
    "GetDataQualityResultRequestRequestTypeDef",
    {
        "ResultId": str,
    },
)
GetDataQualityRuleRecommendationRunRequestRequestTypeDef = TypedDict(
    "GetDataQualityRuleRecommendationRunRequestRequestTypeDef",
    {
        "RunId": str,
    },
)
GetDataQualityRulesetEvaluationRunRequestRequestTypeDef = TypedDict(
    "GetDataQualityRulesetEvaluationRunRequestRequestTypeDef",
    {
        "RunId": str,
    },
)
GetDataQualityRulesetRequestRequestTypeDef = TypedDict(
    "GetDataQualityRulesetRequestRequestTypeDef",
    {
        "Name": str,
    },
)
GetDatabaseRequestRequestTypeDef = TypedDict(
    "GetDatabaseRequestRequestTypeDef",
    {
        "Name": str,
        "CatalogId": NotRequired[str],
    },
)
GetDatabasesRequestRequestTypeDef = TypedDict(
    "GetDatabasesRequestRequestTypeDef",
    {
        "CatalogId": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "ResourceShareType": NotRequired[ResourceShareTypeType],
    },
)
GetDataflowGraphRequestRequestTypeDef = TypedDict(
    "GetDataflowGraphRequestRequestTypeDef",
    {
        "PythonScript": NotRequired[str],
    },
)
GetDevEndpointRequestRequestTypeDef = TypedDict(
    "GetDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
    },
)
GetDevEndpointsRequestRequestTypeDef = TypedDict(
    "GetDevEndpointsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
GetJobBookmarkRequestRequestTypeDef = TypedDict(
    "GetJobBookmarkRequestRequestTypeDef",
    {
        "JobName": str,
        "RunId": NotRequired[str],
    },
)
JobBookmarkEntryTypeDef = TypedDict(
    "JobBookmarkEntryTypeDef",
    {
        "JobName": NotRequired[str],
        "Version": NotRequired[int],
        "Run": NotRequired[int],
        "Attempt": NotRequired[int],
        "PreviousRunId": NotRequired[str],
        "RunId": NotRequired[str],
        "JobBookmark": NotRequired[str],
    },
)
GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "JobName": str,
    },
)
GetJobRunRequestRequestTypeDef = TypedDict(
    "GetJobRunRequestRequestTypeDef",
    {
        "JobName": str,
        "RunId": str,
        "PredecessorsIncluded": NotRequired[bool],
    },
)
GetJobRunsRequestRequestTypeDef = TypedDict(
    "GetJobRunsRequestRequestTypeDef",
    {
        "JobName": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GetJobsRequestRequestTypeDef = TypedDict(
    "GetJobsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GetMLTaskRunRequestRequestTypeDef = TypedDict(
    "GetMLTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
    },
)
TaskRunSortCriteriaTypeDef = TypedDict(
    "TaskRunSortCriteriaTypeDef",
    {
        "Column": TaskRunSortColumnTypeType,
        "SortDirection": SortDirectionTypeType,
    },
)
GetMLTransformRequestRequestTypeDef = TypedDict(
    "GetMLTransformRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)
SchemaColumnTypeDef = TypedDict(
    "SchemaColumnTypeDef",
    {
        "Name": NotRequired[str],
        "DataType": NotRequired[str],
    },
)
TransformSortCriteriaTypeDef = TypedDict(
    "TransformSortCriteriaTypeDef",
    {
        "Column": TransformSortColumnTypeType,
        "SortDirection": SortDirectionTypeType,
    },
)
MappingEntryTypeDef = TypedDict(
    "MappingEntryTypeDef",
    {
        "SourceTable": NotRequired[str],
        "SourcePath": NotRequired[str],
        "SourceType": NotRequired[str],
        "TargetTable": NotRequired[str],
        "TargetPath": NotRequired[str],
        "TargetType": NotRequired[str],
    },
)
GetPartitionIndexesRequestRequestTypeDef = TypedDict(
    "GetPartitionIndexesRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "NextToken": NotRequired[str],
    },
)
GetPartitionRequestRequestTypeDef = TypedDict(
    "GetPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "CatalogId": NotRequired[str],
    },
)
SegmentTypeDef = TypedDict(
    "SegmentTypeDef",
    {
        "SegmentNumber": int,
        "TotalSegments": int,
    },
)
GetResourcePoliciesRequestRequestTypeDef = TypedDict(
    "GetResourcePoliciesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GluePolicyTypeDef = TypedDict(
    "GluePolicyTypeDef",
    {
        "PolicyInJson": NotRequired[str],
        "PolicyHash": NotRequired[str],
        "CreateTime": NotRequired[datetime],
        "UpdateTime": NotRequired[datetime],
    },
)
GetResourcePolicyRequestRequestTypeDef = TypedDict(
    "GetResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": NotRequired[str],
    },
)
SchemaVersionNumberTypeDef = TypedDict(
    "SchemaVersionNumberTypeDef",
    {
        "LatestVersion": NotRequired[bool],
        "VersionNumber": NotRequired[int],
    },
)
GetSecurityConfigurationRequestRequestTypeDef = TypedDict(
    "GetSecurityConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
GetSecurityConfigurationsRequestRequestTypeDef = TypedDict(
    "GetSecurityConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
GetSessionRequestRequestTypeDef = TypedDict(
    "GetSessionRequestRequestTypeDef",
    {
        "Id": str,
        "RequestOrigin": NotRequired[str],
    },
)
GetStatementRequestRequestTypeDef = TypedDict(
    "GetStatementRequestRequestTypeDef",
    {
        "SessionId": str,
        "Id": int,
        "RequestOrigin": NotRequired[str],
    },
)
GetTableOptimizerRequestRequestTypeDef = TypedDict(
    "GetTableOptimizerRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Type": Literal["compaction"],
    },
)
GetTableVersionRequestRequestTypeDef = TypedDict(
    "GetTableVersionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "VersionId": NotRequired[str],
    },
)
GetTableVersionsRequestRequestTypeDef = TypedDict(
    "GetTableVersionsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GetTagsRequestRequestTypeDef = TypedDict(
    "GetTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
GetTriggerRequestRequestTypeDef = TypedDict(
    "GetTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
GetTriggersRequestRequestTypeDef = TypedDict(
    "GetTriggersRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "DependentJobName": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
SupportedDialectTypeDef = TypedDict(
    "SupportedDialectTypeDef",
    {
        "Dialect": NotRequired[ViewDialectType],
        "DialectVersion": NotRequired[str],
    },
)
GetUsageProfileRequestRequestTypeDef = TypedDict(
    "GetUsageProfileRequestRequestTypeDef",
    {
        "Name": str,
    },
)
GetUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "GetUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionName": str,
        "CatalogId": NotRequired[str],
    },
)
GetUserDefinedFunctionsRequestRequestTypeDef = TypedDict(
    "GetUserDefinedFunctionsRequestRequestTypeDef",
    {
        "Pattern": str,
        "CatalogId": NotRequired[str],
        "DatabaseName": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GetWorkflowRequestRequestTypeDef = TypedDict(
    "GetWorkflowRequestRequestTypeDef",
    {
        "Name": str,
        "IncludeGraph": NotRequired[bool],
    },
)
GetWorkflowRunPropertiesRequestRequestTypeDef = TypedDict(
    "GetWorkflowRunPropertiesRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
    },
)
GetWorkflowRunRequestRequestTypeDef = TypedDict(
    "GetWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
        "IncludeGraph": NotRequired[bool],
    },
)
GetWorkflowRunsRequestRequestTypeDef = TypedDict(
    "GetWorkflowRunsRequestRequestTypeDef",
    {
        "Name": str,
        "IncludeGraph": NotRequired[bool],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GlueStudioSchemaColumnTypeDef = TypedDict(
    "GlueStudioSchemaColumnTypeDef",
    {
        "Name": str,
        "Type": NotRequired[str],
    },
)
S3SourceAdditionalOptionsTypeDef = TypedDict(
    "S3SourceAdditionalOptionsTypeDef",
    {
        "BoundedSize": NotRequired[int],
        "BoundedFiles": NotRequired[int],
    },
)
IcebergInputTypeDef = TypedDict(
    "IcebergInputTypeDef",
    {
        "MetadataOperation": Literal["CREATE"],
        "Version": NotRequired[str],
    },
)
ImportCatalogToGlueRequestRequestTypeDef = TypedDict(
    "ImportCatalogToGlueRequestRequestTypeDef",
    {
        "CatalogId": NotRequired[str],
    },
)
ImportLabelsTaskRunPropertiesTypeDef = TypedDict(
    "ImportLabelsTaskRunPropertiesTypeDef",
    {
        "InputS3Path": NotRequired[str],
        "Replace": NotRequired[bool],
    },
)
JDBCConnectorOptionsExtraOutputTypeDef = TypedDict(
    "JDBCConnectorOptionsExtraOutputTypeDef",
    {
        "FilterPredicate": NotRequired[str],
        "PartitionColumn": NotRequired[str],
        "LowerBound": NotRequired[int],
        "UpperBound": NotRequired[int],
        "NumPartitions": NotRequired[int],
        "JobBookmarkKeys": NotRequired[List[str]],
        "JobBookmarkKeysSortOrder": NotRequired[str],
        "DataTypeMapping": NotRequired[Dict[JDBCDataTypeType, GlueRecordTypeType]],
    },
)
JDBCConnectorOptionsOutputTypeDef = TypedDict(
    "JDBCConnectorOptionsOutputTypeDef",
    {
        "FilterPredicate": NotRequired[str],
        "PartitionColumn": NotRequired[str],
        "LowerBound": NotRequired[int],
        "UpperBound": NotRequired[int],
        "NumPartitions": NotRequired[int],
        "JobBookmarkKeys": NotRequired[List[str]],
        "JobBookmarkKeysSortOrder": NotRequired[str],
        "DataTypeMapping": NotRequired[Dict[JDBCDataTypeType, GlueRecordTypeType]],
    },
)
JDBCConnectorOptionsTypeDef = TypedDict(
    "JDBCConnectorOptionsTypeDef",
    {
        "FilterPredicate": NotRequired[str],
        "PartitionColumn": NotRequired[str],
        "LowerBound": NotRequired[int],
        "UpperBound": NotRequired[int],
        "NumPartitions": NotRequired[int],
        "JobBookmarkKeys": NotRequired[Sequence[str]],
        "JobBookmarkKeysSortOrder": NotRequired[str],
        "DataTypeMapping": NotRequired[Mapping[JDBCDataTypeType, GlueRecordTypeType]],
    },
)
PredecessorTypeDef = TypedDict(
    "PredecessorTypeDef",
    {
        "JobName": NotRequired[str],
        "RunId": NotRequired[str],
    },
)
JoinColumnExtraOutputTypeDef = TypedDict(
    "JoinColumnExtraOutputTypeDef",
    {
        "From": str,
        "Keys": List[List[str]],
    },
)
JoinColumnOutputTypeDef = TypedDict(
    "JoinColumnOutputTypeDef",
    {
        "From": str,
        "Keys": List[List[str]],
    },
)
JoinColumnTypeDef = TypedDict(
    "JoinColumnTypeDef",
    {
        "From": str,
        "Keys": Sequence[Sequence[str]],
    },
)
KeySchemaElementTypeDef = TypedDict(
    "KeySchemaElementTypeDef",
    {
        "Name": str,
        "Type": str,
    },
)
LabelingSetGenerationTaskRunPropertiesTypeDef = TypedDict(
    "LabelingSetGenerationTaskRunPropertiesTypeDef",
    {
        "OutputS3Path": NotRequired[str],
    },
)
ListBlueprintsRequestRequestTypeDef = TypedDict(
    "ListBlueprintsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ListColumnStatisticsTaskRunsRequestRequestTypeDef = TypedDict(
    "ListColumnStatisticsTaskRunsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListCrawlersRequestRequestTypeDef = TypedDict(
    "ListCrawlersRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ListCustomEntityTypesRequestRequestTypeDef = TypedDict(
    "ListCustomEntityTypesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ListDevEndpointsRequestRequestTypeDef = TypedDict(
    "ListDevEndpointsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ListRegistriesInputRequestTypeDef = TypedDict(
    "ListRegistriesInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
RegistryListItemTypeDef = TypedDict(
    "RegistryListItemTypeDef",
    {
        "RegistryName": NotRequired[str],
        "RegistryArn": NotRequired[str],
        "Description": NotRequired[str],
        "Status": NotRequired[RegistryStatusType],
        "CreatedTime": NotRequired[str],
        "UpdatedTime": NotRequired[str],
    },
)
SchemaVersionListItemTypeDef = TypedDict(
    "SchemaVersionListItemTypeDef",
    {
        "SchemaArn": NotRequired[str],
        "SchemaVersionId": NotRequired[str],
        "VersionNumber": NotRequired[int],
        "Status": NotRequired[SchemaVersionStatusType],
        "CreatedTime": NotRequired[str],
    },
)
SchemaListItemTypeDef = TypedDict(
    "SchemaListItemTypeDef",
    {
        "RegistryName": NotRequired[str],
        "SchemaName": NotRequired[str],
        "SchemaArn": NotRequired[str],
        "Description": NotRequired[str],
        "SchemaStatus": NotRequired[SchemaStatusType],
        "CreatedTime": NotRequired[str],
        "UpdatedTime": NotRequired[str],
    },
)
ListSessionsRequestRequestTypeDef = TypedDict(
    "ListSessionsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Tags": NotRequired[Mapping[str, str]],
        "RequestOrigin": NotRequired[str],
    },
)
ListStatementsRequestRequestTypeDef = TypedDict(
    "ListStatementsRequestRequestTypeDef",
    {
        "SessionId": str,
        "RequestOrigin": NotRequired[str],
        "NextToken": NotRequired[str],
    },
)
ListTableOptimizerRunsRequestRequestTypeDef = TypedDict(
    "ListTableOptimizerRunsRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Type": Literal["compaction"],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListTriggersRequestRequestTypeDef = TypedDict(
    "ListTriggersRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "DependentJobName": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ListUsageProfilesRequestRequestTypeDef = TypedDict(
    "ListUsageProfilesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
UsageProfileDefinitionTypeDef = TypedDict(
    "UsageProfileDefinitionTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "CreatedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
    },
)
ListWorkflowsRequestRequestTypeDef = TypedDict(
    "ListWorkflowsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
MLUserDataEncryptionTypeDef = TypedDict(
    "MLUserDataEncryptionTypeDef",
    {
        "MlUserDataEncryptionMode": MLUserDataEncryptionModeStringType,
        "KmsKeyId": NotRequired[str],
    },
)
MappingExtraOutputTypeDef = TypedDict(
    "MappingExtraOutputTypeDef",
    {
        "ToKey": NotRequired[str],
        "FromPath": NotRequired[List[str]],
        "FromType": NotRequired[str],
        "ToType": NotRequired[str],
        "Dropped": NotRequired[bool],
        "Children": NotRequired[List[Dict[str, Any]]],
    },
)
MappingOutputTypeDef = TypedDict(
    "MappingOutputTypeDef",
    {
        "ToKey": NotRequired[str],
        "FromPath": NotRequired[List[str]],
        "FromType": NotRequired[str],
        "ToType": NotRequired[str],
        "Dropped": NotRequired[bool],
        "Children": NotRequired[List[Dict[str, Any]]],
    },
)
MappingTypeDef = TypedDict(
    "MappingTypeDef",
    {
        "ToKey": NotRequired[str],
        "FromPath": NotRequired[Sequence[str]],
        "FromType": NotRequired[str],
        "ToType": NotRequired[str],
        "Dropped": NotRequired[bool],
        "Children": NotRequired[Sequence[Dict[str, Any]]],
    },
)
OtherMetadataValueListItemTypeDef = TypedDict(
    "OtherMetadataValueListItemTypeDef",
    {
        "MetadataValue": NotRequired[str],
        "CreatedTime": NotRequired[str],
    },
)
MetadataKeyValuePairTypeDef = TypedDict(
    "MetadataKeyValuePairTypeDef",
    {
        "MetadataKey": NotRequired[str],
        "MetadataValue": NotRequired[str],
    },
)
OAuth2ClientApplicationTypeDef = TypedDict(
    "OAuth2ClientApplicationTypeDef",
    {
        "UserManagedClientApplicationClientId": NotRequired[str],
        "AWSManagedClientApplicationReference": NotRequired[str],
    },
)
OrderTypeDef = TypedDict(
    "OrderTypeDef",
    {
        "Column": str,
        "SortOrder": int,
    },
)
PartitionValueListExtraOutputTypeDef = TypedDict(
    "PartitionValueListExtraOutputTypeDef",
    {
        "Values": List[str],
    },
)
PartitionValueListTypeDef = TypedDict(
    "PartitionValueListTypeDef",
    {
        "Values": Sequence[str],
    },
)
PropertyPredicateTypeDef = TypedDict(
    "PropertyPredicateTypeDef",
    {
        "Key": NotRequired[str],
        "Value": NotRequired[str],
        "Comparator": NotRequired[ComparatorType],
    },
)
PutResourcePolicyRequestRequestTypeDef = TypedDict(
    "PutResourcePolicyRequestRequestTypeDef",
    {
        "PolicyInJson": str,
        "ResourceArn": NotRequired[str],
        "PolicyHashCondition": NotRequired[str],
        "PolicyExistsCondition": NotRequired[ExistConditionType],
        "EnableHybrid": NotRequired[EnableHybridValuesType],
    },
)
PutWorkflowRunPropertiesRequestRequestTypeDef = TypedDict(
    "PutWorkflowRunPropertiesRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
        "RunProperties": Mapping[str, str],
    },
)
RecipeReferenceTypeDef = TypedDict(
    "RecipeReferenceTypeDef",
    {
        "RecipeArn": str,
        "RecipeVersion": str,
    },
)
UpsertRedshiftTargetOptionsExtraOutputTypeDef = TypedDict(
    "UpsertRedshiftTargetOptionsExtraOutputTypeDef",
    {
        "TableLocation": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "UpsertKeys": NotRequired[List[str]],
    },
)
UpsertRedshiftTargetOptionsOutputTypeDef = TypedDict(
    "UpsertRedshiftTargetOptionsOutputTypeDef",
    {
        "TableLocation": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "UpsertKeys": NotRequired[List[str]],
    },
)
UpsertRedshiftTargetOptionsTypeDef = TypedDict(
    "UpsertRedshiftTargetOptionsTypeDef",
    {
        "TableLocation": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "UpsertKeys": NotRequired[Sequence[str]],
    },
)
ResetJobBookmarkRequestRequestTypeDef = TypedDict(
    "ResetJobBookmarkRequestRequestTypeDef",
    {
        "JobName": str,
        "RunId": NotRequired[str],
    },
)
ResourceUriTypeDef = TypedDict(
    "ResourceUriTypeDef",
    {
        "ResourceType": NotRequired[ResourceTypeType],
        "Uri": NotRequired[str],
    },
)
ResumeWorkflowRunRequestRequestTypeDef = TypedDict(
    "ResumeWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
        "NodeIds": Sequence[str],
    },
)
RunMetricsTypeDef = TypedDict(
    "RunMetricsTypeDef",
    {
        "NumberOfBytesCompacted": NotRequired[str],
        "NumberOfFilesCompacted": NotRequired[str],
        "NumberOfDpus": NotRequired[str],
        "JobDurationInHour": NotRequired[str],
    },
)
RunStatementRequestRequestTypeDef = TypedDict(
    "RunStatementRequestRequestTypeDef",
    {
        "SessionId": str,
        "Code": str,
        "RequestOrigin": NotRequired[str],
    },
)
S3DirectSourceAdditionalOptionsTypeDef = TypedDict(
    "S3DirectSourceAdditionalOptionsTypeDef",
    {
        "BoundedSize": NotRequired[int],
        "BoundedFiles": NotRequired[int],
        "EnableSamplePath": NotRequired[bool],
        "SamplePath": NotRequired[str],
    },
)
SortCriterionTypeDef = TypedDict(
    "SortCriterionTypeDef",
    {
        "FieldName": NotRequired[str],
        "Sort": NotRequired[SortType],
    },
)
SerDeInfoOutputTypeDef = TypedDict(
    "SerDeInfoOutputTypeDef",
    {
        "Name": NotRequired[str],
        "SerializationLibrary": NotRequired[str],
        "Parameters": NotRequired[Dict[str, str]],
    },
)
SerDeInfoTypeDef = TypedDict(
    "SerDeInfoTypeDef",
    {
        "Name": NotRequired[str],
        "SerializationLibrary": NotRequired[str],
        "Parameters": NotRequired[Mapping[str, str]],
    },
)
SkewedInfoOutputTypeDef = TypedDict(
    "SkewedInfoOutputTypeDef",
    {
        "SkewedColumnNames": NotRequired[List[str]],
        "SkewedColumnValues": NotRequired[List[str]],
        "SkewedColumnValueLocationMaps": NotRequired[Dict[str, str]],
    },
)
SkewedInfoTypeDef = TypedDict(
    "SkewedInfoTypeDef",
    {
        "SkewedColumnNames": NotRequired[Sequence[str]],
        "SkewedColumnValues": NotRequired[Sequence[str]],
        "SkewedColumnValueLocationMaps": NotRequired[Mapping[str, str]],
    },
)
SqlAliasTypeDef = TypedDict(
    "SqlAliasTypeDef",
    {
        "From": str,
        "Alias": str,
    },
)
StartBlueprintRunRequestRequestTypeDef = TypedDict(
    "StartBlueprintRunRequestRequestTypeDef",
    {
        "BlueprintName": str,
        "RoleArn": str,
        "Parameters": NotRequired[str],
    },
)
StartColumnStatisticsTaskRunRequestRequestTypeDef = TypedDict(
    "StartColumnStatisticsTaskRunRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "Role": str,
        "ColumnNameList": NotRequired[Sequence[str]],
        "SampleSize": NotRequired[float],
        "CatalogID": NotRequired[str],
        "SecurityConfiguration": NotRequired[str],
    },
)
StartCrawlerRequestRequestTypeDef = TypedDict(
    "StartCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
StartCrawlerScheduleRequestRequestTypeDef = TypedDict(
    "StartCrawlerScheduleRequestRequestTypeDef",
    {
        "CrawlerName": str,
    },
)
StartExportLabelsTaskRunRequestRequestTypeDef = TypedDict(
    "StartExportLabelsTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "OutputS3Path": str,
    },
)
StartImportLabelsTaskRunRequestRequestTypeDef = TypedDict(
    "StartImportLabelsTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "InputS3Path": str,
        "ReplaceAllLabels": NotRequired[bool],
    },
)
StartMLEvaluationTaskRunRequestRequestTypeDef = TypedDict(
    "StartMLEvaluationTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
    },
)
StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef = TypedDict(
    "StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef",
    {
        "TransformId": str,
        "OutputS3Path": str,
    },
)
StartTriggerRequestRequestTypeDef = TypedDict(
    "StartTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
StartWorkflowRunRequestRequestTypeDef = TypedDict(
    "StartWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunProperties": NotRequired[Mapping[str, str]],
    },
)
StartingEventBatchConditionTypeDef = TypedDict(
    "StartingEventBatchConditionTypeDef",
    {
        "BatchSize": NotRequired[int],
        "BatchWindow": NotRequired[int],
    },
)
StatementOutputDataTypeDef = TypedDict(
    "StatementOutputDataTypeDef",
    {
        "TextPlain": NotRequired[str],
    },
)
StopColumnStatisticsTaskRunRequestRequestTypeDef = TypedDict(
    "StopColumnStatisticsTaskRunRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
StopCrawlerRequestRequestTypeDef = TypedDict(
    "StopCrawlerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
StopCrawlerScheduleRequestRequestTypeDef = TypedDict(
    "StopCrawlerScheduleRequestRequestTypeDef",
    {
        "CrawlerName": str,
    },
)
StopSessionRequestRequestTypeDef = TypedDict(
    "StopSessionRequestRequestTypeDef",
    {
        "Id": str,
        "RequestOrigin": NotRequired[str],
    },
)
StopTriggerRequestRequestTypeDef = TypedDict(
    "StopTriggerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
StopWorkflowRunRequestRequestTypeDef = TypedDict(
    "StopWorkflowRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
    },
)
TableIdentifierTypeDef = TypedDict(
    "TableIdentifierTypeDef",
    {
        "CatalogId": NotRequired[str],
        "DatabaseName": NotRequired[str],
        "Name": NotRequired[str],
        "Region": NotRequired[str],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagsToAdd": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagsToRemove": Sequence[str],
    },
)
UpdateBlueprintRequestRequestTypeDef = TypedDict(
    "UpdateBlueprintRequestRequestTypeDef",
    {
        "Name": str,
        "BlueprintLocation": str,
        "Description": NotRequired[str],
    },
)
UpdateCsvClassifierRequestTypeDef = TypedDict(
    "UpdateCsvClassifierRequestTypeDef",
    {
        "Name": str,
        "Delimiter": NotRequired[str],
        "QuoteSymbol": NotRequired[str],
        "ContainsHeader": NotRequired[CsvHeaderOptionType],
        "Header": NotRequired[Sequence[str]],
        "DisableValueTrimming": NotRequired[bool],
        "AllowSingleColumn": NotRequired[bool],
        "CustomDatatypeConfigured": NotRequired[bool],
        "CustomDatatypes": NotRequired[Sequence[str]],
        "Serde": NotRequired[CsvSerdeOptionType],
    },
)
UpdateGrokClassifierRequestTypeDef = TypedDict(
    "UpdateGrokClassifierRequestTypeDef",
    {
        "Name": str,
        "Classification": NotRequired[str],
        "GrokPattern": NotRequired[str],
        "CustomPatterns": NotRequired[str],
    },
)
UpdateJsonClassifierRequestTypeDef = TypedDict(
    "UpdateJsonClassifierRequestTypeDef",
    {
        "Name": str,
        "JsonPath": NotRequired[str],
    },
)
UpdateXMLClassifierRequestTypeDef = TypedDict(
    "UpdateXMLClassifierRequestTypeDef",
    {
        "Name": str,
        "Classification": NotRequired[str],
        "RowTag": NotRequired[str],
    },
)
UpdateCrawlerScheduleRequestRequestTypeDef = TypedDict(
    "UpdateCrawlerScheduleRequestRequestTypeDef",
    {
        "CrawlerName": str,
        "Schedule": NotRequired[str],
    },
)
UpdateDataQualityRulesetRequestRequestTypeDef = TypedDict(
    "UpdateDataQualityRulesetRequestRequestTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "Ruleset": NotRequired[str],
    },
)
UpdateJobFromSourceControlRequestRequestTypeDef = TypedDict(
    "UpdateJobFromSourceControlRequestRequestTypeDef",
    {
        "JobName": NotRequired[str],
        "Provider": NotRequired[SourceControlProviderType],
        "RepositoryName": NotRequired[str],
        "RepositoryOwner": NotRequired[str],
        "BranchName": NotRequired[str],
        "Folder": NotRequired[str],
        "CommitId": NotRequired[str],
        "AuthStrategy": NotRequired[SourceControlAuthStrategyType],
        "AuthToken": NotRequired[str],
    },
)
UpdateSourceControlFromJobRequestRequestTypeDef = TypedDict(
    "UpdateSourceControlFromJobRequestRequestTypeDef",
    {
        "JobName": NotRequired[str],
        "Provider": NotRequired[SourceControlProviderType],
        "RepositoryName": NotRequired[str],
        "RepositoryOwner": NotRequired[str],
        "BranchName": NotRequired[str],
        "Folder": NotRequired[str],
        "CommitId": NotRequired[str],
        "AuthStrategy": NotRequired[SourceControlAuthStrategyType],
        "AuthToken": NotRequired[str],
    },
)
UpdateWorkflowRequestRequestTypeDef = TypedDict(
    "UpdateWorkflowRequestRequestTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "DefaultRunProperties": NotRequired[Mapping[str, str]],
        "MaxConcurrentRuns": NotRequired[int],
    },
)
ViewRepresentationInputTypeDef = TypedDict(
    "ViewRepresentationInputTypeDef",
    {
        "Dialect": NotRequired[ViewDialectType],
        "DialectVersion": NotRequired[str],
        "ViewOriginalText": NotRequired[str],
        "ValidationConnection": NotRequired[str],
        "ViewExpandedText": NotRequired[str],
    },
)
ViewRepresentationTypeDef = TypedDict(
    "ViewRepresentationTypeDef",
    {
        "Dialect": NotRequired[ViewDialectType],
        "DialectVersion": NotRequired[str],
        "ViewOriginalText": NotRequired[str],
        "ViewExpandedText": NotRequired[str],
        "ValidationConnection": NotRequired[str],
        "IsStale": NotRequired[bool],
    },
)
WorkflowRunStatisticsTypeDef = TypedDict(
    "WorkflowRunStatisticsTypeDef",
    {
        "TotalActions": NotRequired[int],
        "TimeoutActions": NotRequired[int],
        "FailedActions": NotRequired[int],
        "StoppedActions": NotRequired[int],
        "SucceededActions": NotRequired[int],
        "RunningActions": NotRequired[int],
        "ErroredActions": NotRequired[int],
        "WaitingActions": NotRequired[int],
    },
)
ActionExtraOutputTypeDef = TypedDict(
    "ActionExtraOutputTypeDef",
    {
        "JobName": NotRequired[str],
        "Arguments": NotRequired[Dict[str, str]],
        "Timeout": NotRequired[int],
        "SecurityConfiguration": NotRequired[str],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "CrawlerName": NotRequired[str],
    },
)
ActionOutputTypeDef = TypedDict(
    "ActionOutputTypeDef",
    {
        "JobName": NotRequired[str],
        "Arguments": NotRequired[Dict[str, str]],
        "Timeout": NotRequired[int],
        "SecurityConfiguration": NotRequired[str],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "CrawlerName": NotRequired[str],
    },
)
ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "JobName": NotRequired[str],
        "Arguments": NotRequired[Mapping[str, str]],
        "Timeout": NotRequired[int],
        "SecurityConfiguration": NotRequired[str],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "CrawlerName": NotRequired[str],
    },
)
StartJobRunRequestRequestTypeDef = TypedDict(
    "StartJobRunRequestRequestTypeDef",
    {
        "JobName": str,
        "JobRunId": NotRequired[str],
        "Arguments": NotRequired[Mapping[str, str]],
        "AllocatedCapacity": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxCapacity": NotRequired[float],
        "SecurityConfiguration": NotRequired[str],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "WorkerType": NotRequired[WorkerTypeType],
        "NumberOfWorkers": NotRequired[int],
        "ExecutionClass": NotRequired[ExecutionClassType],
    },
)
AggregateExtraOutputTypeDef = TypedDict(
    "AggregateExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Groups": List[List[str]],
        "Aggs": List[AggregateOperationExtraOutputTypeDef],
    },
)
AggregateOutputTypeDef = TypedDict(
    "AggregateOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Groups": List[List[str]],
        "Aggs": List[AggregateOperationOutputTypeDef],
    },
)
AggregateTypeDef = TypedDict(
    "AggregateTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Groups": Sequence[Sequence[str]],
        "Aggs": Sequence[AggregateOperationTypeDef],
    },
)
AmazonRedshiftNodeDataExtraOutputTypeDef = TypedDict(
    "AmazonRedshiftNodeDataExtraOutputTypeDef",
    {
        "AccessType": NotRequired[str],
        "SourceType": NotRequired[str],
        "Connection": NotRequired[OptionTypeDef],
        "Schema": NotRequired[OptionTypeDef],
        "Table": NotRequired[OptionTypeDef],
        "CatalogDatabase": NotRequired[OptionTypeDef],
        "CatalogTable": NotRequired[OptionTypeDef],
        "CatalogRedshiftSchema": NotRequired[str],
        "CatalogRedshiftTable": NotRequired[str],
        "TempDir": NotRequired[str],
        "IamRole": NotRequired[OptionTypeDef],
        "AdvancedOptions": NotRequired[List[AmazonRedshiftAdvancedOptionTypeDef]],
        "SampleQuery": NotRequired[str],
        "PreAction": NotRequired[str],
        "PostAction": NotRequired[str],
        "Action": NotRequired[str],
        "TablePrefix": NotRequired[str],
        "Upsert": NotRequired[bool],
        "MergeAction": NotRequired[str],
        "MergeWhenMatched": NotRequired[str],
        "MergeWhenNotMatched": NotRequired[str],
        "MergeClause": NotRequired[str],
        "CrawlerConnection": NotRequired[str],
        "TableSchema": NotRequired[List[OptionTypeDef]],
        "StagingTable": NotRequired[str],
        "SelectedColumns": NotRequired[List[OptionTypeDef]],
    },
)
AmazonRedshiftNodeDataOutputTypeDef = TypedDict(
    "AmazonRedshiftNodeDataOutputTypeDef",
    {
        "AccessType": NotRequired[str],
        "SourceType": NotRequired[str],
        "Connection": NotRequired[OptionTypeDef],
        "Schema": NotRequired[OptionTypeDef],
        "Table": NotRequired[OptionTypeDef],
        "CatalogDatabase": NotRequired[OptionTypeDef],
        "CatalogTable": NotRequired[OptionTypeDef],
        "CatalogRedshiftSchema": NotRequired[str],
        "CatalogRedshiftTable": NotRequired[str],
        "TempDir": NotRequired[str],
        "IamRole": NotRequired[OptionTypeDef],
        "AdvancedOptions": NotRequired[List[AmazonRedshiftAdvancedOptionTypeDef]],
        "SampleQuery": NotRequired[str],
        "PreAction": NotRequired[str],
        "PostAction": NotRequired[str],
        "Action": NotRequired[str],
        "TablePrefix": NotRequired[str],
        "Upsert": NotRequired[bool],
        "MergeAction": NotRequired[str],
        "MergeWhenMatched": NotRequired[str],
        "MergeWhenNotMatched": NotRequired[str],
        "MergeClause": NotRequired[str],
        "CrawlerConnection": NotRequired[str],
        "TableSchema": NotRequired[List[OptionTypeDef]],
        "StagingTable": NotRequired[str],
        "SelectedColumns": NotRequired[List[OptionTypeDef]],
    },
)
AmazonRedshiftNodeDataTypeDef = TypedDict(
    "AmazonRedshiftNodeDataTypeDef",
    {
        "AccessType": NotRequired[str],
        "SourceType": NotRequired[str],
        "Connection": NotRequired[OptionTypeDef],
        "Schema": NotRequired[OptionTypeDef],
        "Table": NotRequired[OptionTypeDef],
        "CatalogDatabase": NotRequired[OptionTypeDef],
        "CatalogTable": NotRequired[OptionTypeDef],
        "CatalogRedshiftSchema": NotRequired[str],
        "CatalogRedshiftTable": NotRequired[str],
        "TempDir": NotRequired[str],
        "IamRole": NotRequired[OptionTypeDef],
        "AdvancedOptions": NotRequired[Sequence[AmazonRedshiftAdvancedOptionTypeDef]],
        "SampleQuery": NotRequired[str],
        "PreAction": NotRequired[str],
        "PostAction": NotRequired[str],
        "Action": NotRequired[str],
        "TablePrefix": NotRequired[str],
        "Upsert": NotRequired[bool],
        "MergeAction": NotRequired[str],
        "MergeWhenMatched": NotRequired[str],
        "MergeWhenNotMatched": NotRequired[str],
        "MergeClause": NotRequired[str],
        "CrawlerConnection": NotRequired[str],
        "TableSchema": NotRequired[Sequence[OptionTypeDef]],
        "StagingTable": NotRequired[str],
        "SelectedColumns": NotRequired[Sequence[OptionTypeDef]],
    },
)
SnowflakeNodeDataExtraOutputTypeDef = TypedDict(
    "SnowflakeNodeDataExtraOutputTypeDef",
    {
        "SourceType": NotRequired[str],
        "Connection": NotRequired[OptionTypeDef],
        "Schema": NotRequired[str],
        "Table": NotRequired[str],
        "Database": NotRequired[str],
        "TempDir": NotRequired[str],
        "IamRole": NotRequired[OptionTypeDef],
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "SampleQuery": NotRequired[str],
        "PreAction": NotRequired[str],
        "PostAction": NotRequired[str],
        "Action": NotRequired[str],
        "Upsert": NotRequired[bool],
        "MergeAction": NotRequired[str],
        "MergeWhenMatched": NotRequired[str],
        "MergeWhenNotMatched": NotRequired[str],
        "MergeClause": NotRequired[str],
        "StagingTable": NotRequired[str],
        "SelectedColumns": NotRequired[List[OptionTypeDef]],
        "AutoPushdown": NotRequired[bool],
        "TableSchema": NotRequired[List[OptionTypeDef]],
    },
)
SnowflakeNodeDataOutputTypeDef = TypedDict(
    "SnowflakeNodeDataOutputTypeDef",
    {
        "SourceType": NotRequired[str],
        "Connection": NotRequired[OptionTypeDef],
        "Schema": NotRequired[str],
        "Table": NotRequired[str],
        "Database": NotRequired[str],
        "TempDir": NotRequired[str],
        "IamRole": NotRequired[OptionTypeDef],
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "SampleQuery": NotRequired[str],
        "PreAction": NotRequired[str],
        "PostAction": NotRequired[str],
        "Action": NotRequired[str],
        "Upsert": NotRequired[bool],
        "MergeAction": NotRequired[str],
        "MergeWhenMatched": NotRequired[str],
        "MergeWhenNotMatched": NotRequired[str],
        "MergeClause": NotRequired[str],
        "StagingTable": NotRequired[str],
        "SelectedColumns": NotRequired[List[OptionTypeDef]],
        "AutoPushdown": NotRequired[bool],
        "TableSchema": NotRequired[List[OptionTypeDef]],
    },
)
SnowflakeNodeDataTypeDef = TypedDict(
    "SnowflakeNodeDataTypeDef",
    {
        "SourceType": NotRequired[str],
        "Connection": NotRequired[OptionTypeDef],
        "Schema": NotRequired[str],
        "Table": NotRequired[str],
        "Database": NotRequired[str],
        "TempDir": NotRequired[str],
        "IamRole": NotRequired[OptionTypeDef],
        "AdditionalOptions": NotRequired[Mapping[str, str]],
        "SampleQuery": NotRequired[str],
        "PreAction": NotRequired[str],
        "PostAction": NotRequired[str],
        "Action": NotRequired[str],
        "Upsert": NotRequired[bool],
        "MergeAction": NotRequired[str],
        "MergeWhenMatched": NotRequired[str],
        "MergeWhenNotMatched": NotRequired[str],
        "MergeClause": NotRequired[str],
        "StagingTable": NotRequired[str],
        "SelectedColumns": NotRequired[Sequence[OptionTypeDef]],
        "AutoPushdown": NotRequired[bool],
        "TableSchema": NotRequired[Sequence[OptionTypeDef]],
    },
)
BackfillErrorTypeDef = TypedDict(
    "BackfillErrorTypeDef",
    {
        "Code": NotRequired[BackfillErrorCodeType],
        "Partitions": NotRequired[List[PartitionValueListOutputTypeDef]],
    },
)
CancelMLTaskRunResponseTypeDef = TypedDict(
    "CancelMLTaskRunResponseTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": TaskStatusTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CheckSchemaVersionValidityResponseTypeDef = TypedDict(
    "CheckSchemaVersionValidityResponseTypeDef",
    {
        "Valid": bool,
        "Error": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateBlueprintResponseTypeDef = TypedDict(
    "CreateBlueprintResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateConnectionResponseTypeDef = TypedDict(
    "CreateConnectionResponseTypeDef",
    {
        "CreateConnectionStatus": ConnectionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateCustomEntityTypeResponseTypeDef = TypedDict(
    "CreateCustomEntityTypeResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDataQualityRulesetResponseTypeDef = TypedDict(
    "CreateDataQualityRulesetResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDevEndpointResponseTypeDef = TypedDict(
    "CreateDevEndpointResponseTypeDef",
    {
        "EndpointName": str,
        "Status": str,
        "SecurityGroupIds": List[str],
        "SubnetId": str,
        "RoleArn": str,
        "YarnEndpointAddress": str,
        "ZeppelinRemoteSparkInterpreterPort": int,
        "NumberOfNodes": int,
        "WorkerType": WorkerTypeType,
        "GlueVersion": str,
        "NumberOfWorkers": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "ExtraPythonLibsS3Path": str,
        "ExtraJarsS3Path": str,
        "FailureReason": str,
        "SecurityConfiguration": str,
        "CreatedTimestamp": datetime,
        "Arguments": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateMLTransformResponseTypeDef = TypedDict(
    "CreateMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateRegistryResponseTypeDef = TypedDict(
    "CreateRegistryResponseTypeDef",
    {
        "RegistryArn": str,
        "RegistryName": str,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSchemaResponseTypeDef = TypedDict(
    "CreateSchemaResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "SchemaName": str,
        "SchemaArn": str,
        "Description": str,
        "DataFormat": DataFormatType,
        "Compatibility": CompatibilityType,
        "SchemaCheckpoint": int,
        "LatestSchemaVersion": int,
        "NextSchemaVersion": int,
        "SchemaStatus": SchemaStatusType,
        "Tags": Dict[str, str],
        "SchemaVersionId": str,
        "SchemaVersionStatus": SchemaVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateScriptResponseTypeDef = TypedDict(
    "CreateScriptResponseTypeDef",
    {
        "PythonScript": str,
        "ScalaCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSecurityConfigurationResponseTypeDef = TypedDict(
    "CreateSecurityConfigurationResponseTypeDef",
    {
        "Name": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateTriggerResponseTypeDef = TypedDict(
    "CreateTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateUsageProfileResponseTypeDef = TypedDict(
    "CreateUsageProfileResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateWorkflowResponseTypeDef = TypedDict(
    "CreateWorkflowResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteBlueprintResponseTypeDef = TypedDict(
    "DeleteBlueprintResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteCustomEntityTypeResponseTypeDef = TypedDict(
    "DeleteCustomEntityTypeResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteJobResponseTypeDef = TypedDict(
    "DeleteJobResponseTypeDef",
    {
        "JobName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteMLTransformResponseTypeDef = TypedDict(
    "DeleteMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteRegistryResponseTypeDef = TypedDict(
    "DeleteRegistryResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "Status": RegistryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteSchemaResponseTypeDef = TypedDict(
    "DeleteSchemaResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "Status": SchemaStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteSessionResponseTypeDef = TypedDict(
    "DeleteSessionResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteTriggerResponseTypeDef = TypedDict(
    "DeleteTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteWorkflowResponseTypeDef = TypedDict(
    "DeleteWorkflowResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCustomEntityTypeResponseTypeDef = TypedDict(
    "GetCustomEntityTypeResponseTypeDef",
    {
        "Name": str,
        "RegexString": str,
        "ContextWords": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPlanResponseTypeDef = TypedDict(
    "GetPlanResponseTypeDef",
    {
        "PythonScript": str,
        "ScalaCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetRegistryResponseTypeDef = TypedDict(
    "GetRegistryResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "Description": str,
        "Status": RegistryStatusType,
        "CreatedTime": str,
        "UpdatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {
        "PolicyInJson": str,
        "PolicyHash": str,
        "CreateTime": datetime,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaByDefinitionResponseTypeDef = TypedDict(
    "GetSchemaByDefinitionResponseTypeDef",
    {
        "SchemaVersionId": str,
        "SchemaArn": str,
        "DataFormat": DataFormatType,
        "Status": SchemaVersionStatusType,
        "CreatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaResponseTypeDef = TypedDict(
    "GetSchemaResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "SchemaName": str,
        "SchemaArn": str,
        "Description": str,
        "DataFormat": DataFormatType,
        "Compatibility": CompatibilityType,
        "SchemaCheckpoint": int,
        "LatestSchemaVersion": int,
        "NextSchemaVersion": int,
        "SchemaStatus": SchemaStatusType,
        "CreatedTime": str,
        "UpdatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaVersionResponseTypeDef = TypedDict(
    "GetSchemaVersionResponseTypeDef",
    {
        "SchemaVersionId": str,
        "SchemaDefinition": str,
        "DataFormat": DataFormatType,
        "SchemaArn": str,
        "VersionNumber": int,
        "Status": SchemaVersionStatusType,
        "CreatedTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaVersionsDiffResponseTypeDef = TypedDict(
    "GetSchemaVersionsDiffResponseTypeDef",
    {
        "Diff": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTagsResponseTypeDef = TypedDict(
    "GetTagsResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetWorkflowRunPropertiesResponseTypeDef = TypedDict(
    "GetWorkflowRunPropertiesResponseTypeDef",
    {
        "RunProperties": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListBlueprintsResponseTypeDef = TypedDict(
    "ListBlueprintsResponseTypeDef",
    {
        "Blueprints": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListColumnStatisticsTaskRunsResponseTypeDef = TypedDict(
    "ListColumnStatisticsTaskRunsResponseTypeDef",
    {
        "ColumnStatisticsTaskRunIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListCrawlersResponseTypeDef = TypedDict(
    "ListCrawlersResponseTypeDef",
    {
        "CrawlerNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListDevEndpointsResponseTypeDef = TypedDict(
    "ListDevEndpointsResponseTypeDef",
    {
        "DevEndpointNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "JobNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListMLTransformsResponseTypeDef = TypedDict(
    "ListMLTransformsResponseTypeDef",
    {
        "TransformIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListTriggersResponseTypeDef = TypedDict(
    "ListTriggersResponseTypeDef",
    {
        "TriggerNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListWorkflowsResponseTypeDef = TypedDict(
    "ListWorkflowsResponseTypeDef",
    {
        "Workflows": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef",
    {
        "PolicyHash": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutSchemaVersionMetadataResponseTypeDef = TypedDict(
    "PutSchemaVersionMetadataResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "RegistryName": str,
        "LatestVersion": bool,
        "VersionNumber": int,
        "SchemaVersionId": str,
        "MetadataKey": str,
        "MetadataValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RegisterSchemaVersionResponseTypeDef = TypedDict(
    "RegisterSchemaVersionResponseTypeDef",
    {
        "SchemaVersionId": str,
        "VersionNumber": int,
        "Status": SchemaVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RemoveSchemaVersionMetadataResponseTypeDef = TypedDict(
    "RemoveSchemaVersionMetadataResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "RegistryName": str,
        "LatestVersion": bool,
        "VersionNumber": int,
        "SchemaVersionId": str,
        "MetadataKey": str,
        "MetadataValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResumeWorkflowRunResponseTypeDef = TypedDict(
    "ResumeWorkflowRunResponseTypeDef",
    {
        "RunId": str,
        "NodeIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RunStatementResponseTypeDef = TypedDict(
    "RunStatementResponseTypeDef",
    {
        "Id": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartBlueprintRunResponseTypeDef = TypedDict(
    "StartBlueprintRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartColumnStatisticsTaskRunResponseTypeDef = TypedDict(
    "StartColumnStatisticsTaskRunResponseTypeDef",
    {
        "ColumnStatisticsTaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartDataQualityRuleRecommendationRunResponseTypeDef = TypedDict(
    "StartDataQualityRuleRecommendationRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartDataQualityRulesetEvaluationRunResponseTypeDef = TypedDict(
    "StartDataQualityRulesetEvaluationRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartExportLabelsTaskRunResponseTypeDef = TypedDict(
    "StartExportLabelsTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartImportLabelsTaskRunResponseTypeDef = TypedDict(
    "StartImportLabelsTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartJobRunResponseTypeDef = TypedDict(
    "StartJobRunResponseTypeDef",
    {
        "JobRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartMLEvaluationTaskRunResponseTypeDef = TypedDict(
    "StartMLEvaluationTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartMLLabelingSetGenerationTaskRunResponseTypeDef = TypedDict(
    "StartMLLabelingSetGenerationTaskRunResponseTypeDef",
    {
        "TaskRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartTriggerResponseTypeDef = TypedDict(
    "StartTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartWorkflowRunResponseTypeDef = TypedDict(
    "StartWorkflowRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StopSessionResponseTypeDef = TypedDict(
    "StopSessionResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StopTriggerResponseTypeDef = TypedDict(
    "StopTriggerResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateBlueprintResponseTypeDef = TypedDict(
    "UpdateBlueprintResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataQualityRulesetResponseTypeDef = TypedDict(
    "UpdateDataQualityRulesetResponseTypeDef",
    {
        "Name": str,
        "Description": str,
        "Ruleset": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateJobFromSourceControlResponseTypeDef = TypedDict(
    "UpdateJobFromSourceControlResponseTypeDef",
    {
        "JobName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateJobResponseTypeDef = TypedDict(
    "UpdateJobResponseTypeDef",
    {
        "JobName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateMLTransformResponseTypeDef = TypedDict(
    "UpdateMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateRegistryResponseTypeDef = TypedDict(
    "UpdateRegistryResponseTypeDef",
    {
        "RegistryName": str,
        "RegistryArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateSchemaResponseTypeDef = TypedDict(
    "UpdateSchemaResponseTypeDef",
    {
        "SchemaArn": str,
        "SchemaName": str,
        "RegistryName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateSourceControlFromJobResponseTypeDef = TypedDict(
    "UpdateSourceControlFromJobResponseTypeDef",
    {
        "JobName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateUsageProfileResponseTypeDef = TypedDict(
    "UpdateUsageProfileResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateWorkflowResponseTypeDef = TypedDict(
    "UpdateWorkflowResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchDeleteConnectionResponseTypeDef = TypedDict(
    "BatchDeleteConnectionResponseTypeDef",
    {
        "Succeeded": List[str],
        "Errors": Dict[str, ErrorDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchGetTableOptimizerErrorTypeDef = TypedDict(
    "BatchGetTableOptimizerErrorTypeDef",
    {
        "error": NotRequired[ErrorDetailTypeDef],
        "catalogId": NotRequired[str],
        "databaseName": NotRequired[str],
        "tableName": NotRequired[str],
        "type": NotRequired[Literal["compaction"]],
    },
)
BatchStopJobRunErrorTypeDef = TypedDict(
    "BatchStopJobRunErrorTypeDef",
    {
        "JobName": NotRequired[str],
        "JobRunId": NotRequired[str],
        "ErrorDetail": NotRequired[ErrorDetailTypeDef],
    },
)
BatchUpdatePartitionFailureEntryTypeDef = TypedDict(
    "BatchUpdatePartitionFailureEntryTypeDef",
    {
        "PartitionValueList": NotRequired[List[str]],
        "ErrorDetail": NotRequired[ErrorDetailTypeDef],
    },
)
ColumnErrorTypeDef = TypedDict(
    "ColumnErrorTypeDef",
    {
        "ColumnName": NotRequired[str],
        "Error": NotRequired[ErrorDetailTypeDef],
    },
)
PartitionErrorTypeDef = TypedDict(
    "PartitionErrorTypeDef",
    {
        "PartitionValues": NotRequired[List[str]],
        "ErrorDetail": NotRequired[ErrorDetailTypeDef],
    },
)
TableErrorTypeDef = TypedDict(
    "TableErrorTypeDef",
    {
        "TableName": NotRequired[str],
        "ErrorDetail": NotRequired[ErrorDetailTypeDef],
    },
)
TableVersionErrorTypeDef = TypedDict(
    "TableVersionErrorTypeDef",
    {
        "TableName": NotRequired[str],
        "VersionId": NotRequired[str],
        "ErrorDetail": NotRequired[ErrorDetailTypeDef],
    },
)
BatchGetCustomEntityTypesResponseTypeDef = TypedDict(
    "BatchGetCustomEntityTypesResponseTypeDef",
    {
        "CustomEntityTypes": List[CustomEntityTypeTypeDef],
        "CustomEntityTypesNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListCustomEntityTypesResponseTypeDef = TypedDict(
    "ListCustomEntityTypesResponseTypeDef",
    {
        "CustomEntityTypes": List[CustomEntityTypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
BatchGetDevEndpointsResponseTypeDef = TypedDict(
    "BatchGetDevEndpointsResponseTypeDef",
    {
        "DevEndpoints": List[DevEndpointTypeDef],
        "DevEndpointsNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDevEndpointResponseTypeDef = TypedDict(
    "GetDevEndpointResponseTypeDef",
    {
        "DevEndpoint": DevEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDevEndpointsResponseTypeDef = TypedDict(
    "GetDevEndpointsResponseTypeDef",
    {
        "DevEndpoints": List[DevEndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
BatchGetTableOptimizerRequestRequestTypeDef = TypedDict(
    "BatchGetTableOptimizerRequestRequestTypeDef",
    {
        "Entries": Sequence[BatchGetTableOptimizerEntryTypeDef],
    },
)
DecimalNumberTypeDef = TypedDict(
    "DecimalNumberTypeDef",
    {
        "UnscaledValue": BlobTypeDef,
        "Scale": int,
    },
)
GetBlueprintRunResponseTypeDef = TypedDict(
    "GetBlueprintRunResponseTypeDef",
    {
        "BlueprintRun": BlueprintRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetBlueprintRunsResponseTypeDef = TypedDict(
    "GetBlueprintRunsResponseTypeDef",
    {
        "BlueprintRuns": List[BlueprintRunTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
BlueprintTypeDef = TypedDict(
    "BlueprintTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "CreatedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
        "ParameterSpec": NotRequired[str],
        "BlueprintLocation": NotRequired[str],
        "BlueprintServiceLocation": NotRequired[str],
        "Status": NotRequired[BlueprintStatusType],
        "ErrorMessage": NotRequired[str],
        "LastActiveDefinition": NotRequired[LastActiveDefinitionTypeDef],
    },
)
GetCatalogImportStatusResponseTypeDef = TypedDict(
    "GetCatalogImportStatusResponseTypeDef",
    {
        "ImportStatus": CatalogImportStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CatalogKafkaSourceExtraOutputTypeDef = TypedDict(
    "CatalogKafkaSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KafkaStreamingSourceOptionsExtraOutputTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
DirectKafkaSourceExtraOutputTypeDef = TypedDict(
    "DirectKafkaSourceExtraOutputTypeDef",
    {
        "Name": str,
        "StreamingOptions": NotRequired[KafkaStreamingSourceOptionsExtraOutputTypeDef],
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
CatalogKafkaSourceOutputTypeDef = TypedDict(
    "CatalogKafkaSourceOutputTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KafkaStreamingSourceOptionsOutputTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
DirectKafkaSourceOutputTypeDef = TypedDict(
    "DirectKafkaSourceOutputTypeDef",
    {
        "Name": str,
        "StreamingOptions": NotRequired[KafkaStreamingSourceOptionsOutputTypeDef],
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
CatalogKinesisSourceExtraOutputTypeDef = TypedDict(
    "CatalogKinesisSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KinesisStreamingSourceOptionsExtraOutputTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
DirectKinesisSourceExtraOutputTypeDef = TypedDict(
    "DirectKinesisSourceExtraOutputTypeDef",
    {
        "Name": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KinesisStreamingSourceOptionsExtraOutputTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
CatalogKinesisSourceOutputTypeDef = TypedDict(
    "CatalogKinesisSourceOutputTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KinesisStreamingSourceOptionsOutputTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
DirectKinesisSourceOutputTypeDef = TypedDict(
    "DirectKinesisSourceOutputTypeDef",
    {
        "Name": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KinesisStreamingSourceOptionsOutputTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
GovernedCatalogTargetExtraOutputTypeDef = TypedDict(
    "GovernedCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
GovernedCatalogTargetOutputTypeDef = TypedDict(
    "GovernedCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
GovernedCatalogTargetTypeDef = TypedDict(
    "GovernedCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3CatalogTargetExtraOutputTypeDef = TypedDict(
    "S3CatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3CatalogTargetOutputTypeDef = TypedDict(
    "S3CatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3CatalogTargetTypeDef = TypedDict(
    "S3CatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3DeltaCatalogTargetExtraOutputTypeDef = TypedDict(
    "S3DeltaCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3DeltaCatalogTargetOutputTypeDef = TypedDict(
    "S3DeltaCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3DeltaCatalogTargetTypeDef = TypedDict(
    "S3DeltaCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Table": str,
        "Database": str,
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "AdditionalOptions": NotRequired[Mapping[str, str]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3HudiCatalogTargetExtraOutputTypeDef = TypedDict(
    "S3HudiCatalogTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "AdditionalOptions": Dict[str, str],
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3HudiCatalogTargetOutputTypeDef = TypedDict(
    "S3HudiCatalogTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Table": str,
        "Database": str,
        "AdditionalOptions": Dict[str, str],
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
S3HudiCatalogTargetTypeDef = TypedDict(
    "S3HudiCatalogTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Table": str,
        "Database": str,
        "AdditionalOptions": Mapping[str, str],
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "SchemaChangePolicy": NotRequired[CatalogSchemaChangePolicyTypeDef],
    },
)
ClassifierTypeDef = TypedDict(
    "ClassifierTypeDef",
    {
        "GrokClassifier": NotRequired[GrokClassifierTypeDef],
        "XMLClassifier": NotRequired[XMLClassifierTypeDef],
        "JsonClassifier": NotRequired[JsonClassifierTypeDef],
        "CsvClassifier": NotRequired[CsvClassifierTypeDef],
    },
)
CodeGenNodeOutputTypeDef = TypedDict(
    "CodeGenNodeOutputTypeDef",
    {
        "Id": str,
        "NodeType": str,
        "Args": List[CodeGenNodeArgTypeDef],
        "LineNumber": NotRequired[int],
    },
)
CodeGenNodeTypeDef = TypedDict(
    "CodeGenNodeTypeDef",
    {
        "Id": str,
        "NodeType": str,
        "Args": Sequence[CodeGenNodeArgTypeDef],
        "LineNumber": NotRequired[int],
    },
)
LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {
        "Jdbc": NotRequired[Sequence[CodeGenNodeArgTypeDef]],
        "S3": NotRequired[Sequence[CodeGenNodeArgTypeDef]],
        "DynamoDB": NotRequired[Sequence[CodeGenNodeArgTypeDef]],
    },
)
GetColumnStatisticsTaskRunResponseTypeDef = TypedDict(
    "GetColumnStatisticsTaskRunResponseTypeDef",
    {
        "ColumnStatisticsTaskRun": ColumnStatisticsTaskRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetColumnStatisticsTaskRunsResponseTypeDef = TypedDict(
    "GetColumnStatisticsTaskRunsResponseTypeDef",
    {
        "ColumnStatisticsTaskRuns": List[ColumnStatisticsTaskRunTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
DateColumnStatisticsDataTypeDef = TypedDict(
    "DateColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
        "MinimumValue": NotRequired[TimestampTypeDef],
        "MaximumValue": NotRequired[TimestampTypeDef],
    },
)
GetTableRequestRequestTypeDef = TypedDict(
    "GetTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "Name": str,
        "CatalogId": NotRequired[str],
        "TransactionId": NotRequired[str],
        "QueryAsOfTime": NotRequired[TimestampTypeDef],
    },
)
GetTablesRequestRequestTypeDef = TypedDict(
    "GetTablesRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "CatalogId": NotRequired[str],
        "Expression": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "TransactionId": NotRequired[str],
        "QueryAsOfTime": NotRequired[TimestampTypeDef],
    },
)
KafkaStreamingSourceOptionsTypeDef = TypedDict(
    "KafkaStreamingSourceOptionsTypeDef",
    {
        "BootstrapServers": NotRequired[str],
        "SecurityProtocol": NotRequired[str],
        "ConnectionName": NotRequired[str],
        "TopicName": NotRequired[str],
        "Assign": NotRequired[str],
        "SubscribePattern": NotRequired[str],
        "Classification": NotRequired[str],
        "Delimiter": NotRequired[str],
        "StartingOffsets": NotRequired[str],
        "EndingOffsets": NotRequired[str],
        "PollTimeoutMs": NotRequired[int],
        "NumRetries": NotRequired[int],
        "RetryIntervalMs": NotRequired[int],
        "MaxOffsetsPerTrigger": NotRequired[int],
        "MinPartitions": NotRequired[int],
        "IncludeHeaders": NotRequired[bool],
        "AddRecordTimestamp": NotRequired[str],
        "EmitConsumerLagMetrics": NotRequired[str],
        "StartingTimestamp": NotRequired[TimestampTypeDef],
    },
)
KinesisStreamingSourceOptionsTypeDef = TypedDict(
    "KinesisStreamingSourceOptionsTypeDef",
    {
        "EndpointUrl": NotRequired[str],
        "StreamName": NotRequired[str],
        "Classification": NotRequired[str],
        "Delimiter": NotRequired[str],
        "StartingPosition": NotRequired[StartingPositionType],
        "MaxFetchTimeInMs": NotRequired[int],
        "MaxFetchRecordsPerShard": NotRequired[int],
        "MaxRecordPerRead": NotRequired[int],
        "AddIdleTimeBetweenReads": NotRequired[bool],
        "IdleTimeBetweenReadsInMs": NotRequired[int],
        "DescribeShardInterval": NotRequired[int],
        "NumRetries": NotRequired[int],
        "RetryIntervalMs": NotRequired[int],
        "MaxRetryIntervalMs": NotRequired[int],
        "AvoidEmptyBatches": NotRequired[bool],
        "StreamArn": NotRequired[str],
        "RoleArn": NotRequired[str],
        "RoleSessionName": NotRequired[str],
        "AddRecordTimestamp": NotRequired[str],
        "EmitConsumerLagMetrics": NotRequired[str],
        "StartingTimestamp": NotRequired[TimestampTypeDef],
    },
)
QuerySessionContextTypeDef = TypedDict(
    "QuerySessionContextTypeDef",
    {
        "QueryId": NotRequired[str],
        "QueryStartTime": NotRequired[TimestampTypeDef],
        "ClusterId": NotRequired[str],
        "QueryAuthorizationId": NotRequired[str],
        "AdditionalContext": NotRequired[Mapping[str, str]],
    },
)
TaskRunFilterCriteriaTypeDef = TypedDict(
    "TaskRunFilterCriteriaTypeDef",
    {
        "TaskRunType": NotRequired[TaskTypeType],
        "Status": NotRequired[TaskStatusTypeType],
        "StartedBefore": NotRequired[TimestampTypeDef],
        "StartedAfter": NotRequired[TimestampTypeDef],
    },
)
PredicateExtraOutputTypeDef = TypedDict(
    "PredicateExtraOutputTypeDef",
    {
        "Logical": NotRequired[LogicalType],
        "Conditions": NotRequired[List[ConditionTypeDef]],
    },
)
PredicateOutputTypeDef = TypedDict(
    "PredicateOutputTypeDef",
    {
        "Logical": NotRequired[LogicalType],
        "Conditions": NotRequired[List[ConditionTypeDef]],
    },
)
PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {
        "Logical": NotRequired[LogicalType],
        "Conditions": NotRequired[Sequence[ConditionTypeDef]],
    },
)
ProfileConfigurationOutputTypeDef = TypedDict(
    "ProfileConfigurationOutputTypeDef",
    {
        "SessionConfiguration": NotRequired[Dict[str, ConfigurationObjectOutputTypeDef]],
        "JobConfiguration": NotRequired[Dict[str, ConfigurationObjectOutputTypeDef]],
    },
)
ProfileConfigurationTypeDef = TypedDict(
    "ProfileConfigurationTypeDef",
    {
        "SessionConfiguration": NotRequired[Mapping[str, ConfigurationObjectTypeDef]],
        "JobConfiguration": NotRequired[Mapping[str, ConfigurationObjectTypeDef]],
    },
)
FindMatchesMetricsTypeDef = TypedDict(
    "FindMatchesMetricsTypeDef",
    {
        "AreaUnderPRCurve": NotRequired[float],
        "Precision": NotRequired[float],
        "Recall": NotRequired[float],
        "F1": NotRequired[float],
        "ConfusionMatrix": NotRequired[ConfusionMatrixTypeDef],
        "ColumnImportances": NotRequired[List[ColumnImportanceTypeDef]],
    },
)
ConnectionsListUnionTypeDef = Union[ConnectionsListTypeDef, ConnectionsListExtraOutputTypeDef]
CrawlerNodeDetailsTypeDef = TypedDict(
    "CrawlerNodeDetailsTypeDef",
    {
        "Crawls": NotRequired[List[CrawlTypeDef]],
    },
)
ListCrawlsResponseTypeDef = TypedDict(
    "ListCrawlsResponseTypeDef",
    {
        "Crawls": List[CrawlerHistoryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetCrawlerMetricsResponseTypeDef = TypedDict(
    "GetCrawlerMetricsResponseTypeDef",
    {
        "CrawlerMetricsList": List[CrawlerMetricsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
CrawlerTargetsExtraOutputTypeDef = TypedDict(
    "CrawlerTargetsExtraOutputTypeDef",
    {
        "S3Targets": NotRequired[List[S3TargetExtraOutputTypeDef]],
        "JdbcTargets": NotRequired[List[JdbcTargetExtraOutputTypeDef]],
        "MongoDBTargets": NotRequired[List[MongoDBTargetTypeDef]],
        "DynamoDBTargets": NotRequired[List[DynamoDBTargetTypeDef]],
        "CatalogTargets": NotRequired[List[CatalogTargetExtraOutputTypeDef]],
        "DeltaTargets": NotRequired[List[DeltaTargetExtraOutputTypeDef]],
        "IcebergTargets": NotRequired[List[IcebergTargetExtraOutputTypeDef]],
        "HudiTargets": NotRequired[List[HudiTargetExtraOutputTypeDef]],
    },
)
CrawlerTargetsOutputTypeDef = TypedDict(
    "CrawlerTargetsOutputTypeDef",
    {
        "S3Targets": NotRequired[List[S3TargetOutputTypeDef]],
        "JdbcTargets": NotRequired[List[JdbcTargetOutputTypeDef]],
        "MongoDBTargets": NotRequired[List[MongoDBTargetTypeDef]],
        "DynamoDBTargets": NotRequired[List[DynamoDBTargetTypeDef]],
        "CatalogTargets": NotRequired[List[CatalogTargetOutputTypeDef]],
        "DeltaTargets": NotRequired[List[DeltaTargetOutputTypeDef]],
        "IcebergTargets": NotRequired[List[IcebergTargetOutputTypeDef]],
        "HudiTargets": NotRequired[List[HudiTargetOutputTypeDef]],
    },
)
CrawlerTargetsTypeDef = TypedDict(
    "CrawlerTargetsTypeDef",
    {
        "S3Targets": NotRequired[Sequence[S3TargetTypeDef]],
        "JdbcTargets": NotRequired[Sequence[JdbcTargetTypeDef]],
        "MongoDBTargets": NotRequired[Sequence[MongoDBTargetTypeDef]],
        "DynamoDBTargets": NotRequired[Sequence[DynamoDBTargetTypeDef]],
        "CatalogTargets": NotRequired[Sequence[CatalogTargetTypeDef]],
        "DeltaTargets": NotRequired[Sequence[DeltaTargetTypeDef]],
        "IcebergTargets": NotRequired[Sequence[IcebergTargetTypeDef]],
        "HudiTargets": NotRequired[Sequence[HudiTargetTypeDef]],
    },
)
ListCrawlsRequestRequestTypeDef = TypedDict(
    "ListCrawlsRequestRequestTypeDef",
    {
        "CrawlerName": str,
        "MaxResults": NotRequired[int],
        "Filters": NotRequired[Sequence[CrawlsFilterTypeDef]],
        "NextToken": NotRequired[str],
    },
)
CreateClassifierRequestRequestTypeDef = TypedDict(
    "CreateClassifierRequestRequestTypeDef",
    {
        "GrokClassifier": NotRequired[CreateGrokClassifierRequestTypeDef],
        "XMLClassifier": NotRequired[CreateXMLClassifierRequestTypeDef],
        "JsonClassifier": NotRequired[CreateJsonClassifierRequestTypeDef],
        "CsvClassifier": NotRequired[CreateCsvClassifierRequestTypeDef],
    },
)
CreateDataQualityRulesetRequestRequestTypeDef = TypedDict(
    "CreateDataQualityRulesetRequestRequestTypeDef",
    {
        "Name": str,
        "Ruleset": str,
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
        "TargetTable": NotRequired[DataQualityTargetTableTypeDef],
        "ClientToken": NotRequired[str],
    },
)
DataQualityRulesetFilterCriteriaTypeDef = TypedDict(
    "DataQualityRulesetFilterCriteriaTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "CreatedBefore": NotRequired[TimestampTypeDef],
        "CreatedAfter": NotRequired[TimestampTypeDef],
        "LastModifiedBefore": NotRequired[TimestampTypeDef],
        "LastModifiedAfter": NotRequired[TimestampTypeDef],
        "TargetTable": NotRequired[DataQualityTargetTableTypeDef],
    },
)
DataQualityRulesetListDetailsTypeDef = TypedDict(
    "DataQualityRulesetListDetailsTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "CreatedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
        "TargetTable": NotRequired[DataQualityTargetTableTypeDef],
        "RecommendationRunId": NotRequired[str],
        "RuleCount": NotRequired[int],
    },
)
GetDataQualityRulesetResponseTypeDef = TypedDict(
    "GetDataQualityRulesetResponseTypeDef",
    {
        "Name": str,
        "Description": str,
        "Ruleset": str,
        "TargetTable": DataQualityTargetTableTypeDef,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "RecommendationRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreatePartitionIndexRequestRequestTypeDef = TypedDict(
    "CreatePartitionIndexRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionIndex": PartitionIndexTypeDef,
        "CatalogId": NotRequired[str],
    },
)
CreateSchemaInputRequestTypeDef = TypedDict(
    "CreateSchemaInputRequestTypeDef",
    {
        "SchemaName": str,
        "DataFormat": DataFormatType,
        "RegistryId": NotRequired[RegistryIdTypeDef],
        "Compatibility": NotRequired[CompatibilityType],
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
        "SchemaDefinition": NotRequired[str],
    },
)
DeleteRegistryInputRequestTypeDef = TypedDict(
    "DeleteRegistryInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
    },
)
GetRegistryInputRequestTypeDef = TypedDict(
    "GetRegistryInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
    },
)
ListSchemasInputRequestTypeDef = TypedDict(
    "ListSchemasInputRequestTypeDef",
    {
        "RegistryId": NotRequired[RegistryIdTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
UpdateRegistryInputRequestTypeDef = TypedDict(
    "UpdateRegistryInputRequestTypeDef",
    {
        "RegistryId": RegistryIdTypeDef,
        "Description": str,
    },
)
CreateSessionRequestRequestTypeDef = TypedDict(
    "CreateSessionRequestRequestTypeDef",
    {
        "Id": str,
        "Role": str,
        "Command": SessionCommandTypeDef,
        "Description": NotRequired[str],
        "Timeout": NotRequired[int],
        "IdleTimeout": NotRequired[int],
        "DefaultArguments": NotRequired[Mapping[str, str]],
        "Connections": NotRequired[ConnectionsListTypeDef],
        "MaxCapacity": NotRequired[float],
        "NumberOfWorkers": NotRequired[int],
        "WorkerType": NotRequired[WorkerTypeType],
        "SecurityConfiguration": NotRequired[str],
        "GlueVersion": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
        "RequestOrigin": NotRequired[str],
    },
)
SessionTypeDef = TypedDict(
    "SessionTypeDef",
    {
        "Id": NotRequired[str],
        "CreatedOn": NotRequired[datetime],
        "Status": NotRequired[SessionStatusType],
        "ErrorMessage": NotRequired[str],
        "Description": NotRequired[str],
        "Role": NotRequired[str],
        "Command": NotRequired[SessionCommandTypeDef],
        "DefaultArguments": NotRequired[Dict[str, str]],
        "Connections": NotRequired[ConnectionsListOutputTypeDef],
        "Progress": NotRequired[float],
        "MaxCapacity": NotRequired[float],
        "SecurityConfiguration": NotRequired[str],
        "GlueVersion": NotRequired[str],
        "NumberOfWorkers": NotRequired[int],
        "WorkerType": NotRequired[WorkerTypeType],
        "CompletedOn": NotRequired[datetime],
        "ExecutionTime": NotRequired[float],
        "DPUSeconds": NotRequired[float],
        "IdleTimeout": NotRequired[int],
        "ProfileName": NotRequired[str],
    },
)
CreateTableOptimizerRequestRequestTypeDef = TypedDict(
    "CreateTableOptimizerRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Type": Literal["compaction"],
        "TableOptimizerConfiguration": TableOptimizerConfigurationTypeDef,
    },
)
UpdateTableOptimizerRequestRequestTypeDef = TypedDict(
    "UpdateTableOptimizerRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Type": Literal["compaction"],
        "TableOptimizerConfiguration": TableOptimizerConfigurationTypeDef,
    },
)
EvaluateDataQualityExtraOutputTypeDef = TypedDict(
    "EvaluateDataQualityExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Ruleset": str,
        "Output": NotRequired[DQTransformOutputType],
        "PublishingOptions": NotRequired[DQResultsPublishingOptionsTypeDef],
        "StopJobOnFailureOptions": NotRequired[DQStopJobOnFailureOptionsTypeDef],
    },
)
EvaluateDataQualityMultiFrameExtraOutputTypeDef = TypedDict(
    "EvaluateDataQualityMultiFrameExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Ruleset": str,
        "AdditionalDataSources": NotRequired[Dict[str, str]],
        "PublishingOptions": NotRequired[DQResultsPublishingOptionsTypeDef],
        "AdditionalOptions": NotRequired[Dict[AdditionalOptionKeysType, str]],
        "StopJobOnFailureOptions": NotRequired[DQStopJobOnFailureOptionsTypeDef],
    },
)
EvaluateDataQualityMultiFrameOutputTypeDef = TypedDict(
    "EvaluateDataQualityMultiFrameOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Ruleset": str,
        "AdditionalDataSources": NotRequired[Dict[str, str]],
        "PublishingOptions": NotRequired[DQResultsPublishingOptionsTypeDef],
        "AdditionalOptions": NotRequired[Dict[AdditionalOptionKeysType, str]],
        "StopJobOnFailureOptions": NotRequired[DQStopJobOnFailureOptionsTypeDef],
    },
)
EvaluateDataQualityMultiFrameTypeDef = TypedDict(
    "EvaluateDataQualityMultiFrameTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Ruleset": str,
        "AdditionalDataSources": NotRequired[Mapping[str, str]],
        "PublishingOptions": NotRequired[DQResultsPublishingOptionsTypeDef],
        "AdditionalOptions": NotRequired[Mapping[AdditionalOptionKeysType, str]],
        "StopJobOnFailureOptions": NotRequired[DQStopJobOnFailureOptionsTypeDef],
    },
)
EvaluateDataQualityOutputTypeDef = TypedDict(
    "EvaluateDataQualityOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Ruleset": str,
        "Output": NotRequired[DQTransformOutputType],
        "PublishingOptions": NotRequired[DQResultsPublishingOptionsTypeDef],
        "StopJobOnFailureOptions": NotRequired[DQStopJobOnFailureOptionsTypeDef],
    },
)
EvaluateDataQualityTypeDef = TypedDict(
    "EvaluateDataQualityTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Ruleset": str,
        "Output": NotRequired[DQTransformOutputType],
        "PublishingOptions": NotRequired[DQResultsPublishingOptionsTypeDef],
        "StopJobOnFailureOptions": NotRequired[DQStopJobOnFailureOptionsTypeDef],
    },
)
DataCatalogEncryptionSettingsTypeDef = TypedDict(
    "DataCatalogEncryptionSettingsTypeDef",
    {
        "EncryptionAtRest": NotRequired[EncryptionAtRestTypeDef],
        "ConnectionPasswordEncryption": NotRequired[ConnectionPasswordEncryptionTypeDef],
    },
)
PrincipalPermissionsOutputTypeDef = TypedDict(
    "PrincipalPermissionsOutputTypeDef",
    {
        "Principal": NotRequired[DataLakePrincipalTypeDef],
        "Permissions": NotRequired[List[PermissionType]],
    },
)
PrincipalPermissionsTypeDef = TypedDict(
    "PrincipalPermissionsTypeDef",
    {
        "Principal": NotRequired[DataLakePrincipalTypeDef],
        "Permissions": NotRequired[Sequence[PermissionType]],
    },
)
MetricBasedObservationTypeDef = TypedDict(
    "MetricBasedObservationTypeDef",
    {
        "MetricName": NotRequired[str],
        "MetricValues": NotRequired[DataQualityMetricValuesTypeDef],
        "NewRules": NotRequired[List[str]],
    },
)
DataSourceOutputTypeDef = TypedDict(
    "DataSourceOutputTypeDef",
    {
        "GlueTable": GlueTableOutputTypeDef,
    },
)
DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "GlueTable": GlueTableTypeDef,
    },
)
GlueTableUnionTypeDef = Union[GlueTableTypeDef, GlueTableOutputTypeDef]
NullValueFieldTypeDef = TypedDict(
    "NullValueFieldTypeDef",
    {
        "Value": str,
        "Datatype": DatatypeTypeDef,
    },
)
DecimalColumnStatisticsDataOutputTypeDef = TypedDict(
    "DecimalColumnStatisticsDataOutputTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
        "MinimumValue": NotRequired[DecimalNumberOutputTypeDef],
        "MaximumValue": NotRequired[DecimalNumberOutputTypeDef],
    },
)
DeleteSchemaInputRequestTypeDef = TypedDict(
    "DeleteSchemaInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
    },
)
DeleteSchemaVersionsInputRequestTypeDef = TypedDict(
    "DeleteSchemaVersionsInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "Versions": str,
    },
)
GetSchemaByDefinitionInputRequestTypeDef = TypedDict(
    "GetSchemaByDefinitionInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaDefinition": str,
    },
)
GetSchemaInputRequestTypeDef = TypedDict(
    "GetSchemaInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
    },
)
ListSchemaVersionsInputRequestTypeDef = TypedDict(
    "ListSchemaVersionsInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
RegisterSchemaVersionInputRequestTypeDef = TypedDict(
    "RegisterSchemaVersionInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaDefinition": str,
    },
)
SchemaReferenceTypeDef = TypedDict(
    "SchemaReferenceTypeDef",
    {
        "SchemaId": NotRequired[SchemaIdTypeDef],
        "SchemaVersionId": NotRequired[str],
        "SchemaVersionNumber": NotRequired[int],
    },
)
UpdateDevEndpointRequestRequestTypeDef = TypedDict(
    "UpdateDevEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
        "PublicKey": NotRequired[str],
        "AddPublicKeys": NotRequired[Sequence[str]],
        "DeletePublicKeys": NotRequired[Sequence[str]],
        "CustomLibraries": NotRequired[DevEndpointCustomLibrariesTypeDef],
        "UpdateEtlLibraries": NotRequired[bool],
        "DeleteArguments": NotRequired[Sequence[str]],
        "AddArguments": NotRequired[Mapping[str, str]],
    },
)
S3DeltaDirectTargetExtraOutputTypeDef = TypedDict(
    "S3DeltaDirectTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Compression": DeltaTargetCompressionTypeType,
        "Format": TargetFormatType,
        "PartitionKeys": NotRequired[List[List[str]]],
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3DeltaDirectTargetOutputTypeDef = TypedDict(
    "S3DeltaDirectTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Compression": DeltaTargetCompressionTypeType,
        "Format": TargetFormatType,
        "PartitionKeys": NotRequired[List[List[str]]],
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3DeltaDirectTargetTypeDef = TypedDict(
    "S3DeltaDirectTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Path": str,
        "Compression": DeltaTargetCompressionTypeType,
        "Format": TargetFormatType,
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "AdditionalOptions": NotRequired[Mapping[str, str]],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3DirectTargetExtraOutputTypeDef = TypedDict(
    "S3DirectTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Format": TargetFormatType,
        "PartitionKeys": NotRequired[List[List[str]]],
        "Compression": NotRequired[str],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3DirectTargetOutputTypeDef = TypedDict(
    "S3DirectTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Format": TargetFormatType,
        "PartitionKeys": NotRequired[List[List[str]]],
        "Compression": NotRequired[str],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3DirectTargetTypeDef = TypedDict(
    "S3DirectTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Path": str,
        "Format": TargetFormatType,
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "Compression": NotRequired[str],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3GlueParquetTargetExtraOutputTypeDef = TypedDict(
    "S3GlueParquetTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "Compression": NotRequired[ParquetCompressionTypeType],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3GlueParquetTargetOutputTypeDef = TypedDict(
    "S3GlueParquetTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "PartitionKeys": NotRequired[List[List[str]]],
        "Compression": NotRequired[ParquetCompressionTypeType],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3GlueParquetTargetTypeDef = TypedDict(
    "S3GlueParquetTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Path": str,
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "Compression": NotRequired[ParquetCompressionTypeType],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3HudiDirectTargetExtraOutputTypeDef = TypedDict(
    "S3HudiDirectTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Compression": HudiTargetCompressionTypeType,
        "Format": TargetFormatType,
        "AdditionalOptions": Dict[str, str],
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3HudiDirectTargetOutputTypeDef = TypedDict(
    "S3HudiDirectTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Path": str,
        "Compression": HudiTargetCompressionTypeType,
        "Format": TargetFormatType,
        "AdditionalOptions": Dict[str, str],
        "PartitionKeys": NotRequired[List[List[str]]],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
S3HudiDirectTargetTypeDef = TypedDict(
    "S3HudiDirectTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Path": str,
        "Compression": HudiTargetCompressionTypeType,
        "Format": TargetFormatType,
        "AdditionalOptions": Mapping[str, str],
        "PartitionKeys": NotRequired[Sequence[Sequence[str]]],
        "SchemaChangePolicy": NotRequired[DirectSchemaChangePolicyTypeDef],
    },
)
EncryptionConfigurationExtraOutputTypeDef = TypedDict(
    "EncryptionConfigurationExtraOutputTypeDef",
    {
        "S3Encryption": NotRequired[List[S3EncryptionTypeDef]],
        "CloudWatchEncryption": NotRequired[CloudWatchEncryptionTypeDef],
        "JobBookmarksEncryption": NotRequired[JobBookmarksEncryptionTypeDef],
    },
)
EncryptionConfigurationOutputTypeDef = TypedDict(
    "EncryptionConfigurationOutputTypeDef",
    {
        "S3Encryption": NotRequired[List[S3EncryptionTypeDef]],
        "CloudWatchEncryption": NotRequired[CloudWatchEncryptionTypeDef],
        "JobBookmarksEncryption": NotRequired[JobBookmarksEncryptionTypeDef],
    },
)
EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "S3Encryption": NotRequired[Sequence[S3EncryptionTypeDef]],
        "CloudWatchEncryption": NotRequired[CloudWatchEncryptionTypeDef],
        "JobBookmarksEncryption": NotRequired[JobBookmarksEncryptionTypeDef],
    },
)
SchemaVersionErrorItemTypeDef = TypedDict(
    "SchemaVersionErrorItemTypeDef",
    {
        "VersionNumber": NotRequired[int],
        "ErrorDetails": NotRequired[ErrorDetailsTypeDef],
    },
)
FilterExpressionExtraOutputTypeDef = TypedDict(
    "FilterExpressionExtraOutputTypeDef",
    {
        "Operation": FilterOperationType,
        "Values": List[FilterValueExtraOutputTypeDef],
        "Negated": NotRequired[bool],
    },
)
FilterExpressionOutputTypeDef = TypedDict(
    "FilterExpressionOutputTypeDef",
    {
        "Operation": FilterOperationType,
        "Values": List[FilterValueOutputTypeDef],
        "Negated": NotRequired[bool],
    },
)
FilterExpressionTypeDef = TypedDict(
    "FilterExpressionTypeDef",
    {
        "Operation": FilterOperationType,
        "Values": Sequence[FilterValueTypeDef],
        "Negated": NotRequired[bool],
    },
)
TransformParametersTypeDef = TypedDict(
    "TransformParametersTypeDef",
    {
        "TransformType": Literal["FIND_MATCHES"],
        "FindMatchesParameters": NotRequired[FindMatchesParametersTypeDef],
    },
)
GetClassifiersRequestGetClassifiersPaginateTypeDef = TypedDict(
    "GetClassifiersRequestGetClassifiersPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef = TypedDict(
    "GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef",
    {
        "CrawlerNameList": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetCrawlersRequestGetCrawlersPaginateTypeDef = TypedDict(
    "GetCrawlersRequestGetCrawlersPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetDatabasesRequestGetDatabasesPaginateTypeDef = TypedDict(
    "GetDatabasesRequestGetDatabasesPaginateTypeDef",
    {
        "CatalogId": NotRequired[str],
        "ResourceShareType": NotRequired[ResourceShareTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef = TypedDict(
    "GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetJobRunsRequestGetJobRunsPaginateTypeDef = TypedDict(
    "GetJobRunsRequestGetJobRunsPaginateTypeDef",
    {
        "JobName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetJobsRequestGetJobsPaginateTypeDef = TypedDict(
    "GetJobsRequestGetJobsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef = TypedDict(
    "GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef = TypedDict(
    "GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef = TypedDict(
    "GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetTableVersionsRequestGetTableVersionsPaginateTypeDef = TypedDict(
    "GetTableVersionsRequestGetTableVersionsPaginateTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetTablesRequestGetTablesPaginateTypeDef = TypedDict(
    "GetTablesRequestGetTablesPaginateTypeDef",
    {
        "DatabaseName": str,
        "CatalogId": NotRequired[str],
        "Expression": NotRequired[str],
        "TransactionId": NotRequired[str],
        "QueryAsOfTime": NotRequired[TimestampTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetTriggersRequestGetTriggersPaginateTypeDef = TypedDict(
    "GetTriggersRequestGetTriggersPaginateTypeDef",
    {
        "DependentJobName": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef = TypedDict(
    "GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef",
    {
        "Pattern": str,
        "CatalogId": NotRequired[str],
        "DatabaseName": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListRegistriesInputListRegistriesPaginateTypeDef = TypedDict(
    "ListRegistriesInputListRegistriesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef = TypedDict(
    "ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSchemasInputListSchemasPaginateTypeDef = TypedDict(
    "ListSchemasInputListSchemasPaginateTypeDef",
    {
        "RegistryId": NotRequired[RegistryIdTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListUsageProfilesRequestListUsageProfilesPaginateTypeDef = TypedDict(
    "ListUsageProfilesRequestListUsageProfilesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetConnectionsRequestGetConnectionsPaginateTypeDef = TypedDict(
    "GetConnectionsRequestGetConnectionsPaginateTypeDef",
    {
        "CatalogId": NotRequired[str],
        "Filter": NotRequired[GetConnectionsFilterTypeDef],
        "HidePassword": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetConnectionsRequestRequestTypeDef = TypedDict(
    "GetConnectionsRequestRequestTypeDef",
    {
        "CatalogId": NotRequired[str],
        "Filter": NotRequired[GetConnectionsFilterTypeDef],
        "HidePassword": NotRequired[bool],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
GetJobBookmarkResponseTypeDef = TypedDict(
    "GetJobBookmarkResponseTypeDef",
    {
        "JobBookmarkEntry": JobBookmarkEntryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResetJobBookmarkResponseTypeDef = TypedDict(
    "ResetJobBookmarkResponseTypeDef",
    {
        "JobBookmarkEntry": JobBookmarkEntryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TransformFilterCriteriaTypeDef = TypedDict(
    "TransformFilterCriteriaTypeDef",
    {
        "Name": NotRequired[str],
        "TransformType": NotRequired[Literal["FIND_MATCHES"]],
        "Status": NotRequired[TransformStatusTypeType],
        "GlueVersion": NotRequired[str],
        "CreatedBefore": NotRequired[TimestampTypeDef],
        "CreatedAfter": NotRequired[TimestampTypeDef],
        "LastModifiedBefore": NotRequired[TimestampTypeDef],
        "LastModifiedAfter": NotRequired[TimestampTypeDef],
        "Schema": NotRequired[Sequence[SchemaColumnTypeDef]],
    },
)
GetMappingResponseTypeDef = TypedDict(
    "GetMappingResponseTypeDef",
    {
        "Mapping": List[MappingEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPartitionsRequestGetPartitionsPaginateTypeDef = TypedDict(
    "GetPartitionsRequestGetPartitionsPaginateTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "Expression": NotRequired[str],
        "Segment": NotRequired[SegmentTypeDef],
        "ExcludeColumnSchema": NotRequired[bool],
        "TransactionId": NotRequired[str],
        "QueryAsOfTime": NotRequired[TimestampTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetPartitionsRequestRequestTypeDef = TypedDict(
    "GetPartitionsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "CatalogId": NotRequired[str],
        "Expression": NotRequired[str],
        "NextToken": NotRequired[str],
        "Segment": NotRequired[SegmentTypeDef],
        "MaxResults": NotRequired[int],
        "ExcludeColumnSchema": NotRequired[bool],
        "TransactionId": NotRequired[str],
        "QueryAsOfTime": NotRequired[TimestampTypeDef],
    },
)
GetResourcePoliciesResponseTypeDef = TypedDict(
    "GetResourcePoliciesResponseTypeDef",
    {
        "GetResourcePoliciesResponseList": List[GluePolicyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetSchemaVersionInputRequestTypeDef = TypedDict(
    "GetSchemaVersionInputRequestTypeDef",
    {
        "SchemaId": NotRequired[SchemaIdTypeDef],
        "SchemaVersionId": NotRequired[str],
        "SchemaVersionNumber": NotRequired[SchemaVersionNumberTypeDef],
    },
)
GetSchemaVersionsDiffInputRequestTypeDef = TypedDict(
    "GetSchemaVersionsDiffInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "FirstSchemaVersionNumber": SchemaVersionNumberTypeDef,
        "SecondSchemaVersionNumber": SchemaVersionNumberTypeDef,
        "SchemaDiffType": Literal["SYNTAX_DIFF"],
    },
)
UpdateSchemaInputRequestTypeDef = TypedDict(
    "UpdateSchemaInputRequestTypeDef",
    {
        "SchemaId": SchemaIdTypeDef,
        "SchemaVersionNumber": NotRequired[SchemaVersionNumberTypeDef],
        "Compatibility": NotRequired[CompatibilityType],
        "Description": NotRequired[str],
    },
)
GlueSchemaExtraOutputTypeDef = TypedDict(
    "GlueSchemaExtraOutputTypeDef",
    {
        "Columns": NotRequired[List[GlueStudioSchemaColumnTypeDef]],
    },
)
GlueSchemaOutputTypeDef = TypedDict(
    "GlueSchemaOutputTypeDef",
    {
        "Columns": NotRequired[List[GlueStudioSchemaColumnTypeDef]],
    },
)
GlueSchemaTypeDef = TypedDict(
    "GlueSchemaTypeDef",
    {
        "Columns": NotRequired[Sequence[GlueStudioSchemaColumnTypeDef]],
    },
)
GovernedCatalogSourceTypeDef = TypedDict(
    "GovernedCatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "PartitionPredicate": NotRequired[str],
        "AdditionalOptions": NotRequired[S3SourceAdditionalOptionsTypeDef],
    },
)
S3CatalogSourceTypeDef = TypedDict(
    "S3CatalogSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "PartitionPredicate": NotRequired[str],
        "AdditionalOptions": NotRequired[S3SourceAdditionalOptionsTypeDef],
    },
)
OpenTableFormatInputTypeDef = TypedDict(
    "OpenTableFormatInputTypeDef",
    {
        "IcebergInput": NotRequired[IcebergInputTypeDef],
    },
)
JobRunTypeDef = TypedDict(
    "JobRunTypeDef",
    {
        "Id": NotRequired[str],
        "Attempt": NotRequired[int],
        "PreviousRunId": NotRequired[str],
        "TriggerName": NotRequired[str],
        "JobName": NotRequired[str],
        "JobMode": NotRequired[JobModeType],
        "StartedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
        "CompletedOn": NotRequired[datetime],
        "JobRunState": NotRequired[JobRunStateType],
        "Arguments": NotRequired[Dict[str, str]],
        "ErrorMessage": NotRequired[str],
        "PredecessorRuns": NotRequired[List[PredecessorTypeDef]],
        "AllocatedCapacity": NotRequired[int],
        "ExecutionTime": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxCapacity": NotRequired[float],
        "WorkerType": NotRequired[WorkerTypeType],
        "NumberOfWorkers": NotRequired[int],
        "SecurityConfiguration": NotRequired[str],
        "LogGroupName": NotRequired[str],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "GlueVersion": NotRequired[str],
        "DPUSeconds": NotRequired[float],
        "ExecutionClass": NotRequired[ExecutionClassType],
        "MaintenanceWindow": NotRequired[str],
        "ProfileName": NotRequired[str],
    },
)
JoinExtraOutputTypeDef = TypedDict(
    "JoinExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "JoinType": JoinTypeType,
        "Columns": List[JoinColumnExtraOutputTypeDef],
    },
)
JoinOutputTypeDef = TypedDict(
    "JoinOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "JoinType": JoinTypeType,
        "Columns": List[JoinColumnOutputTypeDef],
    },
)
JoinTypeDef = TypedDict(
    "JoinTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "JoinType": JoinTypeType,
        "Columns": Sequence[JoinColumnTypeDef],
    },
)
TaskRunPropertiesTypeDef = TypedDict(
    "TaskRunPropertiesTypeDef",
    {
        "TaskType": NotRequired[TaskTypeType],
        "ImportLabelsTaskRunProperties": NotRequired[ImportLabelsTaskRunPropertiesTypeDef],
        "ExportLabelsTaskRunProperties": NotRequired[ExportLabelsTaskRunPropertiesTypeDef],
        "LabelingSetGenerationTaskRunProperties": NotRequired[
            LabelingSetGenerationTaskRunPropertiesTypeDef
        ],
        "FindMatchesTaskRunProperties": NotRequired[FindMatchesTaskRunPropertiesTypeDef],
    },
)
ListRegistriesResponseTypeDef = TypedDict(
    "ListRegistriesResponseTypeDef",
    {
        "Registries": List[RegistryListItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListSchemaVersionsResponseTypeDef = TypedDict(
    "ListSchemaVersionsResponseTypeDef",
    {
        "Schemas": List[SchemaVersionListItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListSchemasResponseTypeDef = TypedDict(
    "ListSchemasResponseTypeDef",
    {
        "Schemas": List[SchemaListItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListUsageProfilesResponseTypeDef = TypedDict(
    "ListUsageProfilesResponseTypeDef",
    {
        "Profiles": List[UsageProfileDefinitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
TransformEncryptionTypeDef = TypedDict(
    "TransformEncryptionTypeDef",
    {
        "MlUserDataEncryption": NotRequired[MLUserDataEncryptionTypeDef],
        "TaskRunSecurityConfigurationName": NotRequired[str],
    },
)
MetadataInfoTypeDef = TypedDict(
    "MetadataInfoTypeDef",
    {
        "MetadataValue": NotRequired[str],
        "CreatedTime": NotRequired[str],
        "OtherMetadataValueList": NotRequired[List[OtherMetadataValueListItemTypeDef]],
    },
)
PutSchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "PutSchemaVersionMetadataInputRequestTypeDef",
    {
        "MetadataKeyValue": MetadataKeyValuePairTypeDef,
        "SchemaId": NotRequired[SchemaIdTypeDef],
        "SchemaVersionNumber": NotRequired[SchemaVersionNumberTypeDef],
        "SchemaVersionId": NotRequired[str],
    },
)
QuerySchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "QuerySchemaVersionMetadataInputRequestTypeDef",
    {
        "SchemaId": NotRequired[SchemaIdTypeDef],
        "SchemaVersionNumber": NotRequired[SchemaVersionNumberTypeDef],
        "SchemaVersionId": NotRequired[str],
        "MetadataList": NotRequired[Sequence[MetadataKeyValuePairTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
RemoveSchemaVersionMetadataInputRequestTypeDef = TypedDict(
    "RemoveSchemaVersionMetadataInputRequestTypeDef",
    {
        "MetadataKeyValue": MetadataKeyValuePairTypeDef,
        "SchemaId": NotRequired[SchemaIdTypeDef],
        "SchemaVersionNumber": NotRequired[SchemaVersionNumberTypeDef],
        "SchemaVersionId": NotRequired[str],
    },
)
OAuth2PropertiesInputTypeDef = TypedDict(
    "OAuth2PropertiesInputTypeDef",
    {
        "OAuth2GrantType": NotRequired[OAuth2GrantTypeType],
        "OAuth2ClientApplication": NotRequired[OAuth2ClientApplicationTypeDef],
        "TokenUrl": NotRequired[str],
        "TokenUrlParametersMap": NotRequired[Mapping[str, str]],
        "AuthorizationCodeProperties": NotRequired[AuthorizationCodePropertiesTypeDef],
    },
)
OAuth2PropertiesTypeDef = TypedDict(
    "OAuth2PropertiesTypeDef",
    {
        "OAuth2GrantType": NotRequired[OAuth2GrantTypeType],
        "OAuth2ClientApplication": NotRequired[OAuth2ClientApplicationTypeDef],
        "TokenUrl": NotRequired[str],
        "TokenUrlParametersMap": NotRequired[Dict[str, str]],
    },
)
PartitionValueListUnionTypeDef = Union[
    PartitionValueListTypeDef, PartitionValueListExtraOutputTypeDef
]
RecipeExtraOutputTypeDef = TypedDict(
    "RecipeExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "RecipeReference": RecipeReferenceTypeDef,
    },
)
RecipeOutputTypeDef = TypedDict(
    "RecipeOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "RecipeReference": RecipeReferenceTypeDef,
    },
)
RecipeTypeDef = TypedDict(
    "RecipeTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "RecipeReference": RecipeReferenceTypeDef,
    },
)
RedshiftTargetExtraOutputTypeDef = TypedDict(
    "RedshiftTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
        "RedshiftTmpDir": NotRequired[str],
        "TmpDirIAMRole": NotRequired[str],
        "UpsertRedshiftOptions": NotRequired[UpsertRedshiftTargetOptionsExtraOutputTypeDef],
    },
)
RedshiftTargetOutputTypeDef = TypedDict(
    "RedshiftTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Database": str,
        "Table": str,
        "RedshiftTmpDir": NotRequired[str],
        "TmpDirIAMRole": NotRequired[str],
        "UpsertRedshiftOptions": NotRequired[UpsertRedshiftTargetOptionsOutputTypeDef],
    },
)
RedshiftTargetTypeDef = TypedDict(
    "RedshiftTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Database": str,
        "Table": str,
        "RedshiftTmpDir": NotRequired[str],
        "TmpDirIAMRole": NotRequired[str],
        "UpsertRedshiftOptions": NotRequired[UpsertRedshiftTargetOptionsTypeDef],
    },
)
UserDefinedFunctionInputTypeDef = TypedDict(
    "UserDefinedFunctionInputTypeDef",
    {
        "FunctionName": NotRequired[str],
        "ClassName": NotRequired[str],
        "OwnerName": NotRequired[str],
        "OwnerType": NotRequired[PrincipalTypeType],
        "ResourceUris": NotRequired[Sequence[ResourceUriTypeDef]],
    },
)
UserDefinedFunctionTypeDef = TypedDict(
    "UserDefinedFunctionTypeDef",
    {
        "FunctionName": NotRequired[str],
        "DatabaseName": NotRequired[str],
        "ClassName": NotRequired[str],
        "OwnerName": NotRequired[str],
        "OwnerType": NotRequired[PrincipalTypeType],
        "CreateTime": NotRequired[datetime],
        "ResourceUris": NotRequired[List[ResourceUriTypeDef]],
        "CatalogId": NotRequired[str],
    },
)
TableOptimizerRunTypeDef = TypedDict(
    "TableOptimizerRunTypeDef",
    {
        "eventType": NotRequired[TableOptimizerEventTypeType],
        "startTimestamp": NotRequired[datetime],
        "endTimestamp": NotRequired[datetime],
        "metrics": NotRequired[RunMetricsTypeDef],
        "error": NotRequired[str],
    },
)
SearchTablesRequestRequestTypeDef = TypedDict(
    "SearchTablesRequestRequestTypeDef",
    {
        "CatalogId": NotRequired[str],
        "NextToken": NotRequired[str],
        "Filters": NotRequired[Sequence[PropertyPredicateTypeDef]],
        "SearchText": NotRequired[str],
        "SortCriteria": NotRequired[Sequence[SortCriterionTypeDef]],
        "MaxResults": NotRequired[int],
        "ResourceShareType": NotRequired[ResourceShareTypeType],
    },
)
StatementOutputTypeDef = TypedDict(
    "StatementOutputTypeDef",
    {
        "Data": NotRequired[StatementOutputDataTypeDef],
        "ExecutionCount": NotRequired[int],
        "Status": NotRequired[StatementStateType],
        "ErrorName": NotRequired[str],
        "ErrorValue": NotRequired[str],
        "Traceback": NotRequired[List[str]],
    },
)
UpdateClassifierRequestRequestTypeDef = TypedDict(
    "UpdateClassifierRequestRequestTypeDef",
    {
        "GrokClassifier": NotRequired[UpdateGrokClassifierRequestTypeDef],
        "XMLClassifier": NotRequired[UpdateXMLClassifierRequestTypeDef],
        "JsonClassifier": NotRequired[UpdateJsonClassifierRequestTypeDef],
        "CsvClassifier": NotRequired[UpdateCsvClassifierRequestTypeDef],
    },
)
ViewDefinitionInputTypeDef = TypedDict(
    "ViewDefinitionInputTypeDef",
    {
        "IsProtected": NotRequired[bool],
        "Definer": NotRequired[str],
        "Representations": NotRequired[Sequence[ViewRepresentationInputTypeDef]],
        "SubObjects": NotRequired[Sequence[str]],
    },
)
ViewDefinitionTypeDef = TypedDict(
    "ViewDefinitionTypeDef",
    {
        "IsProtected": NotRequired[bool],
        "Definer": NotRequired[str],
        "SubObjects": NotRequired[List[str]],
        "Representations": NotRequired[List[ViewRepresentationTypeDef]],
    },
)
ActionUnionTypeDef = Union[ActionTypeDef, ActionExtraOutputTypeDef]
AmazonRedshiftSourceExtraOutputTypeDef = TypedDict(
    "AmazonRedshiftSourceExtraOutputTypeDef",
    {
        "Name": NotRequired[str],
        "Data": NotRequired[AmazonRedshiftNodeDataExtraOutputTypeDef],
    },
)
AmazonRedshiftTargetExtraOutputTypeDef = TypedDict(
    "AmazonRedshiftTargetExtraOutputTypeDef",
    {
        "Name": NotRequired[str],
        "Data": NotRequired[AmazonRedshiftNodeDataExtraOutputTypeDef],
        "Inputs": NotRequired[List[str]],
    },
)
AmazonRedshiftSourceOutputTypeDef = TypedDict(
    "AmazonRedshiftSourceOutputTypeDef",
    {
        "Name": NotRequired[str],
        "Data": NotRequired[AmazonRedshiftNodeDataOutputTypeDef],
    },
)
AmazonRedshiftTargetOutputTypeDef = TypedDict(
    "AmazonRedshiftTargetOutputTypeDef",
    {
        "Name": NotRequired[str],
        "Data": NotRequired[AmazonRedshiftNodeDataOutputTypeDef],
        "Inputs": NotRequired[List[str]],
    },
)
AmazonRedshiftSourceTypeDef = TypedDict(
    "AmazonRedshiftSourceTypeDef",
    {
        "Name": NotRequired[str],
        "Data": NotRequired[AmazonRedshiftNodeDataTypeDef],
    },
)
AmazonRedshiftTargetTypeDef = TypedDict(
    "AmazonRedshiftTargetTypeDef",
    {
        "Name": NotRequired[str],
        "Data": NotRequired[AmazonRedshiftNodeDataTypeDef],
        "Inputs": NotRequired[Sequence[str]],
    },
)
SnowflakeTargetExtraOutputTypeDef = TypedDict(
    "SnowflakeTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Data": SnowflakeNodeDataExtraOutputTypeDef,
        "Inputs": NotRequired[List[str]],
    },
)
SnowflakeTargetOutputTypeDef = TypedDict(
    "SnowflakeTargetOutputTypeDef",
    {
        "Name": str,
        "Data": SnowflakeNodeDataOutputTypeDef,
        "Inputs": NotRequired[List[str]],
    },
)
SnowflakeTargetTypeDef = TypedDict(
    "SnowflakeTargetTypeDef",
    {
        "Name": str,
        "Data": SnowflakeNodeDataTypeDef,
        "Inputs": NotRequired[Sequence[str]],
    },
)
PartitionIndexDescriptorTypeDef = TypedDict(
    "PartitionIndexDescriptorTypeDef",
    {
        "IndexName": str,
        "Keys": List[KeySchemaElementTypeDef],
        "IndexStatus": PartitionIndexStatusType,
        "BackfillErrors": NotRequired[List[BackfillErrorTypeDef]],
    },
)
BatchStopJobRunResponseTypeDef = TypedDict(
    "BatchStopJobRunResponseTypeDef",
    {
        "SuccessfulSubmissions": List[BatchStopJobRunSuccessfulSubmissionTypeDef],
        "Errors": List[BatchStopJobRunErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchUpdatePartitionResponseTypeDef = TypedDict(
    "BatchUpdatePartitionResponseTypeDef",
    {
        "Errors": List[BatchUpdatePartitionFailureEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchCreatePartitionResponseTypeDef = TypedDict(
    "BatchCreatePartitionResponseTypeDef",
    {
        "Errors": List[PartitionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchDeletePartitionResponseTypeDef = TypedDict(
    "BatchDeletePartitionResponseTypeDef",
    {
        "Errors": List[PartitionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchDeleteTableResponseTypeDef = TypedDict(
    "BatchDeleteTableResponseTypeDef",
    {
        "Errors": List[TableErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchDeleteTableVersionResponseTypeDef = TypedDict(
    "BatchDeleteTableVersionResponseTypeDef",
    {
        "Errors": List[TableVersionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DecimalColumnStatisticsDataTypeDef = TypedDict(
    "DecimalColumnStatisticsDataTypeDef",
    {
        "NumberOfNulls": int,
        "NumberOfDistinctValues": int,
        "MinimumValue": NotRequired[DecimalNumberTypeDef],
        "MaximumValue": NotRequired[DecimalNumberTypeDef],
    },
)
BatchGetBlueprintsResponseTypeDef = TypedDict(
    "BatchGetBlueprintsResponseTypeDef",
    {
        "Blueprints": List[BlueprintTypeDef],
        "MissingBlueprints": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetBlueprintResponseTypeDef = TypedDict(
    "GetBlueprintResponseTypeDef",
    {
        "Blueprint": BlueprintTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetClassifierResponseTypeDef = TypedDict(
    "GetClassifierResponseTypeDef",
    {
        "Classifier": ClassifierTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetClassifiersResponseTypeDef = TypedDict(
    "GetClassifiersResponseTypeDef",
    {
        "Classifiers": List[ClassifierTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetDataflowGraphResponseTypeDef = TypedDict(
    "GetDataflowGraphResponseTypeDef",
    {
        "DagNodes": List[CodeGenNodeOutputTypeDef],
        "DagEdges": List[CodeGenEdgeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CodeGenNodeUnionTypeDef = Union[CodeGenNodeTypeDef, CodeGenNodeOutputTypeDef]
GetMappingRequestRequestTypeDef = TypedDict(
    "GetMappingRequestRequestTypeDef",
    {
        "Source": CatalogEntryTypeDef,
        "Sinks": NotRequired[Sequence[CatalogEntryTypeDef]],
        "Location": NotRequired[LocationTypeDef],
    },
)
GetPlanRequestRequestTypeDef = TypedDict(
    "GetPlanRequestRequestTypeDef",
    {
        "Mapping": Sequence[MappingEntryTypeDef],
        "Source": CatalogEntryTypeDef,
        "Sinks": NotRequired[Sequence[CatalogEntryTypeDef]],
        "Location": NotRequired[LocationTypeDef],
        "Language": NotRequired[LanguageType],
        "AdditionalPlanOptionsMap": NotRequired[Mapping[str, str]],
    },
)
CatalogKafkaSourceTypeDef = TypedDict(
    "CatalogKafkaSourceTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KafkaStreamingSourceOptionsTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
DirectKafkaSourceTypeDef = TypedDict(
    "DirectKafkaSourceTypeDef",
    {
        "Name": str,
        "StreamingOptions": NotRequired[KafkaStreamingSourceOptionsTypeDef],
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
CatalogKinesisSourceTypeDef = TypedDict(
    "CatalogKinesisSourceTypeDef",
    {
        "Name": str,
        "Table": str,
        "Database": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KinesisStreamingSourceOptionsTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
DirectKinesisSourceTypeDef = TypedDict(
    "DirectKinesisSourceTypeDef",
    {
        "Name": str,
        "WindowSize": NotRequired[int],
        "DetectSchema": NotRequired[bool],
        "StreamingOptions": NotRequired[KinesisStreamingSourceOptionsTypeDef],
        "DataPreviewOptions": NotRequired[StreamingDataPreviewOptionsTypeDef],
    },
)
GetUnfilteredPartitionMetadataRequestRequestTypeDef = TypedDict(
    "GetUnfilteredPartitionMetadataRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
        "Region": NotRequired[str],
        "AuditContext": NotRequired[AuditContextTypeDef],
        "QuerySessionContext": NotRequired[QuerySessionContextTypeDef],
    },
)
GetUnfilteredPartitionsMetadataRequestRequestTypeDef = TypedDict(
    "GetUnfilteredPartitionsMetadataRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
        "Region": NotRequired[str],
        "Expression": NotRequired[str],
        "AuditContext": NotRequired[AuditContextTypeDef],
        "NextToken": NotRequired[str],
        "Segment": NotRequired[SegmentTypeDef],
        "MaxResults": NotRequired[int],
        "QuerySessionContext": NotRequired[QuerySessionContextTypeDef],
    },
)
GetUnfilteredTableMetadataRequestRequestTypeDef = TypedDict(
    "GetUnfilteredTableMetadataRequestRequestTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "Name": str,
        "SupportedPermissionTypes": Sequence[PermissionTypeType],
        "Region": NotRequired[str],
        "AuditContext": NotRequired[AuditContextTypeDef],
        "ParentResourceArn": NotRequired[str],
        "RootResourceArn": NotRequired[str],
        "SupportedDialect": NotRequired[SupportedDialectTypeDef],
        "Permissions": NotRequired[Sequence[PermissionType]],
        "QuerySessionContext": NotRequired[QuerySessionContextTypeDef],
    },
)
GetMLTaskRunsRequestRequestTypeDef = TypedDict(
    "GetMLTaskRunsRequestRequestTypeDef",
    {
        "TransformId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filter": NotRequired[TaskRunFilterCriteriaTypeDef],
        "Sort": NotRequired[TaskRunSortCriteriaTypeDef],
    },
)
TriggerTypeDef = TypedDict(
    "TriggerTypeDef",
    {
        "Name": NotRequired[str],
        "WorkflowName": NotRequired[str],
        "Id": NotRequired[str],
        "Type": NotRequired[TriggerTypeType],
        "State": NotRequired[TriggerStateType],
        "Description": NotRequired[str],
        "Schedule": NotRequired[str],
        "Actions": NotRequired[List[ActionOutputTypeDef]],
        "Predicate": NotRequired[PredicateOutputTypeDef],
        "EventBatchingCondition": NotRequired[EventBatchingConditionTypeDef],
    },
)
PredicateUnionTypeDef = Union[PredicateTypeDef, PredicateExtraOutputTypeDef]
TriggerUpdateTypeDef = TypedDict(
    "TriggerUpdateTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Schedule": NotRequired[str],
        "Actions": NotRequired[Sequence[ActionTypeDef]],
        "Predicate": NotRequired[PredicateTypeDef],
        "EventBatchingCondition": NotRequired[EventBatchingConditionTypeDef],
    },
)
GetUsageProfileResponseTypeDef = TypedDict(
    "GetUsageProfileResponseTypeDef",
    {
        "Name": str,
        "Description": str,
        "Configuration": ProfileConfigurationOutputTypeDef,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateUsageProfileRequestRequestTypeDef = TypedDict(
    "CreateUsageProfileRequestRequestTypeDef",
    {
        "Name": str,
        "Configuration": ProfileConfigurationTypeDef,
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ProfileConfigurationUnionTypeDef = Union[
    ProfileConfigurationTypeDef, ProfileConfigurationOutputTypeDef
]
UpdateUsageProfileRequestRequestTypeDef = TypedDict(
    "UpdateUsageProfileRequestRequestTypeDef",
    {
        "Name": str,
        "Configuration": ProfileConfigurationTypeDef,
        "Description": NotRequired[str],
    },
)
EvaluationMetricsTypeDef = TypedDict(
    "EvaluationMetricsTypeDef",
    {
        "TransformType": Literal["FIND_MATCHES"],
        "FindMatchesMetrics": NotRequired[FindMatchesMetricsTypeDef],
    },
)
CrawlerTypeDef = TypedDict(
    "CrawlerTypeDef",
    {
        "Name": NotRequired[str],
        "Role": NotRequired[str],
        "Targets": NotRequired[CrawlerTargetsOutputTypeDef],
        "DatabaseName": NotRequired[str],
        "Description": NotRequired[str],
        "Classifiers": NotRequired[List[str]],
        "RecrawlPolicy": NotRequired[RecrawlPolicyTypeDef],
        "SchemaChangePolicy": NotRequired[SchemaChangePolicyTypeDef],
        "LineageConfiguration": NotRequired[LineageConfigurationTypeDef],
        "State": NotRequired[CrawlerStateType],
        "TablePrefix": NotRequired[str],
        "Schedule": NotRequired[ScheduleTypeDef],
        "CrawlElapsedTime": NotRequired[int],
        "CreationTime": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "LastCrawl": NotRequired[LastCrawlInfoTypeDef],
        "Version": NotRequired[int],
        "Configuration": NotRequired[str],
        "CrawlerSecurityConfiguration": NotRequired[str],
        "LakeFormationConfiguration": NotRequired[LakeFormationConfigurationTypeDef],
    },
)
CrawlerTargetsUnionTypeDef = Union[CrawlerTargetsTypeDef, CrawlerTargetsExtraOutputTypeDef]
CreateCrawlerRequestRequestTypeDef = TypedDict(
    "CreateCrawlerRequestRequestTypeDef",
    {
        "Name": str,
        "Role": str,
        "Targets": CrawlerTargetsTypeDef,
        "DatabaseName": NotRequired[str],
        "Description": NotRequired[str],
        "Schedule": NotRequired[str],
        "Classifiers": NotRequired[Sequence[str]],
        "TablePrefix": NotRequired[str],
        "SchemaChangePolicy": NotRequired[SchemaChangePolicyTypeDef],
        "RecrawlPolicy": NotRequired[RecrawlPolicyTypeDef],
        "LineageConfiguration": NotRequired[LineageConfigurationTypeDef],
        "LakeFormationConfiguration": NotRequired[LakeFormationConfigurationTypeDef],
        "Configuration": NotRequired[str],
        "CrawlerSecurityConfiguration": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
UpdateCrawlerRequestRequestTypeDef = TypedDict(
    "UpdateCrawlerRequestRequestTypeDef",
    {
        "Name": str,
        "Role": NotRequired[str],
        "DatabaseName": NotRequired[str],
        "Description": NotRequired[str],
        "Targets": NotRequired[CrawlerTargetsTypeDef],
        "Schedule": NotRequired[str],
        "Classifiers": NotRequired[Sequence[str]],
        "TablePrefix": NotRequired[str],
        "SchemaChangePolicy": NotRequired[SchemaChangePolicyTypeDef],
        "RecrawlPolicy": NotRequired[RecrawlPolicyTypeDef],
        "LineageConfiguration": NotRequired[LineageConfigurationTypeDef],
        "LakeFormationConfiguration": NotRequired[LakeFormationConfigurationTypeDef],
        "Configuration": NotRequired[str],
        "CrawlerSecurityConfiguration": NotRequired[str],
    },
)
ListDataQualityRulesetsRequestRequestTypeDef = TypedDict(
    "ListDataQualityRulesetsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filter": NotRequired[DataQualityRulesetFilterCriteriaTypeDef],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
ListDataQualityRulesetsResponseTypeDef = TypedDict(
    "ListDataQualityRulesetsResponseTypeDef",
    {
        "Rulesets": List[DataQualityRulesetListDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
CreateSessionResponseTypeDef = TypedDict(
    "CreateSessionResponseTypeDef",
    {
        "Session": SessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "Session": SessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListSessionsResponseTypeDef = TypedDict(
    "ListSessionsResponseTypeDef",
    {
        "Ids": List[str],
        "Sessions": List[SessionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetDataCatalogEncryptionSettingsResponseTypeDef = TypedDict(
    "GetDataCatalogEncryptionSettingsResponseTypeDef",
    {
        "DataCatalogEncryptionSettings": DataCatalogEncryptionSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutDataCatalogEncryptionSettingsRequestRequestTypeDef = TypedDict(
    "PutDataCatalogEncryptionSettingsRequestRequestTypeDef",
    {
        "DataCatalogEncryptionSettings": DataCatalogEncryptionSettingsTypeDef,
        "CatalogId": NotRequired[str],
    },
)
DatabaseTypeDef = TypedDict(
    "DatabaseTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "LocationUri": NotRequired[str],
        "Parameters": NotRequired[Dict[str, str]],
        "CreateTime": NotRequired[datetime],
        "CreateTableDefaultPermissions": NotRequired[List[PrincipalPermissionsOutputTypeDef]],
        "TargetDatabase": NotRequired[DatabaseIdentifierTypeDef],
        "CatalogId": NotRequired[str],
        "FederatedDatabase": NotRequired[FederatedDatabaseTypeDef],
    },
)
DatabaseInputTypeDef = TypedDict(
    "DatabaseInputTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "LocationUri": NotRequired[str],
        "Parameters": NotRequired[Mapping[str, str]],
        "CreateTableDefaultPermissions": NotRequired[Sequence[PrincipalPermissionsTypeDef]],
        "TargetDatabase": NotRequired[DatabaseIdentifierTypeDef],
        "FederatedDatabase": NotRequired[FederatedDatabaseTypeDef],
    },
)
DataQualityObservationTypeDef = TypedDict(
    "DataQualityObservationTypeDef",
    {
        "Description": NotRequired[str],
        "MetricBasedObservation": NotRequired[MetricBasedObservationTypeDef],
    },
)
DataQualityResultDescriptionTypeDef = TypedDict(
    "DataQualityResultDescriptionTypeDef",
    {
        "ResultId": NotRequired[str],
        "DataSource": NotRequired[DataSourceOutputTypeDef],
        "JobName": NotRequired[str],
        "JobRunId": NotRequired[str],
        "StartedOn": NotRequired[datetime],
    },
)
DataQualityRuleRecommendationRunDescriptionTypeDef = TypedDict(
    "DataQualityRuleRecommendationRunDescriptionTypeDef",
    {
        "RunId": NotRequired[str],
        "Status": NotRequired[TaskStatusTypeType],
        "StartedOn": NotRequired[datetime],
        "DataSource": NotRequired[DataSourceOutputTypeDef],
    },
)
DataQualityRulesetEvaluationRunDescriptionTypeDef = TypedDict(
    "DataQualityRulesetEvaluationRunDescriptionTypeDef",
    {
        "RunId": NotRequired[str],
        "Status": NotRequired[TaskStatusTypeType],
        "StartedOn": NotRequired[datetime],
        "DataSource": NotRequired[DataSourceOutputTypeDef],
    },
)
GetDataQualityRuleRecommendationRunResponseTypeDef = TypedDict(
    "GetDataQualityRuleRecommendationRunResponseTypeDef",
    {
        "RunId": str,
        "DataSource": DataSourceOutputTypeDef,
        "Role": str,
        "NumberOfWorkers": int,
        "Timeout": int,
        "Status": TaskStatusTypeType,
        "ErrorString": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "ExecutionTime": int,
        "RecommendedRuleset": str,
        "CreatedRulesetName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataQualityRulesetEvaluationRunResponseTypeDef = TypedDict(
    "GetDataQualityRulesetEvaluationRunResponseTypeDef",
    {
        "RunId": str,
        "DataSource": DataSourceOutputTypeDef,
        "Role": str,
        "NumberOfWorkers": int,
        "Timeout": int,
        "AdditionalRunOptions": DataQualityEvaluationRunAdditionalRunOptionsTypeDef,
        "Status": TaskStatusTypeType,
        "ErrorString": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "ExecutionTime": int,
        "RulesetNames": List[str],
        "ResultIds": List[str],
        "AdditionalDataSources": Dict[str, DataSourceOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataQualityResultFilterCriteriaTypeDef = TypedDict(
    "DataQualityResultFilterCriteriaTypeDef",
    {
        "DataSource": NotRequired[DataSourceTypeDef],
        "JobName": NotRequired[str],
        "JobRunId": NotRequired[str],
        "StartedAfter": NotRequired[TimestampTypeDef],
        "StartedBefore": NotRequired[TimestampTypeDef],
    },
)
DataQualityRuleRecommendationRunFilterTypeDef = TypedDict(
    "DataQualityRuleRecommendationRunFilterTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "StartedBefore": NotRequired[TimestampTypeDef],
        "StartedAfter": NotRequired[TimestampTypeDef],
    },
)
DataQualityRulesetEvaluationRunFilterTypeDef = TypedDict(
    "DataQualityRulesetEvaluationRunFilterTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "StartedBefore": NotRequired[TimestampTypeDef],
        "StartedAfter": NotRequired[TimestampTypeDef],
    },
)
DataSourceUnionTypeDef = Union[DataSourceTypeDef, DataSourceOutputTypeDef]
StartDataQualityRuleRecommendationRunRequestRequestTypeDef = TypedDict(
    "StartDataQualityRuleRecommendationRunRequestRequestTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "Role": str,
        "NumberOfWorkers": NotRequired[int],
        "Timeout": NotRequired[int],
        "CreatedRulesetName": NotRequired[str],
        "ClientToken": NotRequired[str],
    },
)
DropNullFieldsExtraOutputTypeDef = TypedDict(
    "DropNullFieldsExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "NullCheckBoxList": NotRequired[NullCheckBoxListTypeDef],
        "NullTextList": NotRequired[List[NullValueFieldTypeDef]],
    },
)
DropNullFieldsOutputTypeDef = TypedDict(
    "DropNullFieldsOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "NullCheckBoxList": NotRequired[NullCheckBoxListTypeDef],
        "NullTextList": NotRequired[List[NullValueFieldTypeDef]],
    },
)
DropNullFieldsTypeDef = TypedDict(
    "DropNullFieldsTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "NullCheckBoxList": NotRequired[NullCheckBoxListTypeDef],
        "NullTextList": NotRequired[Sequence[NullValueFieldTypeDef]],
    },
)
ColumnStatisticsDataOutputTypeDef = TypedDict(
    "ColumnStatisticsDataOutputTypeDef",
    {
        "Type": ColumnStatisticsTypeType,
        "BooleanColumnStatisticsData": NotRequired[BooleanColumnStatisticsDataTypeDef],
        "DateColumnStatisticsData": NotRequired[DateColumnStatisticsDataOutputTypeDef],
        "DecimalColumnStatisticsData": NotRequired[DecimalColumnStatisticsDataOutputTypeDef],
        "DoubleColumnStatisticsData": NotRequired[DoubleColumnStatisticsDataTypeDef],
        "LongColumnStatisticsData": NotRequired[LongColumnStatisticsDataTypeDef],
        "StringColumnStatisticsData": NotRequired[StringColumnStatisticsDataTypeDef],
        "BinaryColumnStatisticsData": NotRequired[BinaryColumnStatisticsDataTypeDef],
    },
)
StorageDescriptorOutputTypeDef = TypedDict(
    "StorageDescriptorOutputTypeDef",
    {
        "Columns": NotRequired[List[ColumnOutputTypeDef]],
        "Location": NotRequired[str],
        "AdditionalLocations": NotRequired[List[str]],
        "InputFormat": NotRequired[str],
        "OutputFormat": NotRequired[str],
        "Compressed": NotRequired[bool],
        "NumberOfBuckets": NotRequired[int],
        "SerdeInfo": NotRequired[SerDeInfoOutputTypeDef],
        "BucketColumns": NotRequired[List[str]],
        "SortColumns": NotRequired[List[OrderTypeDef]],
        "Parameters": NotRequired[Dict[str, str]],
        "SkewedInfo": NotRequired[SkewedInfoOutputTypeDef],
        "StoredAsSubDirectories": NotRequired[bool],
        "SchemaReference": NotRequired[SchemaReferenceTypeDef],
    },
)
StorageDescriptorTypeDef = TypedDict(
    "StorageDescriptorTypeDef",
    {
        "Columns": NotRequired[Sequence[ColumnTypeDef]],
        "Location": NotRequired[str],
        "AdditionalLocations": NotRequired[Sequence[str]],
        "InputFormat": NotRequired[str],
        "OutputFormat": NotRequired[str],
        "Compressed": NotRequired[bool],
        "NumberOfBuckets": NotRequired[int],
        "SerdeInfo": NotRequired[SerDeInfoTypeDef],
        "BucketColumns": NotRequired[Sequence[str]],
        "SortColumns": NotRequired[Sequence[OrderTypeDef]],
        "Parameters": NotRequired[Mapping[str, str]],
        "SkewedInfo": NotRequired[SkewedInfoTypeDef],
        "StoredAsSubDirectories": NotRequired[bool],
        "SchemaReference": NotRequired[SchemaReferenceTypeDef],
    },
)
SecurityConfigurationTypeDef = TypedDict(
    "SecurityConfigurationTypeDef",
    {
        "Name": NotRequired[str],
        "CreatedTimeStamp": NotRequired[datetime],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationOutputTypeDef],
    },
)
CreateSecurityConfigurationRequestRequestTypeDef = TypedDict(
    "CreateSecurityConfigurationRequestRequestTypeDef",
    {
        "Name": str,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
)
EncryptionConfigurationUnionTypeDef = Union[
    EncryptionConfigurationTypeDef, EncryptionConfigurationExtraOutputTypeDef
]
DeleteSchemaVersionsResponseTypeDef = TypedDict(
    "DeleteSchemaVersionsResponseTypeDef",
    {
        "SchemaVersionErrors": List[SchemaVersionErrorItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FilterExtraOutputTypeDef = TypedDict(
    "FilterExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "LogicalOperator": FilterLogicalOperatorType,
        "Filters": List[FilterExpressionExtraOutputTypeDef],
    },
)
FilterOutputTypeDef = TypedDict(
    "FilterOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "LogicalOperator": FilterLogicalOperatorType,
        "Filters": List[FilterExpressionOutputTypeDef],
    },
)
FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "LogicalOperator": FilterLogicalOperatorType,
        "Filters": Sequence[FilterExpressionTypeDef],
    },
)
UpdateMLTransformRequestRequestTypeDef = TypedDict(
    "UpdateMLTransformRequestRequestTypeDef",
    {
        "TransformId": str,
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Parameters": NotRequired[TransformParametersTypeDef],
        "Role": NotRequired[str],
        "GlueVersion": NotRequired[str],
        "MaxCapacity": NotRequired[float],
        "WorkerType": NotRequired[WorkerTypeType],
        "NumberOfWorkers": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxRetries": NotRequired[int],
    },
)
GetMLTransformsRequestRequestTypeDef = TypedDict(
    "GetMLTransformsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filter": NotRequired[TransformFilterCriteriaTypeDef],
        "Sort": NotRequired[TransformSortCriteriaTypeDef],
    },
)
ListMLTransformsRequestRequestTypeDef = TypedDict(
    "ListMLTransformsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filter": NotRequired[TransformFilterCriteriaTypeDef],
        "Sort": NotRequired[TransformSortCriteriaTypeDef],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
AthenaConnectorSourceExtraOutputTypeDef = TypedDict(
    "AthenaConnectorSourceExtraOutputTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "SchemaName": str,
        "ConnectionTable": NotRequired[str],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
CatalogDeltaSourceExtraOutputTypeDef = TypedDict(
    "CatalogDeltaSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalDeltaOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
CatalogHudiSourceExtraOutputTypeDef = TypedDict(
    "CatalogHudiSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalHudiOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
ConnectorDataSourceExtraOutputTypeDef = TypedDict(
    "ConnectorDataSourceExtraOutputTypeDef",
    {
        "Name": str,
        "ConnectionType": str,
        "Data": Dict[str, str],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
CustomCodeExtraOutputTypeDef = TypedDict(
    "CustomCodeExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Code": str,
        "ClassName": str,
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
DynamicTransformExtraOutputTypeDef = TypedDict(
    "DynamicTransformExtraOutputTypeDef",
    {
        "Name": str,
        "TransformName": str,
        "Inputs": List[str],
        "FunctionName": str,
        "Path": str,
        "Parameters": NotRequired[List[TransformConfigParameterExtraOutputTypeDef]],
        "Version": NotRequired[str],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
JDBCConnectorSourceExtraOutputTypeDef = TypedDict(
    "JDBCConnectorSourceExtraOutputTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[JDBCConnectorOptionsExtraOutputTypeDef],
        "ConnectionTable": NotRequired[str],
        "Query": NotRequired[str],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
JDBCConnectorTargetExtraOutputTypeDef = TypedDict(
    "JDBCConnectorTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ConnectionName": str,
        "ConnectionTable": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
S3CatalogDeltaSourceExtraOutputTypeDef = TypedDict(
    "S3CatalogDeltaSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalDeltaOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
S3CatalogHudiSourceExtraOutputTypeDef = TypedDict(
    "S3CatalogHudiSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalHudiOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
S3CsvSourceExtraOutputTypeDef = TypedDict(
    "S3CsvSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "Separator": SeparatorType,
        "QuoteChar": QuoteCharType,
        "CompressionType": NotRequired[CompressionTypeType],
        "Exclusions": NotRequired[List[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "Escaper": NotRequired[str],
        "Multiline": NotRequired[bool],
        "WithHeader": NotRequired[bool],
        "WriteHeader": NotRequired[bool],
        "SkipFirst": NotRequired[bool],
        "OptimizePerformance": NotRequired[bool],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
S3DeltaSourceExtraOutputTypeDef = TypedDict(
    "S3DeltaSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "AdditionalDeltaOptions": NotRequired[Dict[str, str]],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
S3HudiSourceExtraOutputTypeDef = TypedDict(
    "S3HudiSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "AdditionalHudiOptions": NotRequired[Dict[str, str]],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
S3JsonSourceExtraOutputTypeDef = TypedDict(
    "S3JsonSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "CompressionType": NotRequired[CompressionTypeType],
        "Exclusions": NotRequired[List[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "JsonPath": NotRequired[str],
        "Multiline": NotRequired[bool],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
S3ParquetSourceExtraOutputTypeDef = TypedDict(
    "S3ParquetSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "CompressionType": NotRequired[ParquetCompressionTypeType],
        "Exclusions": NotRequired[List[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
SnowflakeSourceExtraOutputTypeDef = TypedDict(
    "SnowflakeSourceExtraOutputTypeDef",
    {
        "Name": str,
        "Data": SnowflakeNodeDataExtraOutputTypeDef,
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
SparkConnectorSourceExtraOutputTypeDef = TypedDict(
    "SparkConnectorSourceExtraOutputTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
SparkConnectorTargetExtraOutputTypeDef = TypedDict(
    "SparkConnectorTargetExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
SparkSQLExtraOutputTypeDef = TypedDict(
    "SparkSQLExtraOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "SqlQuery": str,
        "SqlAliases": List[SqlAliasTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaExtraOutputTypeDef]],
    },
)
AthenaConnectorSourceOutputTypeDef = TypedDict(
    "AthenaConnectorSourceOutputTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "SchemaName": str,
        "ConnectionTable": NotRequired[str],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
CatalogDeltaSourceOutputTypeDef = TypedDict(
    "CatalogDeltaSourceOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalDeltaOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
CatalogHudiSourceOutputTypeDef = TypedDict(
    "CatalogHudiSourceOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalHudiOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
ConnectorDataSourceOutputTypeDef = TypedDict(
    "ConnectorDataSourceOutputTypeDef",
    {
        "Name": str,
        "ConnectionType": str,
        "Data": Dict[str, str],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
CustomCodeOutputTypeDef = TypedDict(
    "CustomCodeOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "Code": str,
        "ClassName": str,
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
DynamicTransformOutputTypeDef = TypedDict(
    "DynamicTransformOutputTypeDef",
    {
        "Name": str,
        "TransformName": str,
        "Inputs": List[str],
        "FunctionName": str,
        "Path": str,
        "Parameters": NotRequired[List[TransformConfigParameterOutputTypeDef]],
        "Version": NotRequired[str],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
JDBCConnectorSourceOutputTypeDef = TypedDict(
    "JDBCConnectorSourceOutputTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[JDBCConnectorOptionsOutputTypeDef],
        "ConnectionTable": NotRequired[str],
        "Query": NotRequired[str],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
JDBCConnectorTargetOutputTypeDef = TypedDict(
    "JDBCConnectorTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ConnectionName": str,
        "ConnectionTable": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
S3CatalogDeltaSourceOutputTypeDef = TypedDict(
    "S3CatalogDeltaSourceOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalDeltaOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
S3CatalogHudiSourceOutputTypeDef = TypedDict(
    "S3CatalogHudiSourceOutputTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalHudiOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
S3CsvSourceOutputTypeDef = TypedDict(
    "S3CsvSourceOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "Separator": SeparatorType,
        "QuoteChar": QuoteCharType,
        "CompressionType": NotRequired[CompressionTypeType],
        "Exclusions": NotRequired[List[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "Escaper": NotRequired[str],
        "Multiline": NotRequired[bool],
        "WithHeader": NotRequired[bool],
        "WriteHeader": NotRequired[bool],
        "SkipFirst": NotRequired[bool],
        "OptimizePerformance": NotRequired[bool],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
S3DeltaSourceOutputTypeDef = TypedDict(
    "S3DeltaSourceOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "AdditionalDeltaOptions": NotRequired[Dict[str, str]],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
S3HudiSourceOutputTypeDef = TypedDict(
    "S3HudiSourceOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "AdditionalHudiOptions": NotRequired[Dict[str, str]],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
S3JsonSourceOutputTypeDef = TypedDict(
    "S3JsonSourceOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "CompressionType": NotRequired[CompressionTypeType],
        "Exclusions": NotRequired[List[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "JsonPath": NotRequired[str],
        "Multiline": NotRequired[bool],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
S3ParquetSourceOutputTypeDef = TypedDict(
    "S3ParquetSourceOutputTypeDef",
    {
        "Name": str,
        "Paths": List[str],
        "CompressionType": NotRequired[ParquetCompressionTypeType],
        "Exclusions": NotRequired[List[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
SnowflakeSourceOutputTypeDef = TypedDict(
    "SnowflakeSourceOutputTypeDef",
    {
        "Name": str,
        "Data": SnowflakeNodeDataOutputTypeDef,
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
SparkConnectorSourceOutputTypeDef = TypedDict(
    "SparkConnectorSourceOutputTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
SparkConnectorTargetOutputTypeDef = TypedDict(
    "SparkConnectorTargetOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Dict[str, str]],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
SparkSQLOutputTypeDef = TypedDict(
    "SparkSQLOutputTypeDef",
    {
        "Name": str,
        "Inputs": List[str],
        "SqlQuery": str,
        "SqlAliases": List[SqlAliasTypeDef],
        "OutputSchemas": NotRequired[List[GlueSchemaOutputTypeDef]],
    },
)
AthenaConnectorSourceTypeDef = TypedDict(
    "AthenaConnectorSourceTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "SchemaName": str,
        "ConnectionTable": NotRequired[str],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
CatalogDeltaSourceTypeDef = TypedDict(
    "CatalogDeltaSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalDeltaOptions": NotRequired[Mapping[str, str]],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
CatalogHudiSourceTypeDef = TypedDict(
    "CatalogHudiSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalHudiOptions": NotRequired[Mapping[str, str]],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
ConnectorDataSourceTypeDef = TypedDict(
    "ConnectorDataSourceTypeDef",
    {
        "Name": str,
        "ConnectionType": str,
        "Data": Mapping[str, str],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
CustomCodeTypeDef = TypedDict(
    "CustomCodeTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "Code": str,
        "ClassName": str,
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
DynamicTransformTypeDef = TypedDict(
    "DynamicTransformTypeDef",
    {
        "Name": str,
        "TransformName": str,
        "Inputs": Sequence[str],
        "FunctionName": str,
        "Path": str,
        "Parameters": NotRequired[Sequence[TransformConfigParameterTypeDef]],
        "Version": NotRequired[str],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
JDBCConnectorSourceTypeDef = TypedDict(
    "JDBCConnectorSourceTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[JDBCConnectorOptionsTypeDef],
        "ConnectionTable": NotRequired[str],
        "Query": NotRequired[str],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
JDBCConnectorTargetTypeDef = TypedDict(
    "JDBCConnectorTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "ConnectionName": str,
        "ConnectionTable": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Mapping[str, str]],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
S3CatalogDeltaSourceTypeDef = TypedDict(
    "S3CatalogDeltaSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalDeltaOptions": NotRequired[Mapping[str, str]],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
S3CatalogHudiSourceTypeDef = TypedDict(
    "S3CatalogHudiSourceTypeDef",
    {
        "Name": str,
        "Database": str,
        "Table": str,
        "AdditionalHudiOptions": NotRequired[Mapping[str, str]],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
S3CsvSourceTypeDef = TypedDict(
    "S3CsvSourceTypeDef",
    {
        "Name": str,
        "Paths": Sequence[str],
        "Separator": SeparatorType,
        "QuoteChar": QuoteCharType,
        "CompressionType": NotRequired[CompressionTypeType],
        "Exclusions": NotRequired[Sequence[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "Escaper": NotRequired[str],
        "Multiline": NotRequired[bool],
        "WithHeader": NotRequired[bool],
        "WriteHeader": NotRequired[bool],
        "SkipFirst": NotRequired[bool],
        "OptimizePerformance": NotRequired[bool],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
S3DeltaSourceTypeDef = TypedDict(
    "S3DeltaSourceTypeDef",
    {
        "Name": str,
        "Paths": Sequence[str],
        "AdditionalDeltaOptions": NotRequired[Mapping[str, str]],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
S3HudiSourceTypeDef = TypedDict(
    "S3HudiSourceTypeDef",
    {
        "Name": str,
        "Paths": Sequence[str],
        "AdditionalHudiOptions": NotRequired[Mapping[str, str]],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
S3JsonSourceTypeDef = TypedDict(
    "S3JsonSourceTypeDef",
    {
        "Name": str,
        "Paths": Sequence[str],
        "CompressionType": NotRequired[CompressionTypeType],
        "Exclusions": NotRequired[Sequence[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "JsonPath": NotRequired[str],
        "Multiline": NotRequired[bool],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
S3ParquetSourceTypeDef = TypedDict(
    "S3ParquetSourceTypeDef",
    {
        "Name": str,
        "Paths": Sequence[str],
        "CompressionType": NotRequired[ParquetCompressionTypeType],
        "Exclusions": NotRequired[Sequence[str]],
        "GroupSize": NotRequired[str],
        "GroupFiles": NotRequired[str],
        "Recurse": NotRequired[bool],
        "MaxBand": NotRequired[int],
        "MaxFilesInBand": NotRequired[int],
        "AdditionalOptions": NotRequired[S3DirectSourceAdditionalOptionsTypeDef],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
SnowflakeSourceTypeDef = TypedDict(
    "SnowflakeSourceTypeDef",
    {
        "Name": str,
        "Data": SnowflakeNodeDataTypeDef,
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
SparkConnectorSourceTypeDef = TypedDict(
    "SparkConnectorSourceTypeDef",
    {
        "Name": str,
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Mapping[str, str]],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
SparkConnectorTargetTypeDef = TypedDict(
    "SparkConnectorTargetTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "ConnectionName": str,
        "ConnectorName": str,
        "ConnectionType": str,
        "AdditionalOptions": NotRequired[Mapping[str, str]],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
SparkSQLTypeDef = TypedDict(
    "SparkSQLTypeDef",
    {
        "Name": str,
        "Inputs": Sequence[str],
        "SqlQuery": str,
        "SqlAliases": Sequence[SqlAliasTypeDef],
        "OutputSchemas": NotRequired[Sequence[GlueSchemaTypeDef]],
    },
)
GetJobRunResponseTypeDef = TypedDict(
    "GetJobRunResponseTypeDef",
    {
        "JobRun": JobRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetJobRunsResponseTypeDef = TypedDict(
    "GetJobRunsResponseTypeDef",
    {
        "JobRuns": List[JobRunTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
JobNodeDetailsTypeDef = TypedDict(
    "JobNodeDetailsTypeDef",
    {
        "JobRuns": NotRequired[List[JobRunTypeDef]],
    },
)
GetMLTaskRunResponseTypeDef = TypedDict(
    "GetMLTaskRunResponseTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": TaskStatusTypeType,
        "LogGroupName": str,
        "Properties": TaskRunPropertiesTypeDef,
        "ErrorString": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "ExecutionTime": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TaskRunTypeDef = TypedDict(
    "TaskRunTypeDef",
    {
        "TransformId": NotRequired[str],
        "TaskRunId": NotRequired[str],
        "Status": NotRequired[TaskStatusTypeType],
        "LogGroupName": NotRequired[str],
        "Properties": NotRequired[TaskRunPropertiesTypeDef],
        "ErrorString": NotRequired[str],
        "StartedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
        "CompletedOn": NotRequired[datetime],
        "ExecutionTime": NotRequired[int],
    },
)
CreateMLTransformRequestRequestTypeDef = TypedDict(
    "CreateMLTransformRequestRequestTypeDef",
    {
        "Name": str,
        "InputRecordTables": Sequence[GlueTableUnionTypeDef],
        "Parameters": TransformParametersTypeDef,
        "Role": str,
        "Description": NotRequired[str],
        "GlueVersion": NotRequired[str],
        "MaxCapacity": NotRequired[float],
        "WorkerType": NotRequired[WorkerTypeType],
        "NumberOfWorkers": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxRetries": NotRequired[int],
        "Tags": NotRequired[Mapping[str, str]],
        "TransformEncryption": NotRequired[TransformEncryptionTypeDef],
    },
)
QuerySchemaVersionMetadataResponseTypeDef = TypedDict(
    "QuerySchemaVersionMetadataResponseTypeDef",
    {
        "MetadataInfoMap": Dict[str, MetadataInfoTypeDef],
        "SchemaVersionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
AuthenticationConfigurationInputTypeDef = TypedDict(
    "AuthenticationConfigurationInputTypeDef",
    {
        "AuthenticationType": NotRequired[AuthenticationTypeType],
        "SecretArn": NotRequired[str],
        "OAuth2Properties": NotRequired[OAuth2PropertiesInputTypeDef],
    },
)
AuthenticationConfigurationTypeDef = TypedDict(
    "AuthenticationConfigurationTypeDef",
    {
        "AuthenticationType": NotRequired[AuthenticationTypeType],
        "SecretArn": NotRequired[str],
        "OAuth2Properties": NotRequired[OAuth2PropertiesTypeDef],
    },
)
BatchDeletePartitionRequestRequestTypeDef = TypedDict(
    "BatchDeletePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionsToDelete": Sequence[PartitionValueListUnionTypeDef],
        "CatalogId": NotRequired[str],
    },
)
BatchGetPartitionRequestRequestTypeDef = TypedDict(
    "BatchGetPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionsToGet": Sequence[PartitionValueListUnionTypeDef],
        "CatalogId": NotRequired[str],
    },
)
CreateUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "CreateUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionInput": UserDefinedFunctionInputTypeDef,
        "CatalogId": NotRequired[str],
    },
)
UpdateUserDefinedFunctionRequestRequestTypeDef = TypedDict(
    "UpdateUserDefinedFunctionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "FunctionName": str,
        "FunctionInput": UserDefinedFunctionInputTypeDef,
        "CatalogId": NotRequired[str],
    },
)
GetUserDefinedFunctionResponseTypeDef = TypedDict(
    "GetUserDefinedFunctionResponseTypeDef",
    {
        "UserDefinedFunction": UserDefinedFunctionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetUserDefinedFunctionsResponseTypeDef = TypedDict(
    "GetUserDefinedFunctionsResponseTypeDef",
    {
        "UserDefinedFunctions": List[UserDefinedFunctionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListTableOptimizerRunsResponseTypeDef = TypedDict(
    "ListTableOptimizerRunsResponseTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "TableOptimizerRuns": List[TableOptimizerRunTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
TableOptimizerTypeDef = TypedDict(
    "TableOptimizerTypeDef",
    {
        "type": NotRequired[Literal["compaction"]],
        "configuration": NotRequired[TableOptimizerConfigurationTypeDef],
        "lastRun": NotRequired[TableOptimizerRunTypeDef],
    },
)
StatementTypeDef = TypedDict(
    "StatementTypeDef",
    {
        "Id": NotRequired[int],
        "Code": NotRequired[str],
        "State": NotRequired[StatementStateType],
        "Output": NotRequired[StatementOutputTypeDef],
        "Progress": NotRequired[float],
        "StartedOn": NotRequired[int],
        "CompletedOn": NotRequired[int],
    },
)
CreateTriggerRequestRequestTypeDef = TypedDict(
    "CreateTriggerRequestRequestTypeDef",
    {
        "Name": str,
        "Type": TriggerTypeType,
        "Actions": Sequence[ActionUnionTypeDef],
        "WorkflowName": NotRequired[str],
        "Schedule": NotRequired[str],
        "Predicate": NotRequired[PredicateTypeDef],
        "Description": NotRequired[str],
        "StartOnCreation": NotRequired[bool],
        "Tags": NotRequired[Mapping[str, str]],
        "EventBatchingCondition": NotRequired[EventBatchingConditionTypeDef],
    },
)
GetPartitionIndexesResponseTypeDef = TypedDict(
    "GetPartitionIndexesResponseTypeDef",
    {
        "PartitionIndexDescriptorList": List[PartitionIndexDescriptorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ColumnStatisticsDataTypeDef = TypedDict(
    "ColumnStatisticsDataTypeDef",
    {
        "Type": ColumnStatisticsTypeType,
        "BooleanColumnStatisticsData": NotRequired[BooleanColumnStatisticsDataTypeDef],
        "DateColumnStatisticsData": NotRequired[DateColumnStatisticsDataTypeDef],
        "DecimalColumnStatisticsData": NotRequired[DecimalColumnStatisticsDataTypeDef],
        "DoubleColumnStatisticsData": NotRequired[DoubleColumnStatisticsDataTypeDef],
        "LongColumnStatisticsData": NotRequired[LongColumnStatisticsDataTypeDef],
        "StringColumnStatisticsData": NotRequired[StringColumnStatisticsDataTypeDef],
        "BinaryColumnStatisticsData": NotRequired[BinaryColumnStatisticsDataTypeDef],
    },
)
CreateScriptRequestRequestTypeDef = TypedDict(
    "CreateScriptRequestRequestTypeDef",
    {
        "DagNodes": NotRequired[Sequence[CodeGenNodeUnionTypeDef]],
        "DagEdges": NotRequired[Sequence[CodeGenEdgeTypeDef]],
        "Language": NotRequired[LanguageType],
    },
)
BatchGetTriggersResponseTypeDef = TypedDict(
    "BatchGetTriggersResponseTypeDef",
    {
        "Triggers": List[TriggerTypeDef],
        "TriggersNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTriggerResponseTypeDef = TypedDict(
    "GetTriggerResponseTypeDef",
    {
        "Trigger": TriggerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTriggersResponseTypeDef = TypedDict(
    "GetTriggersResponseTypeDef",
    {
        "Triggers": List[TriggerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
TriggerNodeDetailsTypeDef = TypedDict(
    "TriggerNodeDetailsTypeDef",
    {
        "Trigger": NotRequired[TriggerTypeDef],
    },
)
UpdateTriggerResponseTypeDef = TypedDict(
    "UpdateTriggerResponseTypeDef",
    {
        "Trigger": TriggerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTriggerRequestRequestTypeDef = TypedDict(
    "UpdateTriggerRequestRequestTypeDef",
    {
        "Name": str,
        "TriggerUpdate": TriggerUpdateTypeDef,
    },
)
GetMLTransformResponseTypeDef = TypedDict(
    "GetMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "Name": str,
        "Description": str,
        "Status": TransformStatusTypeType,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "InputRecordTables": List[GlueTableOutputTypeDef],
        "Parameters": TransformParametersTypeDef,
        "EvaluationMetrics": EvaluationMetricsTypeDef,
        "LabelCount": int,
        "Schema": List[SchemaColumnTypeDef],
        "Role": str,
        "GlueVersion": str,
        "MaxCapacity": float,
        "WorkerType": WorkerTypeType,
        "NumberOfWorkers": int,
        "Timeout": int,
        "MaxRetries": int,
        "TransformEncryption": TransformEncryptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MLTransformTypeDef = TypedDict(
    "MLTransformTypeDef",
    {
        "TransformId": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Status": NotRequired[TransformStatusTypeType],
        "CreatedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
        "InputRecordTables": NotRequired[List[GlueTableOutputTypeDef]],
        "Parameters": NotRequired[TransformParametersTypeDef],
        "EvaluationMetrics": NotRequired[EvaluationMetricsTypeDef],
        "LabelCount": NotRequired[int],
        "Schema": NotRequired[List[SchemaColumnTypeDef]],
        "Role": NotRequired[str],
        "GlueVersion": NotRequired[str],
        "MaxCapacity": NotRequired[float],
        "WorkerType": NotRequired[WorkerTypeType],
        "NumberOfWorkers": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxRetries": NotRequired[int],
        "TransformEncryption": NotRequired[TransformEncryptionTypeDef],
    },
)
BatchGetCrawlersResponseTypeDef = TypedDict(
    "BatchGetCrawlersResponseTypeDef",
    {
        "Crawlers": List[CrawlerTypeDef],
        "CrawlersNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCrawlerResponseTypeDef = TypedDict(
    "GetCrawlerResponseTypeDef",
    {
        "Crawler": CrawlerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCrawlersResponseTypeDef = TypedDict(
    "GetCrawlersResponseTypeDef",
    {
        "Crawlers": List[CrawlerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetDatabaseResponseTypeDef = TypedDict(
    "GetDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDatabasesResponseTypeDef = TypedDict(
    "GetDatabasesResponseTypeDef",
    {
        "DatabaseList": List[DatabaseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
CreateDatabaseRequestRequestTypeDef = TypedDict(
    "CreateDatabaseRequestRequestTypeDef",
    {
        "DatabaseInput": DatabaseInputTypeDef,
        "CatalogId": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
UpdateDatabaseRequestRequestTypeDef = TypedDict(
    "UpdateDatabaseRequestRequestTypeDef",
    {
        "Name": str,
        "DatabaseInput": DatabaseInputTypeDef,
        "CatalogId": NotRequired[str],
    },
)
DataQualityResultTypeDef = TypedDict(
    "DataQualityResultTypeDef",
    {
        "ResultId": NotRequired[str],
        "Score": NotRequired[float],
        "DataSource": NotRequired[DataSourceOutputTypeDef],
        "RulesetName": NotRequired[str],
        "EvaluationContext": NotRequired[str],
        "StartedOn": NotRequired[datetime],
        "CompletedOn": NotRequired[datetime],
        "JobName": NotRequired[str],
        "JobRunId": NotRequired[str],
        "RulesetEvaluationRunId": NotRequired[str],
        "RuleResults": NotRequired[List[DataQualityRuleResultTypeDef]],
        "AnalyzerResults": NotRequired[List[DataQualityAnalyzerResultTypeDef]],
        "Observations": NotRequired[List[DataQualityObservationTypeDef]],
    },
)
GetDataQualityResultResponseTypeDef = TypedDict(
    "GetDataQualityResultResponseTypeDef",
    {
        "ResultId": str,
        "Score": float,
        "DataSource": DataSourceOutputTypeDef,
        "RulesetName": str,
        "EvaluationContext": str,
        "StartedOn": datetime,
        "CompletedOn": datetime,
        "JobName": str,
        "JobRunId": str,
        "RulesetEvaluationRunId": str,
        "RuleResults": List[DataQualityRuleResultTypeDef],
        "AnalyzerResults": List[DataQualityAnalyzerResultTypeDef],
        "Observations": List[DataQualityObservationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDataQualityResultsResponseTypeDef = TypedDict(
    "ListDataQualityResultsResponseTypeDef",
    {
        "Results": List[DataQualityResultDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListDataQualityRuleRecommendationRunsResponseTypeDef = TypedDict(
    "ListDataQualityRuleRecommendationRunsResponseTypeDef",
    {
        "Runs": List[DataQualityRuleRecommendationRunDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListDataQualityRulesetEvaluationRunsResponseTypeDef = TypedDict(
    "ListDataQualityRulesetEvaluationRunsResponseTypeDef",
    {
        "Runs": List[DataQualityRulesetEvaluationRunDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListDataQualityResultsRequestRequestTypeDef = TypedDict(
    "ListDataQualityResultsRequestRequestTypeDef",
    {
        "Filter": NotRequired[DataQualityResultFilterCriteriaTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListDataQualityRuleRecommendationRunsRequestRequestTypeDef = TypedDict(
    "ListDataQualityRuleRecommendationRunsRequestRequestTypeDef",
    {
        "Filter": NotRequired[DataQualityRuleRecommendationRunFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListDataQualityRulesetEvaluationRunsRequestRequestTypeDef = TypedDict(
    "ListDataQualityRulesetEvaluationRunsRequestRequestTypeDef",
    {
        "Filter": NotRequired[DataQualityRulesetEvaluationRunFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
StartDataQualityRulesetEvaluationRunRequestRequestTypeDef = TypedDict(
    "StartDataQualityRulesetEvaluationRunRequestRequestTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "Role": str,
        "RulesetNames": Sequence[str],
        "NumberOfWorkers": NotRequired[int],
        "Timeout": NotRequired[int],
        "ClientToken": NotRequired[str],
        "AdditionalRunOptions": NotRequired[DataQualityEvaluationRunAdditionalRunOptionsTypeDef],
        "AdditionalDataSources": NotRequired[Mapping[str, DataSourceUnionTypeDef]],
    },
)
ColumnStatisticsOutputTypeDef = TypedDict(
    "ColumnStatisticsOutputTypeDef",
    {
        "ColumnName": str,
        "ColumnType": str,
        "AnalyzedTime": datetime,
        "StatisticsData": ColumnStatisticsDataOutputTypeDef,
    },
)
PartitionTypeDef = TypedDict(
    "PartitionTypeDef",
    {
        "Values": NotRequired[List[str]],
        "DatabaseName": NotRequired[str],
        "TableName": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "LastAccessTime": NotRequired[datetime],
        "StorageDescriptor": NotRequired[StorageDescriptorOutputTypeDef],
        "Parameters": NotRequired[Dict[str, str]],
        "LastAnalyzedTime": NotRequired[datetime],
        "CatalogId": NotRequired[str],
    },
)
TableTypeDef = TypedDict(
    "TableTypeDef",
    {
        "Name": str,
        "DatabaseName": NotRequired[str],
        "Description": NotRequired[str],
        "Owner": NotRequired[str],
        "CreateTime": NotRequired[datetime],
        "UpdateTime": NotRequired[datetime],
        "LastAccessTime": NotRequired[datetime],
        "LastAnalyzedTime": NotRequired[datetime],
        "Retention": NotRequired[int],
        "StorageDescriptor": NotRequired[StorageDescriptorOutputTypeDef],
        "PartitionKeys": NotRequired[List[ColumnOutputTypeDef]],
        "ViewOriginalText": NotRequired[str],
        "ViewExpandedText": NotRequired[str],
        "TableType": NotRequired[str],
        "Parameters": NotRequired[Dict[str, str]],
        "CreatedBy": NotRequired[str],
        "IsRegisteredWithLakeFormation": NotRequired[bool],
        "TargetTable": NotRequired[TableIdentifierTypeDef],
        "CatalogId": NotRequired[str],
        "VersionId": NotRequired[str],
        "FederatedTable": NotRequired[FederatedTableTypeDef],
        "ViewDefinition": NotRequired[ViewDefinitionTypeDef],
        "IsMultiDialectView": NotRequired[bool],
    },
)
PartitionInputTypeDef = TypedDict(
    "PartitionInputTypeDef",
    {
        "Values": NotRequired[Sequence[str]],
        "LastAccessTime": NotRequired[TimestampTypeDef],
        "StorageDescriptor": NotRequired[StorageDescriptorTypeDef],
        "Parameters": NotRequired[Mapping[str, str]],
        "LastAnalyzedTime": NotRequired[TimestampTypeDef],
    },
)
TableInputTypeDef = TypedDict(
    "TableInputTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "Owner": NotRequired[str],
        "LastAccessTime": NotRequired[TimestampTypeDef],
        "LastAnalyzedTime": NotRequired[TimestampTypeDef],
        "Retention": NotRequired[int],
        "StorageDescriptor": NotRequired[StorageDescriptorTypeDef],
        "PartitionKeys": NotRequired[Sequence[ColumnTypeDef]],
        "ViewOriginalText": NotRequired[str],
        "ViewExpandedText": NotRequired[str],
        "TableType": NotRequired[str],
        "Parameters": NotRequired[Mapping[str, str]],
        "TargetTable": NotRequired[TableIdentifierTypeDef],
        "ViewDefinition": NotRequired[ViewDefinitionInputTypeDef],
    },
)
GetSecurityConfigurationResponseTypeDef = TypedDict(
    "GetSecurityConfigurationResponseTypeDef",
    {
        "SecurityConfiguration": SecurityConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSecurityConfigurationsResponseTypeDef = TypedDict(
    "GetSecurityConfigurationsResponseTypeDef",
    {
        "SecurityConfigurations": List[SecurityConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
CodeGenConfigurationNodeExtraOutputTypeDef = TypedDict(
    "CodeGenConfigurationNodeExtraOutputTypeDef",
    {
        "AthenaConnectorSource": NotRequired[AthenaConnectorSourceExtraOutputTypeDef],
        "JDBCConnectorSource": NotRequired[JDBCConnectorSourceExtraOutputTypeDef],
        "SparkConnectorSource": NotRequired[SparkConnectorSourceExtraOutputTypeDef],
        "CatalogSource": NotRequired[CatalogSourceTypeDef],
        "RedshiftSource": NotRequired[RedshiftSourceTypeDef],
        "S3CatalogSource": NotRequired[S3CatalogSourceTypeDef],
        "S3CsvSource": NotRequired[S3CsvSourceExtraOutputTypeDef],
        "S3JsonSource": NotRequired[S3JsonSourceExtraOutputTypeDef],
        "S3ParquetSource": NotRequired[S3ParquetSourceExtraOutputTypeDef],
        "RelationalCatalogSource": NotRequired[RelationalCatalogSourceTypeDef],
        "DynamoDBCatalogSource": NotRequired[DynamoDBCatalogSourceTypeDef],
        "JDBCConnectorTarget": NotRequired[JDBCConnectorTargetExtraOutputTypeDef],
        "SparkConnectorTarget": NotRequired[SparkConnectorTargetExtraOutputTypeDef],
        "CatalogTarget": NotRequired[BasicCatalogTargetExtraOutputTypeDef],
        "RedshiftTarget": NotRequired[RedshiftTargetExtraOutputTypeDef],
        "S3CatalogTarget": NotRequired[S3CatalogTargetExtraOutputTypeDef],
        "S3GlueParquetTarget": NotRequired[S3GlueParquetTargetExtraOutputTypeDef],
        "S3DirectTarget": NotRequired[S3DirectTargetExtraOutputTypeDef],
        "ApplyMapping": NotRequired[ApplyMappingExtraOutputTypeDef],
        "SelectFields": NotRequired[SelectFieldsExtraOutputTypeDef],
        "DropFields": NotRequired[DropFieldsExtraOutputTypeDef],
        "RenameField": NotRequired[RenameFieldExtraOutputTypeDef],
        "Spigot": NotRequired[SpigotExtraOutputTypeDef],
        "Join": NotRequired[JoinExtraOutputTypeDef],
        "SplitFields": NotRequired[SplitFieldsExtraOutputTypeDef],
        "SelectFromCollection": NotRequired[SelectFromCollectionExtraOutputTypeDef],
        "FillMissingValues": NotRequired[FillMissingValuesExtraOutputTypeDef],
        "Filter": NotRequired[FilterExtraOutputTypeDef],
        "CustomCode": NotRequired[CustomCodeExtraOutputTypeDef],
        "SparkSQL": NotRequired[SparkSQLExtraOutputTypeDef],
        "DirectKinesisSource": NotRequired[DirectKinesisSourceExtraOutputTypeDef],
        "DirectKafkaSource": NotRequired[DirectKafkaSourceExtraOutputTypeDef],
        "CatalogKinesisSource": NotRequired[CatalogKinesisSourceExtraOutputTypeDef],
        "CatalogKafkaSource": NotRequired[CatalogKafkaSourceExtraOutputTypeDef],
        "DropNullFields": NotRequired[DropNullFieldsExtraOutputTypeDef],
        "Merge": NotRequired[MergeExtraOutputTypeDef],
        "Union": NotRequired[UnionExtraOutputTypeDef],
        "PIIDetection": NotRequired[PIIDetectionExtraOutputTypeDef],
        "Aggregate": NotRequired[AggregateExtraOutputTypeDef],
        "DropDuplicates": NotRequired[DropDuplicatesExtraOutputTypeDef],
        "GovernedCatalogTarget": NotRequired[GovernedCatalogTargetExtraOutputTypeDef],
        "GovernedCatalogSource": NotRequired[GovernedCatalogSourceTypeDef],
        "MicrosoftSQLServerCatalogSource": NotRequired[MicrosoftSQLServerCatalogSourceTypeDef],
        "MySQLCatalogSource": NotRequired[MySQLCatalogSourceTypeDef],
        "OracleSQLCatalogSource": NotRequired[OracleSQLCatalogSourceTypeDef],
        "PostgreSQLCatalogSource": NotRequired[PostgreSQLCatalogSourceTypeDef],
        "MicrosoftSQLServerCatalogTarget": NotRequired[
            MicrosoftSQLServerCatalogTargetExtraOutputTypeDef
        ],
        "MySQLCatalogTarget": NotRequired[MySQLCatalogTargetExtraOutputTypeDef],
        "OracleSQLCatalogTarget": NotRequired[OracleSQLCatalogTargetExtraOutputTypeDef],
        "PostgreSQLCatalogTarget": NotRequired[PostgreSQLCatalogTargetExtraOutputTypeDef],
        "DynamicTransform": NotRequired[DynamicTransformExtraOutputTypeDef],
        "EvaluateDataQuality": NotRequired[EvaluateDataQualityExtraOutputTypeDef],
        "S3CatalogHudiSource": NotRequired[S3CatalogHudiSourceExtraOutputTypeDef],
        "CatalogHudiSource": NotRequired[CatalogHudiSourceExtraOutputTypeDef],
        "S3HudiSource": NotRequired[S3HudiSourceExtraOutputTypeDef],
        "S3HudiCatalogTarget": NotRequired[S3HudiCatalogTargetExtraOutputTypeDef],
        "S3HudiDirectTarget": NotRequired[S3HudiDirectTargetExtraOutputTypeDef],
        "DirectJDBCSource": NotRequired[DirectJDBCSourceTypeDef],
        "S3CatalogDeltaSource": NotRequired[S3CatalogDeltaSourceExtraOutputTypeDef],
        "CatalogDeltaSource": NotRequired[CatalogDeltaSourceExtraOutputTypeDef],
        "S3DeltaSource": NotRequired[S3DeltaSourceExtraOutputTypeDef],
        "S3DeltaCatalogTarget": NotRequired[S3DeltaCatalogTargetExtraOutputTypeDef],
        "S3DeltaDirectTarget": NotRequired[S3DeltaDirectTargetExtraOutputTypeDef],
        "AmazonRedshiftSource": NotRequired[AmazonRedshiftSourceExtraOutputTypeDef],
        "AmazonRedshiftTarget": NotRequired[AmazonRedshiftTargetExtraOutputTypeDef],
        "EvaluateDataQualityMultiFrame": NotRequired[
            EvaluateDataQualityMultiFrameExtraOutputTypeDef
        ],
        "Recipe": NotRequired[RecipeExtraOutputTypeDef],
        "SnowflakeSource": NotRequired[SnowflakeSourceExtraOutputTypeDef],
        "SnowflakeTarget": NotRequired[SnowflakeTargetExtraOutputTypeDef],
        "ConnectorDataSource": NotRequired[ConnectorDataSourceExtraOutputTypeDef],
        "ConnectorDataTarget": NotRequired[ConnectorDataTargetExtraOutputTypeDef],
    },
)
CodeGenConfigurationNodeOutputTypeDef = TypedDict(
    "CodeGenConfigurationNodeOutputTypeDef",
    {
        "AthenaConnectorSource": NotRequired[AthenaConnectorSourceOutputTypeDef],
        "JDBCConnectorSource": NotRequired[JDBCConnectorSourceOutputTypeDef],
        "SparkConnectorSource": NotRequired[SparkConnectorSourceOutputTypeDef],
        "CatalogSource": NotRequired[CatalogSourceTypeDef],
        "RedshiftSource": NotRequired[RedshiftSourceTypeDef],
        "S3CatalogSource": NotRequired[S3CatalogSourceTypeDef],
        "S3CsvSource": NotRequired[S3CsvSourceOutputTypeDef],
        "S3JsonSource": NotRequired[S3JsonSourceOutputTypeDef],
        "S3ParquetSource": NotRequired[S3ParquetSourceOutputTypeDef],
        "RelationalCatalogSource": NotRequired[RelationalCatalogSourceTypeDef],
        "DynamoDBCatalogSource": NotRequired[DynamoDBCatalogSourceTypeDef],
        "JDBCConnectorTarget": NotRequired[JDBCConnectorTargetOutputTypeDef],
        "SparkConnectorTarget": NotRequired[SparkConnectorTargetOutputTypeDef],
        "CatalogTarget": NotRequired[BasicCatalogTargetOutputTypeDef],
        "RedshiftTarget": NotRequired[RedshiftTargetOutputTypeDef],
        "S3CatalogTarget": NotRequired[S3CatalogTargetOutputTypeDef],
        "S3GlueParquetTarget": NotRequired[S3GlueParquetTargetOutputTypeDef],
        "S3DirectTarget": NotRequired[S3DirectTargetOutputTypeDef],
        "ApplyMapping": NotRequired[ApplyMappingOutputTypeDef],
        "SelectFields": NotRequired[SelectFieldsOutputTypeDef],
        "DropFields": NotRequired[DropFieldsOutputTypeDef],
        "RenameField": NotRequired[RenameFieldOutputTypeDef],
        "Spigot": NotRequired[SpigotOutputTypeDef],
        "Join": NotRequired[JoinOutputTypeDef],
        "SplitFields": NotRequired[SplitFieldsOutputTypeDef],
        "SelectFromCollection": NotRequired[SelectFromCollectionOutputTypeDef],
        "FillMissingValues": NotRequired[FillMissingValuesOutputTypeDef],
        "Filter": NotRequired[FilterOutputTypeDef],
        "CustomCode": NotRequired[CustomCodeOutputTypeDef],
        "SparkSQL": NotRequired[SparkSQLOutputTypeDef],
        "DirectKinesisSource": NotRequired[DirectKinesisSourceOutputTypeDef],
        "DirectKafkaSource": NotRequired[DirectKafkaSourceOutputTypeDef],
        "CatalogKinesisSource": NotRequired[CatalogKinesisSourceOutputTypeDef],
        "CatalogKafkaSource": NotRequired[CatalogKafkaSourceOutputTypeDef],
        "DropNullFields": NotRequired[DropNullFieldsOutputTypeDef],
        "Merge": NotRequired[MergeOutputTypeDef],
        "Union": NotRequired[UnionOutputTypeDef],
        "PIIDetection": NotRequired[PIIDetectionOutputTypeDef],
        "Aggregate": NotRequired[AggregateOutputTypeDef],
        "DropDuplicates": NotRequired[DropDuplicatesOutputTypeDef],
        "GovernedCatalogTarget": NotRequired[GovernedCatalogTargetOutputTypeDef],
        "GovernedCatalogSource": NotRequired[GovernedCatalogSourceTypeDef],
        "MicrosoftSQLServerCatalogSource": NotRequired[MicrosoftSQLServerCatalogSourceTypeDef],
        "MySQLCatalogSource": NotRequired[MySQLCatalogSourceTypeDef],
        "OracleSQLCatalogSource": NotRequired[OracleSQLCatalogSourceTypeDef],
        "PostgreSQLCatalogSource": NotRequired[PostgreSQLCatalogSourceTypeDef],
        "MicrosoftSQLServerCatalogTarget": NotRequired[
            MicrosoftSQLServerCatalogTargetOutputTypeDef
        ],
        "MySQLCatalogTarget": NotRequired[MySQLCatalogTargetOutputTypeDef],
        "OracleSQLCatalogTarget": NotRequired[OracleSQLCatalogTargetOutputTypeDef],
        "PostgreSQLCatalogTarget": NotRequired[PostgreSQLCatalogTargetOutputTypeDef],
        "DynamicTransform": NotRequired[DynamicTransformOutputTypeDef],
        "EvaluateDataQuality": NotRequired[EvaluateDataQualityOutputTypeDef],
        "S3CatalogHudiSource": NotRequired[S3CatalogHudiSourceOutputTypeDef],
        "CatalogHudiSource": NotRequired[CatalogHudiSourceOutputTypeDef],
        "S3HudiSource": NotRequired[S3HudiSourceOutputTypeDef],
        "S3HudiCatalogTarget": NotRequired[S3HudiCatalogTargetOutputTypeDef],
        "S3HudiDirectTarget": NotRequired[S3HudiDirectTargetOutputTypeDef],
        "DirectJDBCSource": NotRequired[DirectJDBCSourceTypeDef],
        "S3CatalogDeltaSource": NotRequired[S3CatalogDeltaSourceOutputTypeDef],
        "CatalogDeltaSource": NotRequired[CatalogDeltaSourceOutputTypeDef],
        "S3DeltaSource": NotRequired[S3DeltaSourceOutputTypeDef],
        "S3DeltaCatalogTarget": NotRequired[S3DeltaCatalogTargetOutputTypeDef],
        "S3DeltaDirectTarget": NotRequired[S3DeltaDirectTargetOutputTypeDef],
        "AmazonRedshiftSource": NotRequired[AmazonRedshiftSourceOutputTypeDef],
        "AmazonRedshiftTarget": NotRequired[AmazonRedshiftTargetOutputTypeDef],
        "EvaluateDataQualityMultiFrame": NotRequired[EvaluateDataQualityMultiFrameOutputTypeDef],
        "Recipe": NotRequired[RecipeOutputTypeDef],
        "SnowflakeSource": NotRequired[SnowflakeSourceOutputTypeDef],
        "SnowflakeTarget": NotRequired[SnowflakeTargetOutputTypeDef],
        "ConnectorDataSource": NotRequired[ConnectorDataSourceOutputTypeDef],
        "ConnectorDataTarget": NotRequired[ConnectorDataTargetOutputTypeDef],
    },
)
CodeGenConfigurationNodeTypeDef = TypedDict(
    "CodeGenConfigurationNodeTypeDef",
    {
        "AthenaConnectorSource": NotRequired[AthenaConnectorSourceTypeDef],
        "JDBCConnectorSource": NotRequired[JDBCConnectorSourceTypeDef],
        "SparkConnectorSource": NotRequired[SparkConnectorSourceTypeDef],
        "CatalogSource": NotRequired[CatalogSourceTypeDef],
        "RedshiftSource": NotRequired[RedshiftSourceTypeDef],
        "S3CatalogSource": NotRequired[S3CatalogSourceTypeDef],
        "S3CsvSource": NotRequired[S3CsvSourceTypeDef],
        "S3JsonSource": NotRequired[S3JsonSourceTypeDef],
        "S3ParquetSource": NotRequired[S3ParquetSourceTypeDef],
        "RelationalCatalogSource": NotRequired[RelationalCatalogSourceTypeDef],
        "DynamoDBCatalogSource": NotRequired[DynamoDBCatalogSourceTypeDef],
        "JDBCConnectorTarget": NotRequired[JDBCConnectorTargetTypeDef],
        "SparkConnectorTarget": NotRequired[SparkConnectorTargetTypeDef],
        "CatalogTarget": NotRequired[BasicCatalogTargetTypeDef],
        "RedshiftTarget": NotRequired[RedshiftTargetTypeDef],
        "S3CatalogTarget": NotRequired[S3CatalogTargetTypeDef],
        "S3GlueParquetTarget": NotRequired[S3GlueParquetTargetTypeDef],
        "S3DirectTarget": NotRequired[S3DirectTargetTypeDef],
        "ApplyMapping": NotRequired[ApplyMappingTypeDef],
        "SelectFields": NotRequired[SelectFieldsTypeDef],
        "DropFields": NotRequired[DropFieldsTypeDef],
        "RenameField": NotRequired[RenameFieldTypeDef],
        "Spigot": NotRequired[SpigotTypeDef],
        "Join": NotRequired[JoinTypeDef],
        "SplitFields": NotRequired[SplitFieldsTypeDef],
        "SelectFromCollection": NotRequired[SelectFromCollectionTypeDef],
        "FillMissingValues": NotRequired[FillMissingValuesTypeDef],
        "Filter": NotRequired[FilterTypeDef],
        "CustomCode": NotRequired[CustomCodeTypeDef],
        "SparkSQL": NotRequired[SparkSQLTypeDef],
        "DirectKinesisSource": NotRequired[DirectKinesisSourceTypeDef],
        "DirectKafkaSource": NotRequired[DirectKafkaSourceTypeDef],
        "CatalogKinesisSource": NotRequired[CatalogKinesisSourceTypeDef],
        "CatalogKafkaSource": NotRequired[CatalogKafkaSourceTypeDef],
        "DropNullFields": NotRequired[DropNullFieldsTypeDef],
        "Merge": NotRequired[MergeTypeDef],
        "Union": NotRequired[UnionTypeDef],
        "PIIDetection": NotRequired[PIIDetectionTypeDef],
        "Aggregate": NotRequired[AggregateTypeDef],
        "DropDuplicates": NotRequired[DropDuplicatesTypeDef],
        "GovernedCatalogTarget": NotRequired[GovernedCatalogTargetTypeDef],
        "GovernedCatalogSource": NotRequired[GovernedCatalogSourceTypeDef],
        "MicrosoftSQLServerCatalogSource": NotRequired[MicrosoftSQLServerCatalogSourceTypeDef],
        "MySQLCatalogSource": NotRequired[MySQLCatalogSourceTypeDef],
        "OracleSQLCatalogSource": NotRequired[OracleSQLCatalogSourceTypeDef],
        "PostgreSQLCatalogSource": NotRequired[PostgreSQLCatalogSourceTypeDef],
        "MicrosoftSQLServerCatalogTarget": NotRequired[MicrosoftSQLServerCatalogTargetTypeDef],
        "MySQLCatalogTarget": NotRequired[MySQLCatalogTargetTypeDef],
        "OracleSQLCatalogTarget": NotRequired[OracleSQLCatalogTargetTypeDef],
        "PostgreSQLCatalogTarget": NotRequired[PostgreSQLCatalogTargetTypeDef],
        "DynamicTransform": NotRequired[DynamicTransformTypeDef],
        "EvaluateDataQuality": NotRequired[EvaluateDataQualityTypeDef],
        "S3CatalogHudiSource": NotRequired[S3CatalogHudiSourceTypeDef],
        "CatalogHudiSource": NotRequired[CatalogHudiSourceTypeDef],
        "S3HudiSource": NotRequired[S3HudiSourceTypeDef],
        "S3HudiCatalogTarget": NotRequired[S3HudiCatalogTargetTypeDef],
        "S3HudiDirectTarget": NotRequired[S3HudiDirectTargetTypeDef],
        "DirectJDBCSource": NotRequired[DirectJDBCSourceTypeDef],
        "S3CatalogDeltaSource": NotRequired[S3CatalogDeltaSourceTypeDef],
        "CatalogDeltaSource": NotRequired[CatalogDeltaSourceTypeDef],
        "S3DeltaSource": NotRequired[S3DeltaSourceTypeDef],
        "S3DeltaCatalogTarget": NotRequired[S3DeltaCatalogTargetTypeDef],
        "S3DeltaDirectTarget": NotRequired[S3DeltaDirectTargetTypeDef],
        "AmazonRedshiftSource": NotRequired[AmazonRedshiftSourceTypeDef],
        "AmazonRedshiftTarget": NotRequired[AmazonRedshiftTargetTypeDef],
        "EvaluateDataQualityMultiFrame": NotRequired[EvaluateDataQualityMultiFrameTypeDef],
        "Recipe": NotRequired[RecipeTypeDef],
        "SnowflakeSource": NotRequired[SnowflakeSourceTypeDef],
        "SnowflakeTarget": NotRequired[SnowflakeTargetTypeDef],
        "ConnectorDataSource": NotRequired[ConnectorDataSourceTypeDef],
        "ConnectorDataTarget": NotRequired[ConnectorDataTargetTypeDef],
    },
)
GetMLTaskRunsResponseTypeDef = TypedDict(
    "GetMLTaskRunsResponseTypeDef",
    {
        "TaskRuns": List[TaskRunTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ConnectionInputTypeDef = TypedDict(
    "ConnectionInputTypeDef",
    {
        "Name": str,
        "ConnectionType": ConnectionTypeType,
        "ConnectionProperties": Mapping[ConnectionPropertyKeyType, str],
        "Description": NotRequired[str],
        "MatchCriteria": NotRequired[Sequence[str]],
        "PhysicalConnectionRequirements": NotRequired[PhysicalConnectionRequirementsTypeDef],
        "AuthenticationConfiguration": NotRequired[AuthenticationConfigurationInputTypeDef],
        "ValidateCredentials": NotRequired[bool],
    },
)
ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "ConnectionType": NotRequired[ConnectionTypeType],
        "MatchCriteria": NotRequired[List[str]],
        "ConnectionProperties": NotRequired[Dict[ConnectionPropertyKeyType, str]],
        "PhysicalConnectionRequirements": NotRequired[PhysicalConnectionRequirementsOutputTypeDef],
        "CreationTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "LastUpdatedBy": NotRequired[str],
        "Status": NotRequired[ConnectionStatusType],
        "StatusReason": NotRequired[str],
        "LastConnectionValidationTime": NotRequired[datetime],
        "AuthenticationConfiguration": NotRequired[AuthenticationConfigurationTypeDef],
    },
)
BatchTableOptimizerTypeDef = TypedDict(
    "BatchTableOptimizerTypeDef",
    {
        "catalogId": NotRequired[str],
        "databaseName": NotRequired[str],
        "tableName": NotRequired[str],
        "tableOptimizer": NotRequired[TableOptimizerTypeDef],
    },
)
GetTableOptimizerResponseTypeDef = TypedDict(
    "GetTableOptimizerResponseTypeDef",
    {
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "TableOptimizer": TableOptimizerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStatementResponseTypeDef = TypedDict(
    "GetStatementResponseTypeDef",
    {
        "Statement": StatementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStatementsResponseTypeDef = TypedDict(
    "ListStatementsResponseTypeDef",
    {
        "Statements": List[StatementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ColumnStatisticsTypeDef = TypedDict(
    "ColumnStatisticsTypeDef",
    {
        "ColumnName": str,
        "ColumnType": str,
        "AnalyzedTime": TimestampTypeDef,
        "StatisticsData": ColumnStatisticsDataTypeDef,
    },
)
NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "Type": NotRequired[NodeTypeType],
        "Name": NotRequired[str],
        "UniqueId": NotRequired[str],
        "TriggerDetails": NotRequired[TriggerNodeDetailsTypeDef],
        "JobDetails": NotRequired[JobNodeDetailsTypeDef],
        "CrawlerDetails": NotRequired[CrawlerNodeDetailsTypeDef],
    },
)
GetMLTransformsResponseTypeDef = TypedDict(
    "GetMLTransformsResponseTypeDef",
    {
        "Transforms": List[MLTransformTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
BatchGetDataQualityResultResponseTypeDef = TypedDict(
    "BatchGetDataQualityResultResponseTypeDef",
    {
        "Results": List[DataQualityResultTypeDef],
        "ResultsNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ColumnStatisticsErrorTypeDef = TypedDict(
    "ColumnStatisticsErrorTypeDef",
    {
        "ColumnStatistics": NotRequired[ColumnStatisticsOutputTypeDef],
        "Error": NotRequired[ErrorDetailTypeDef],
    },
)
GetColumnStatisticsForPartitionResponseTypeDef = TypedDict(
    "GetColumnStatisticsForPartitionResponseTypeDef",
    {
        "ColumnStatisticsList": List[ColumnStatisticsOutputTypeDef],
        "Errors": List[ColumnErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetColumnStatisticsForTableResponseTypeDef = TypedDict(
    "GetColumnStatisticsForTableResponseTypeDef",
    {
        "ColumnStatisticsList": List[ColumnStatisticsOutputTypeDef],
        "Errors": List[ColumnErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchGetPartitionResponseTypeDef = TypedDict(
    "BatchGetPartitionResponseTypeDef",
    {
        "Partitions": List[PartitionTypeDef],
        "UnprocessedKeys": List[PartitionValueListOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPartitionResponseTypeDef = TypedDict(
    "GetPartitionResponseTypeDef",
    {
        "Partition": PartitionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPartitionsResponseTypeDef = TypedDict(
    "GetPartitionsResponseTypeDef",
    {
        "Partitions": List[PartitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetUnfilteredPartitionMetadataResponseTypeDef = TypedDict(
    "GetUnfilteredPartitionMetadataResponseTypeDef",
    {
        "Partition": PartitionTypeDef,
        "AuthorizedColumns": List[str],
        "IsRegisteredWithLakeFormation": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UnfilteredPartitionTypeDef = TypedDict(
    "UnfilteredPartitionTypeDef",
    {
        "Partition": NotRequired[PartitionTypeDef],
        "AuthorizedColumns": NotRequired[List[str]],
        "IsRegisteredWithLakeFormation": NotRequired[bool],
    },
)
GetTableResponseTypeDef = TypedDict(
    "GetTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTablesResponseTypeDef = TypedDict(
    "GetTablesResponseTypeDef",
    {
        "TableList": List[TableTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetUnfilteredTableMetadataResponseTypeDef = TypedDict(
    "GetUnfilteredTableMetadataResponseTypeDef",
    {
        "Table": TableTypeDef,
        "AuthorizedColumns": List[str],
        "IsRegisteredWithLakeFormation": bool,
        "CellFilters": List[ColumnRowFilterTypeDef],
        "QueryAuthorizationId": str,
        "IsMultiDialectView": bool,
        "ResourceArn": str,
        "IsProtected": bool,
        "Permissions": List[PermissionType],
        "RowFilter": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchTablesResponseTypeDef = TypedDict(
    "SearchTablesResponseTypeDef",
    {
        "TableList": List[TableTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
TableVersionTypeDef = TypedDict(
    "TableVersionTypeDef",
    {
        "Table": NotRequired[TableTypeDef],
        "VersionId": NotRequired[str],
    },
)
BatchCreatePartitionRequestRequestTypeDef = TypedDict(
    "BatchCreatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionInputList": Sequence[PartitionInputTypeDef],
        "CatalogId": NotRequired[str],
    },
)
BatchUpdatePartitionRequestEntryTypeDef = TypedDict(
    "BatchUpdatePartitionRequestEntryTypeDef",
    {
        "PartitionValueList": Sequence[str],
        "PartitionInput": PartitionInputTypeDef,
    },
)
CreatePartitionRequestRequestTypeDef = TypedDict(
    "CreatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionInput": PartitionInputTypeDef,
        "CatalogId": NotRequired[str],
    },
)
UpdatePartitionRequestRequestTypeDef = TypedDict(
    "UpdatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValueList": Sequence[str],
        "PartitionInput": PartitionInputTypeDef,
        "CatalogId": NotRequired[str],
    },
)
CreateTableRequestRequestTypeDef = TypedDict(
    "CreateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableInput": TableInputTypeDef,
        "CatalogId": NotRequired[str],
        "PartitionIndexes": NotRequired[Sequence[PartitionIndexTypeDef]],
        "TransactionId": NotRequired[str],
        "OpenTableFormatInput": NotRequired[OpenTableFormatInputTypeDef],
    },
)
UpdateTableRequestRequestTypeDef = TypedDict(
    "UpdateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableInput": TableInputTypeDef,
        "CatalogId": NotRequired[str],
        "SkipArchive": NotRequired[bool],
        "TransactionId": NotRequired[str],
        "VersionId": NotRequired[str],
        "ViewUpdateAction": NotRequired[ViewUpdateActionType],
        "Force": NotRequired[bool],
    },
)
JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "Name": NotRequired[str],
        "JobMode": NotRequired[JobModeType],
        "Description": NotRequired[str],
        "LogUri": NotRequired[str],
        "Role": NotRequired[str],
        "CreatedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
        "ExecutionProperty": NotRequired[ExecutionPropertyTypeDef],
        "Command": NotRequired[JobCommandTypeDef],
        "DefaultArguments": NotRequired[Dict[str, str]],
        "NonOverridableArguments": NotRequired[Dict[str, str]],
        "Connections": NotRequired[ConnectionsListOutputTypeDef],
        "MaxRetries": NotRequired[int],
        "AllocatedCapacity": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxCapacity": NotRequired[float],
        "WorkerType": NotRequired[WorkerTypeType],
        "NumberOfWorkers": NotRequired[int],
        "SecurityConfiguration": NotRequired[str],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "GlueVersion": NotRequired[str],
        "CodeGenConfigurationNodes": NotRequired[Dict[str, CodeGenConfigurationNodeOutputTypeDef]],
        "ExecutionClass": NotRequired[ExecutionClassType],
        "SourceControlDetails": NotRequired[SourceControlDetailsTypeDef],
        "MaintenanceWindow": NotRequired[str],
        "ProfileName": NotRequired[str],
    },
)
CodeGenConfigurationNodeUnionTypeDef = Union[
    CodeGenConfigurationNodeTypeDef, CodeGenConfigurationNodeExtraOutputTypeDef
]
JobUpdateTypeDef = TypedDict(
    "JobUpdateTypeDef",
    {
        "JobMode": NotRequired[JobModeType],
        "Description": NotRequired[str],
        "LogUri": NotRequired[str],
        "Role": NotRequired[str],
        "ExecutionProperty": NotRequired[ExecutionPropertyTypeDef],
        "Command": NotRequired[JobCommandTypeDef],
        "DefaultArguments": NotRequired[Mapping[str, str]],
        "NonOverridableArguments": NotRequired[Mapping[str, str]],
        "Connections": NotRequired[ConnectionsListTypeDef],
        "MaxRetries": NotRequired[int],
        "AllocatedCapacity": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxCapacity": NotRequired[float],
        "WorkerType": NotRequired[WorkerTypeType],
        "NumberOfWorkers": NotRequired[int],
        "SecurityConfiguration": NotRequired[str],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "GlueVersion": NotRequired[str],
        "CodeGenConfigurationNodes": NotRequired[Mapping[str, CodeGenConfigurationNodeTypeDef]],
        "ExecutionClass": NotRequired[ExecutionClassType],
        "SourceControlDetails": NotRequired[SourceControlDetailsTypeDef],
        "MaintenanceWindow": NotRequired[str],
    },
)
CreateConnectionRequestRequestTypeDef = TypedDict(
    "CreateConnectionRequestRequestTypeDef",
    {
        "ConnectionInput": ConnectionInputTypeDef,
        "CatalogId": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
UpdateConnectionRequestRequestTypeDef = TypedDict(
    "UpdateConnectionRequestRequestTypeDef",
    {
        "Name": str,
        "ConnectionInput": ConnectionInputTypeDef,
        "CatalogId": NotRequired[str],
    },
)
GetConnectionResponseTypeDef = TypedDict(
    "GetConnectionResponseTypeDef",
    {
        "Connection": ConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetConnectionsResponseTypeDef = TypedDict(
    "GetConnectionsResponseTypeDef",
    {
        "ConnectionList": List[ConnectionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
BatchGetTableOptimizerResponseTypeDef = TypedDict(
    "BatchGetTableOptimizerResponseTypeDef",
    {
        "TableOptimizers": List[BatchTableOptimizerTypeDef],
        "Failures": List[BatchGetTableOptimizerErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ColumnStatisticsUnionTypeDef = Union[ColumnStatisticsTypeDef, ColumnStatisticsOutputTypeDef]
WorkflowGraphTypeDef = TypedDict(
    "WorkflowGraphTypeDef",
    {
        "Nodes": NotRequired[List[NodeTypeDef]],
        "Edges": NotRequired[List[EdgeTypeDef]],
    },
)
UpdateColumnStatisticsForPartitionResponseTypeDef = TypedDict(
    "UpdateColumnStatisticsForPartitionResponseTypeDef",
    {
        "Errors": List[ColumnStatisticsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateColumnStatisticsForTableResponseTypeDef = TypedDict(
    "UpdateColumnStatisticsForTableResponseTypeDef",
    {
        "Errors": List[ColumnStatisticsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetUnfilteredPartitionsMetadataResponseTypeDef = TypedDict(
    "GetUnfilteredPartitionsMetadataResponseTypeDef",
    {
        "UnfilteredPartitions": List[UnfilteredPartitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetTableVersionResponseTypeDef = TypedDict(
    "GetTableVersionResponseTypeDef",
    {
        "TableVersion": TableVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTableVersionsResponseTypeDef = TypedDict(
    "GetTableVersionsResponseTypeDef",
    {
        "TableVersions": List[TableVersionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
BatchUpdatePartitionRequestRequestTypeDef = TypedDict(
    "BatchUpdatePartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "Entries": Sequence[BatchUpdatePartitionRequestEntryTypeDef],
        "CatalogId": NotRequired[str],
    },
)
BatchGetJobsResponseTypeDef = TypedDict(
    "BatchGetJobsResponseTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "JobsNotFound": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "Job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetJobsResponseTypeDef = TypedDict(
    "GetJobsResponseTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
CreateJobRequestRequestTypeDef = TypedDict(
    "CreateJobRequestRequestTypeDef",
    {
        "Name": str,
        "Role": str,
        "Command": JobCommandTypeDef,
        "JobMode": NotRequired[JobModeType],
        "Description": NotRequired[str],
        "LogUri": NotRequired[str],
        "ExecutionProperty": NotRequired[ExecutionPropertyTypeDef],
        "DefaultArguments": NotRequired[Mapping[str, str]],
        "NonOverridableArguments": NotRequired[Mapping[str, str]],
        "Connections": NotRequired[ConnectionsListTypeDef],
        "MaxRetries": NotRequired[int],
        "AllocatedCapacity": NotRequired[int],
        "Timeout": NotRequired[int],
        "MaxCapacity": NotRequired[float],
        "SecurityConfiguration": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
        "NotificationProperty": NotRequired[NotificationPropertyTypeDef],
        "GlueVersion": NotRequired[str],
        "NumberOfWorkers": NotRequired[int],
        "WorkerType": NotRequired[WorkerTypeType],
        "CodeGenConfigurationNodes": NotRequired[
            Mapping[str, CodeGenConfigurationNodeUnionTypeDef]
        ],
        "ExecutionClass": NotRequired[ExecutionClassType],
        "SourceControlDetails": NotRequired[SourceControlDetailsTypeDef],
        "MaintenanceWindow": NotRequired[str],
    },
)
UpdateJobRequestRequestTypeDef = TypedDict(
    "UpdateJobRequestRequestTypeDef",
    {
        "JobName": str,
        "JobUpdate": JobUpdateTypeDef,
    },
)
UpdateColumnStatisticsForPartitionRequestRequestTypeDef = TypedDict(
    "UpdateColumnStatisticsForPartitionRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "PartitionValues": Sequence[str],
        "ColumnStatisticsList": Sequence[ColumnStatisticsUnionTypeDef],
        "CatalogId": NotRequired[str],
    },
)
UpdateColumnStatisticsForTableRequestRequestTypeDef = TypedDict(
    "UpdateColumnStatisticsForTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "ColumnStatisticsList": Sequence[ColumnStatisticsUnionTypeDef],
        "CatalogId": NotRequired[str],
    },
)
WorkflowRunTypeDef = TypedDict(
    "WorkflowRunTypeDef",
    {
        "Name": NotRequired[str],
        "WorkflowRunId": NotRequired[str],
        "PreviousRunId": NotRequired[str],
        "WorkflowRunProperties": NotRequired[Dict[str, str]],
        "StartedOn": NotRequired[datetime],
        "CompletedOn": NotRequired[datetime],
        "Status": NotRequired[WorkflowRunStatusType],
        "ErrorMessage": NotRequired[str],
        "Statistics": NotRequired[WorkflowRunStatisticsTypeDef],
        "Graph": NotRequired[WorkflowGraphTypeDef],
        "StartingEventBatchCondition": NotRequired[StartingEventBatchConditionTypeDef],
    },
)
GetWorkflowRunResponseTypeDef = TypedDict(
    "GetWorkflowRunResponseTypeDef",
    {
        "Run": WorkflowRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetWorkflowRunsResponseTypeDef = TypedDict(
    "GetWorkflowRunsResponseTypeDef",
    {
        "Runs": List[WorkflowRunTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
WorkflowTypeDef = TypedDict(
    "WorkflowTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "DefaultRunProperties": NotRequired[Dict[str, str]],
        "CreatedOn": NotRequired[datetime],
        "LastModifiedOn": NotRequired[datetime],
        "LastRun": NotRequired[WorkflowRunTypeDef],
        "Graph": NotRequired[WorkflowGraphTypeDef],
        "MaxConcurrentRuns": NotRequired[int],
        "BlueprintDetails": NotRequired[BlueprintDetailsTypeDef],
    },
)
BatchGetWorkflowsResponseTypeDef = TypedDict(
    "BatchGetWorkflowsResponseTypeDef",
    {
        "Workflows": List[WorkflowTypeDef],
        "MissingWorkflows": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetWorkflowResponseTypeDef = TypedDict(
    "GetWorkflowResponseTypeDef",
    {
        "Workflow": WorkflowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

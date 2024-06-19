"""
Type annotations for bedrock-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ConversationRoleType,
    GuardrailContentFilterConfidenceType,
    GuardrailContentFilterTypeType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationPolicyActionType,
    GuardrailStreamProcessingModeType,
    GuardrailTraceType,
    ImageFormatType,
    StopReasonType,
    ToolResultStatusType,
    TraceType,
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
    "BlobTypeDef",
    "ToolUseBlockDeltaTypeDef",
    "ToolUseBlockOutputTypeDef",
    "ToolUseBlockStartTypeDef",
    "ContentBlockStopEventTypeDef",
    "ToolUseBlockTypeDef",
    "ConverseMetricsTypeDef",
    "GuardrailConfigurationTypeDef",
    "InferenceConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "TokenUsageTypeDef",
    "ConverseStreamMetricsTypeDef",
    "InternalServerExceptionTypeDef",
    "MessageStartEventTypeDef",
    "MessageStopEventTypeDef",
    "ModelStreamErrorExceptionTypeDef",
    "ThrottlingExceptionTypeDef",
    "ValidationExceptionTypeDef",
    "GuardrailStreamConfigurationTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailConverseTextBlockTypeDef",
    "GuardrailCustomWordTypeDef",
    "GuardrailManagedWordTypeDef",
    "GuardrailPiiEntityFilterTypeDef",
    "GuardrailRegexFilterTypeDef",
    "GuardrailTopicTypeDef",
    "ImageSourceOutputTypeDef",
    "ModelTimeoutExceptionTypeDef",
    "PayloadPartTypeDef",
    "SpecificToolChoiceTypeDef",
    "ToolInputSchemaTypeDef",
    "ImageSourceTypeDef",
    "InvokeModelRequestRequestTypeDef",
    "InvokeModelWithResponseStreamRequestRequestTypeDef",
    "ContentBlockDeltaTypeDef",
    "ContentBlockStartTypeDef",
    "InvokeModelResponseTypeDef",
    "GuardrailContentPolicyAssessmentTypeDef",
    "GuardrailConverseContentBlockTypeDef",
    "GuardrailWordPolicyAssessmentTypeDef",
    "GuardrailSensitiveInformationPolicyAssessmentTypeDef",
    "GuardrailTopicPolicyAssessmentTypeDef",
    "ImageBlockOutputTypeDef",
    "ResponseStreamTypeDef",
    "ToolChoiceTypeDef",
    "ToolSpecificationTypeDef",
    "ImageBlockTypeDef",
    "ContentBlockDeltaEventTypeDef",
    "ContentBlockStartEventTypeDef",
    "SystemContentBlockTypeDef",
    "GuardrailAssessmentTypeDef",
    "ToolResultContentBlockOutputTypeDef",
    "InvokeModelWithResponseStreamResponseTypeDef",
    "ToolTypeDef",
    "ToolResultContentBlockTypeDef",
    "GuardrailTraceAssessmentTypeDef",
    "ToolResultBlockOutputTypeDef",
    "ToolConfigurationTypeDef",
    "ToolResultBlockTypeDef",
    "ConverseStreamTraceTypeDef",
    "ConverseTraceTypeDef",
    "ContentBlockOutputTypeDef",
    "ContentBlockTypeDef",
    "ConverseStreamMetadataEventTypeDef",
    "MessageOutputTypeDef",
    "MessageTypeDef",
    "ConverseStreamOutputTypeDef",
    "ConverseOutputTypeDef",
    "MessageUnionTypeDef",
    "ConverseStreamResponseTypeDef",
    "ConverseResponseTypeDef",
    "ConverseRequestRequestTypeDef",
    "ConverseStreamRequestRequestTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ToolUseBlockDeltaTypeDef = TypedDict(
    "ToolUseBlockDeltaTypeDef",
    {
        "input": str,
    },
)
ToolUseBlockOutputTypeDef = TypedDict(
    "ToolUseBlockOutputTypeDef",
    {
        "toolUseId": str,
        "name": str,
        "input": Dict[str, Any],
    },
)
ToolUseBlockStartTypeDef = TypedDict(
    "ToolUseBlockStartTypeDef",
    {
        "toolUseId": str,
        "name": str,
    },
)
ContentBlockStopEventTypeDef = TypedDict(
    "ContentBlockStopEventTypeDef",
    {
        "contentBlockIndex": int,
    },
)
ToolUseBlockTypeDef = TypedDict(
    "ToolUseBlockTypeDef",
    {
        "toolUseId": str,
        "name": str,
        "input": Mapping[str, Any],
    },
)
ConverseMetricsTypeDef = TypedDict(
    "ConverseMetricsTypeDef",
    {
        "latencyMs": int,
    },
)
GuardrailConfigurationTypeDef = TypedDict(
    "GuardrailConfigurationTypeDef",
    {
        "guardrailIdentifier": str,
        "guardrailVersion": str,
        "trace": NotRequired[GuardrailTraceType],
    },
)
InferenceConfigurationTypeDef = TypedDict(
    "InferenceConfigurationTypeDef",
    {
        "maxTokens": NotRequired[int],
        "temperature": NotRequired[float],
        "topP": NotRequired[float],
        "stopSequences": NotRequired[Sequence[str]],
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
TokenUsageTypeDef = TypedDict(
    "TokenUsageTypeDef",
    {
        "inputTokens": int,
        "outputTokens": int,
        "totalTokens": int,
    },
)
ConverseStreamMetricsTypeDef = TypedDict(
    "ConverseStreamMetricsTypeDef",
    {
        "latencyMs": int,
    },
)
InternalServerExceptionTypeDef = TypedDict(
    "InternalServerExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
MessageStartEventTypeDef = TypedDict(
    "MessageStartEventTypeDef",
    {
        "role": ConversationRoleType,
    },
)
MessageStopEventTypeDef = TypedDict(
    "MessageStopEventTypeDef",
    {
        "stopReason": StopReasonType,
        "additionalModelResponseFields": NotRequired[Dict[str, Any]],
    },
)
ModelStreamErrorExceptionTypeDef = TypedDict(
    "ModelStreamErrorExceptionTypeDef",
    {
        "message": NotRequired[str],
        "originalStatusCode": NotRequired[int],
        "originalMessage": NotRequired[str],
    },
)
ThrottlingExceptionTypeDef = TypedDict(
    "ThrottlingExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ValidationExceptionTypeDef = TypedDict(
    "ValidationExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
GuardrailStreamConfigurationTypeDef = TypedDict(
    "GuardrailStreamConfigurationTypeDef",
    {
        "guardrailIdentifier": str,
        "guardrailVersion": str,
        "trace": NotRequired[GuardrailTraceType],
        "streamProcessingMode": NotRequired[GuardrailStreamProcessingModeType],
    },
)
GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "confidence": GuardrailContentFilterConfidenceType,
        "action": Literal["BLOCKED"],
    },
)
GuardrailConverseTextBlockTypeDef = TypedDict(
    "GuardrailConverseTextBlockTypeDef",
    {
        "text": str,
    },
)
GuardrailCustomWordTypeDef = TypedDict(
    "GuardrailCustomWordTypeDef",
    {
        "match": str,
        "action": Literal["BLOCKED"],
    },
)
GuardrailManagedWordTypeDef = TypedDict(
    "GuardrailManagedWordTypeDef",
    {
        "match": str,
        "type": Literal["PROFANITY"],
        "action": Literal["BLOCKED"],
    },
)
GuardrailPiiEntityFilterTypeDef = TypedDict(
    "GuardrailPiiEntityFilterTypeDef",
    {
        "match": str,
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationPolicyActionType,
    },
)
GuardrailRegexFilterTypeDef = TypedDict(
    "GuardrailRegexFilterTypeDef",
    {
        "action": GuardrailSensitiveInformationPolicyActionType,
        "name": NotRequired[str],
        "match": NotRequired[str],
        "regex": NotRequired[str],
    },
)
GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "name": str,
        "type": Literal["DENY"],
        "action": Literal["BLOCKED"],
    },
)
ImageSourceOutputTypeDef = TypedDict(
    "ImageSourceOutputTypeDef",
    {
        "bytes": NotRequired[bytes],
    },
)
ModelTimeoutExceptionTypeDef = TypedDict(
    "ModelTimeoutExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
PayloadPartTypeDef = TypedDict(
    "PayloadPartTypeDef",
    {
        "bytes": NotRequired[bytes],
    },
)
SpecificToolChoiceTypeDef = TypedDict(
    "SpecificToolChoiceTypeDef",
    {
        "name": str,
    },
)
ToolInputSchemaTypeDef = TypedDict(
    "ToolInputSchemaTypeDef",
    {
        "json": NotRequired[Mapping[str, Any]],
    },
)
ImageSourceTypeDef = TypedDict(
    "ImageSourceTypeDef",
    {
        "bytes": NotRequired[BlobTypeDef],
    },
)
InvokeModelRequestRequestTypeDef = TypedDict(
    "InvokeModelRequestRequestTypeDef",
    {
        "body": BlobTypeDef,
        "modelId": str,
        "contentType": NotRequired[str],
        "accept": NotRequired[str],
        "trace": NotRequired[TraceType],
        "guardrailIdentifier": NotRequired[str],
        "guardrailVersion": NotRequired[str],
    },
)
InvokeModelWithResponseStreamRequestRequestTypeDef = TypedDict(
    "InvokeModelWithResponseStreamRequestRequestTypeDef",
    {
        "body": BlobTypeDef,
        "modelId": str,
        "contentType": NotRequired[str],
        "accept": NotRequired[str],
        "trace": NotRequired[TraceType],
        "guardrailIdentifier": NotRequired[str],
        "guardrailVersion": NotRequired[str],
    },
)
ContentBlockDeltaTypeDef = TypedDict(
    "ContentBlockDeltaTypeDef",
    {
        "text": NotRequired[str],
        "toolUse": NotRequired[ToolUseBlockDeltaTypeDef],
    },
)
ContentBlockStartTypeDef = TypedDict(
    "ContentBlockStartTypeDef",
    {
        "toolUse": NotRequired[ToolUseBlockStartTypeDef],
    },
)
InvokeModelResponseTypeDef = TypedDict(
    "InvokeModelResponseTypeDef",
    {
        "body": StreamingBody,
        "contentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GuardrailContentPolicyAssessmentTypeDef = TypedDict(
    "GuardrailContentPolicyAssessmentTypeDef",
    {
        "filters": List[GuardrailContentFilterTypeDef],
    },
)
GuardrailConverseContentBlockTypeDef = TypedDict(
    "GuardrailConverseContentBlockTypeDef",
    {
        "text": NotRequired[GuardrailConverseTextBlockTypeDef],
    },
)
GuardrailWordPolicyAssessmentTypeDef = TypedDict(
    "GuardrailWordPolicyAssessmentTypeDef",
    {
        "customWords": List[GuardrailCustomWordTypeDef],
        "managedWordLists": List[GuardrailManagedWordTypeDef],
    },
)
GuardrailSensitiveInformationPolicyAssessmentTypeDef = TypedDict(
    "GuardrailSensitiveInformationPolicyAssessmentTypeDef",
    {
        "piiEntities": List[GuardrailPiiEntityFilterTypeDef],
        "regexes": List[GuardrailRegexFilterTypeDef],
    },
)
GuardrailTopicPolicyAssessmentTypeDef = TypedDict(
    "GuardrailTopicPolicyAssessmentTypeDef",
    {
        "topics": List[GuardrailTopicTypeDef],
    },
)
ImageBlockOutputTypeDef = TypedDict(
    "ImageBlockOutputTypeDef",
    {
        "format": ImageFormatType,
        "source": ImageSourceOutputTypeDef,
    },
)
ResponseStreamTypeDef = TypedDict(
    "ResponseStreamTypeDef",
    {
        "chunk": NotRequired[PayloadPartTypeDef],
        "internalServerException": NotRequired[InternalServerExceptionTypeDef],
        "modelStreamErrorException": NotRequired[ModelStreamErrorExceptionTypeDef],
        "validationException": NotRequired[ValidationExceptionTypeDef],
        "throttlingException": NotRequired[ThrottlingExceptionTypeDef],
        "modelTimeoutException": NotRequired[ModelTimeoutExceptionTypeDef],
    },
)
ToolChoiceTypeDef = TypedDict(
    "ToolChoiceTypeDef",
    {
        "auto": NotRequired[Mapping[str, Any]],
        "any": NotRequired[Mapping[str, Any]],
        "tool": NotRequired[SpecificToolChoiceTypeDef],
    },
)
ToolSpecificationTypeDef = TypedDict(
    "ToolSpecificationTypeDef",
    {
        "name": str,
        "inputSchema": ToolInputSchemaTypeDef,
        "description": NotRequired[str],
    },
)
ImageBlockTypeDef = TypedDict(
    "ImageBlockTypeDef",
    {
        "format": ImageFormatType,
        "source": ImageSourceTypeDef,
    },
)
ContentBlockDeltaEventTypeDef = TypedDict(
    "ContentBlockDeltaEventTypeDef",
    {
        "delta": ContentBlockDeltaTypeDef,
        "contentBlockIndex": int,
    },
)
ContentBlockStartEventTypeDef = TypedDict(
    "ContentBlockStartEventTypeDef",
    {
        "start": ContentBlockStartTypeDef,
        "contentBlockIndex": int,
    },
)
SystemContentBlockTypeDef = TypedDict(
    "SystemContentBlockTypeDef",
    {
        "text": NotRequired[str],
        "guardContent": NotRequired[GuardrailConverseContentBlockTypeDef],
    },
)
GuardrailAssessmentTypeDef = TypedDict(
    "GuardrailAssessmentTypeDef",
    {
        "topicPolicy": NotRequired[GuardrailTopicPolicyAssessmentTypeDef],
        "contentPolicy": NotRequired[GuardrailContentPolicyAssessmentTypeDef],
        "wordPolicy": NotRequired[GuardrailWordPolicyAssessmentTypeDef],
        "sensitiveInformationPolicy": NotRequired[
            GuardrailSensitiveInformationPolicyAssessmentTypeDef
        ],
    },
)
ToolResultContentBlockOutputTypeDef = TypedDict(
    "ToolResultContentBlockOutputTypeDef",
    {
        "json": NotRequired[Dict[str, Any]],
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockOutputTypeDef],
    },
)
InvokeModelWithResponseStreamResponseTypeDef = TypedDict(
    "InvokeModelWithResponseStreamResponseTypeDef",
    {
        "body": "EventStream[ResponseStreamTypeDef]",
        "contentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ToolTypeDef = TypedDict(
    "ToolTypeDef",
    {
        "toolSpec": NotRequired[ToolSpecificationTypeDef],
    },
)
ToolResultContentBlockTypeDef = TypedDict(
    "ToolResultContentBlockTypeDef",
    {
        "json": NotRequired[Mapping[str, Any]],
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockTypeDef],
    },
)
GuardrailTraceAssessmentTypeDef = TypedDict(
    "GuardrailTraceAssessmentTypeDef",
    {
        "modelOutput": NotRequired[List[str]],
        "inputAssessment": NotRequired[Dict[str, GuardrailAssessmentTypeDef]],
        "outputAssessments": NotRequired[Dict[str, List[GuardrailAssessmentTypeDef]]],
    },
)
ToolResultBlockOutputTypeDef = TypedDict(
    "ToolResultBlockOutputTypeDef",
    {
        "toolUseId": str,
        "content": List[ToolResultContentBlockOutputTypeDef],
        "status": NotRequired[ToolResultStatusType],
    },
)
ToolConfigurationTypeDef = TypedDict(
    "ToolConfigurationTypeDef",
    {
        "tools": Sequence[ToolTypeDef],
        "toolChoice": NotRequired[ToolChoiceTypeDef],
    },
)
ToolResultBlockTypeDef = TypedDict(
    "ToolResultBlockTypeDef",
    {
        "toolUseId": str,
        "content": Sequence[ToolResultContentBlockTypeDef],
        "status": NotRequired[ToolResultStatusType],
    },
)
ConverseStreamTraceTypeDef = TypedDict(
    "ConverseStreamTraceTypeDef",
    {
        "guardrail": NotRequired[GuardrailTraceAssessmentTypeDef],
    },
)
ConverseTraceTypeDef = TypedDict(
    "ConverseTraceTypeDef",
    {
        "guardrail": NotRequired[GuardrailTraceAssessmentTypeDef],
    },
)
ContentBlockOutputTypeDef = TypedDict(
    "ContentBlockOutputTypeDef",
    {
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockOutputTypeDef],
        "toolUse": NotRequired[ToolUseBlockOutputTypeDef],
        "toolResult": NotRequired[ToolResultBlockOutputTypeDef],
        "guardContent": NotRequired[GuardrailConverseContentBlockTypeDef],
    },
)
ContentBlockTypeDef = TypedDict(
    "ContentBlockTypeDef",
    {
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockTypeDef],
        "toolUse": NotRequired[ToolUseBlockTypeDef],
        "toolResult": NotRequired[ToolResultBlockTypeDef],
        "guardContent": NotRequired[GuardrailConverseContentBlockTypeDef],
    },
)
ConverseStreamMetadataEventTypeDef = TypedDict(
    "ConverseStreamMetadataEventTypeDef",
    {
        "usage": TokenUsageTypeDef,
        "metrics": ConverseStreamMetricsTypeDef,
        "trace": NotRequired[ConverseStreamTraceTypeDef],
    },
)
MessageOutputTypeDef = TypedDict(
    "MessageOutputTypeDef",
    {
        "role": ConversationRoleType,
        "content": List[ContentBlockOutputTypeDef],
    },
)
MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "role": ConversationRoleType,
        "content": Sequence[ContentBlockTypeDef],
    },
)
ConverseStreamOutputTypeDef = TypedDict(
    "ConverseStreamOutputTypeDef",
    {
        "messageStart": NotRequired[MessageStartEventTypeDef],
        "contentBlockStart": NotRequired[ContentBlockStartEventTypeDef],
        "contentBlockDelta": NotRequired[ContentBlockDeltaEventTypeDef],
        "contentBlockStop": NotRequired[ContentBlockStopEventTypeDef],
        "messageStop": NotRequired[MessageStopEventTypeDef],
        "metadata": NotRequired[ConverseStreamMetadataEventTypeDef],
        "internalServerException": NotRequired[InternalServerExceptionTypeDef],
        "modelStreamErrorException": NotRequired[ModelStreamErrorExceptionTypeDef],
        "validationException": NotRequired[ValidationExceptionTypeDef],
        "throttlingException": NotRequired[ThrottlingExceptionTypeDef],
    },
)
ConverseOutputTypeDef = TypedDict(
    "ConverseOutputTypeDef",
    {
        "message": NotRequired[MessageOutputTypeDef],
    },
)
MessageUnionTypeDef = Union[MessageTypeDef, MessageOutputTypeDef]
ConverseStreamResponseTypeDef = TypedDict(
    "ConverseStreamResponseTypeDef",
    {
        "stream": "EventStream[ConverseStreamOutputTypeDef]",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConverseResponseTypeDef = TypedDict(
    "ConverseResponseTypeDef",
    {
        "output": ConverseOutputTypeDef,
        "stopReason": StopReasonType,
        "usage": TokenUsageTypeDef,
        "metrics": ConverseMetricsTypeDef,
        "additionalModelResponseFields": Dict[str, Any],
        "trace": ConverseTraceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConverseRequestRequestTypeDef = TypedDict(
    "ConverseRequestRequestTypeDef",
    {
        "modelId": str,
        "messages": Sequence[MessageUnionTypeDef],
        "system": NotRequired[Sequence[SystemContentBlockTypeDef]],
        "inferenceConfig": NotRequired[InferenceConfigurationTypeDef],
        "toolConfig": NotRequired[ToolConfigurationTypeDef],
        "guardrailConfig": NotRequired[GuardrailConfigurationTypeDef],
        "additionalModelRequestFields": NotRequired[Mapping[str, Any]],
        "additionalModelResponseFieldPaths": NotRequired[Sequence[str]],
    },
)
ConverseStreamRequestRequestTypeDef = TypedDict(
    "ConverseStreamRequestRequestTypeDef",
    {
        "modelId": str,
        "messages": Sequence[MessageUnionTypeDef],
        "system": NotRequired[Sequence[SystemContentBlockTypeDef]],
        "inferenceConfig": NotRequired[InferenceConfigurationTypeDef],
        "toolConfig": NotRequired[ToolConfigurationTypeDef],
        "guardrailConfig": NotRequired[GuardrailStreamConfigurationTypeDef],
        "additionalModelRequestFields": NotRequired[Mapping[str, Any]],
        "additionalModelResponseFieldPaths": NotRequired[Sequence[str]],
    },
)

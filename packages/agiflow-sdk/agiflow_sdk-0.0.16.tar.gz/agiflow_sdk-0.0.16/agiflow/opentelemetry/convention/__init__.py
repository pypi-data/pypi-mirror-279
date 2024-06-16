from agiflow.opentelemetry.convention.database_span_attributes import (
  DatabaseSpanAttributes,
  DatabaseSpanAttributesValidator
)
from agiflow.opentelemetry.convention.framework_span_attributes import (
  FrameworkSpanAttributes,
  FrameworkSpanAttributesValidator
)
from agiflow.opentelemetry.convention.llm_span_attributes import (
  LLMSpanAttributes,
  LLMSpanAttributesValidator
)
from agiflow.opentelemetry.convention.agiflow_attributes import (
  AgiflowSpanAttributes,
  AgiflowSpanAttributesValidator
)
from agiflow.opentelemetry.convention.constants import (
  Event,
  OpenAIMethods,
  ChromaDBMethods,
  PineconeMethods,
  AgiflowServiceTypes,
  WeaviateMethods,
  LLMTypes,
  LLMPromptKeys,
  LLMPromptRoles,
  LLMResponseKeys,
  LLMTokenUsageKeys,
)


class SpanAttributes(AgiflowSpanAttributes, LLMSpanAttributes, FrameworkSpanAttributes, DatabaseSpanAttributes):
    """
    All span attributes collected by Agiflow.
    Using this for key value instead of hard coding to ensure
    consistent telemetry schema.
    """
    def __init__(self):
        super()


__all__ = [
  'LLMSpanAttributes',
  'DatabaseSpanAttributes',
  'FrameworkSpanAttributes',
  'Event',
  'OpenAIMethods',
  'ChromaDBMethods',
  'PineconeMethods',
  'FrameworkSpanAttributesValidator',
  'DatabaseSpanAttributesValidator',
  'LLMSpanAttributesValidator',
  'AgiflowSpanAttributesValidator',
  'AgiflowSpanAttributes',
  'AgiflowServiceTypes',
  "LLMTypes",
  "LLMPromptKeys",
  "LLMPromptRoles",
  "LLMResponseKeys",
  "LLMTokenUsageKeys",
  "SpanAttributes",
  "WeaviateMethods",
  ]

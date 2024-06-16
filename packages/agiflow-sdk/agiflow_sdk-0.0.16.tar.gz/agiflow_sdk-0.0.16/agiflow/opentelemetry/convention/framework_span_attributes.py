from __future__ import annotations

from typing import Optional

from pydantic import Field
from agiflow.opentelemetry.convention.agiflow_attributes import AgiflowSpanAttributesValidator


class FrameworkSpanAttributes():
    FRAMEWORK_ENTRYPOINT = 'framework.entrypoint'
    FRAMEWORK_NODE = 'framework.node'
    FRAMEWORK_EDGE = 'framework.edge'
    FRAMEWORK_FINISHPOINT = 'framework.finishpoint'


class FrameworkSpanAttributesValidator(AgiflowSpanAttributesValidator):
    FRAMEWORK_ENDPOINT: Optional[str] = Field(None, alias=FrameworkSpanAttributes.FRAMEWORK_ENTRYPOINT)
    FRAMEWORK_NODE: Optional[str] = Field(None, alias=FrameworkSpanAttributes.FRAMEWORK_NODE)
    FRAMEWORK_EDGE: Optional[str] = Field(None, alias=FrameworkSpanAttributes.FRAMEWORK_EDGE)
    FRAMEWORK_FINISH_POINT: Optional[str] = Field(None, alias=FrameworkSpanAttributes.FRAMEWORK_FINISHPOINT)

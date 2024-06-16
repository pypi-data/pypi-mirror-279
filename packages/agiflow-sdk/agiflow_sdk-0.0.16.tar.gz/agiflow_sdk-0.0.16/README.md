# Agiflow Python Sdk

Agiflow’s Python SDK allows you to easily start monitoring and debugging your LLM execution. Tracing is done in a non-intrusive way, built on top of OpenTelemetry. You can choose to export the traces to Agiflow, or to your existing observability stack.

Please visit [Agiflow Python Sdk documentation](https://docs.agiflow.io/libraries/python/getting-started) for details.

## Getting started
Get your API Key from https://app.agiflow.io and set environment variable AGIFLOW_API_KEY=<API_KEY>. Then, at the root of you application, start instrumentation with:

``` python
from agiflow import Agiflow


Agiflow.init(
  name="APP NAME"
)
```


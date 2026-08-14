**EcoLogits API** provides a language-agnostic HTTP interface to the
[EcoLogits](https://ecologits.ai) library, so any stack — not just Python — can
estimate the environmental footprint of generative-AI inference.
It supports LLM request estimations and video generation estimations through
separate endpoint families because their inputs and model catalogs differ.

## What is EcoLogits?

EcoLogits is an open-source project (part of the CodeCarbon non-profit) that estimates
the environmental impacts of AI model usage at inference time.
It follows Life Cycle Assessment (LCA) principles defined by ISO 14044.

## Environmental metrics

| Metric | Unit | Description |
|---|---|---|
| **Energy** | kWh | Energy consumed by the request |
| **GWP** (Global Warming Potential) | kgCO₂eq | Greenhouse gas emissions |
| **ADPe** (Abiotic Depletion Potential) | kgSbeq | Mineral & metal resource depletion |
| **PE** (Primary Energy) | MJ | Total primary energy consumed |
| **WCF** (Water Consumption Footprint) | L | Fresh water consumed by data centers and power generation, not returned to its source |

Results are returned as **approximation intervals** (min/max range), not single point estimates.

Use `/v1beta/estimations` with `/v1beta/providers` and `/v1beta/models/{provider}`
for LLM inference. Use `/v1beta/video-estimations` with `/v1beta/video-providers`
and `/v1beta/video-models/{provider}` for video generation.

## Useful links

- [EcoLogits documentation](https://ecologits.ai/)
- [Methodology](https://ecologits.ai/latest/methodology/)
- [GitHub repository](https://github.com/mlco2/ecologits)

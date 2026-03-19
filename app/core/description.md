**EcoLogits API** provides a language-agnostic HTTP interface to the
[EcoLogits](https://ecologits.ai) library, so any stack — not just Python — can
estimate the environmental footprint of generative-AI inference.

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

## Useful links

- [EcoLogits documentation](https://ecologits.ai/dev/)
- [Methodology](https://ecologits.ai/dev/methodology/)
- [GitHub repository](https://github.com/mlco2/ecologits)

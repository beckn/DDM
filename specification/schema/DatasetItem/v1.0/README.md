# DatasetItem v1.0

**Schema ID:** `https://schema.beckn.io/DatasetItem/v1.0`
**Status:** Superseded by [v1.1](../v1.1/)

---

## Overview

Metadata for a dataset product in a Beckn catalog, extending [schema.org Dataset](https://schema.org/Dataset). Attached to `Item.itemAttributes` in `on_discover`. Covers static, recurring, and real-time datasets delivered inline, by download, in a data enclave, or off-channel.

---

## Files

| File | Description |
|------|-------------|
| [`attributes.yaml`](./attributes.yaml) | OpenAPI 3.1 schema |
| [`context.jsonld`](./context.jsonld) | JSON-LD 1.1 term → IRI mappings |
| [`vocab.jsonld`](./vocab.jsonld) | RDF vocabulary — class and property definitions |

---

## Fields

Required: `schema:identifier`, `schema:name`, `schema:temporalCoverage`.

| Field | Type | Description |
|-------|------|-------------|
| `schema:*` | — | Standard schema.org Dataset fields: `description`, `spatialCoverage`, `license`, `distribution`, `variableMeasured`, `measurementTechnique`, `usageInfo`, `conditionsOfAccess`, `temporalResolution`, `spatialResolution`, `creator`, `isBasedOn` |
| `dataset:refreshType` | string | Refresh model: `STATIC`, `RECURRING`, `REAL_TIME` |
| `dataset:refreshFrequency` | string | Refresh cadence for recurring / real-time datasets |
| `dataset:granularity` | string | Observation unit granularity (e.g. `GRID_DAILY`, `STATION_HOURLY`) |
| `dataset:rowCountEstimate` | integer | Approximate row count |
| `dataset:columnCount` | integer | Number of columns |
| `dataset:sensitivityLevel` | string | Sensitivity classification (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, …) |
| `dataset:verticalRange` | string \| object | Vertical extent (e.g. surface, 0–2 km AGL) |
| `dataset:dataType` | string | Data representation (e.g. `GriddedProbabilityField`, `TimeSeries`) |
| `dataset:rawUpdateFrequency` | string | Update frequency of the underlying raw dataset |
| `dataset:latestRawDataAt` | date-time | Timestamp of the latest raw data feeding this dataset |
| `dataset:accessMethod` | enum | `INLINE`, `DOWNLOAD`, `DATA_ENCLAVE`, `OFF_CHANNEL` |
| `dataset:dataPayload` | object | Self-describing JSON-LD payload carried inline when `accessMethod` is `INLINE` (`@context` must resolve to the payload schema) |
| `dataset:qualityFlags` | object | Quality metrics: `gapFilledPercent`, `outlierRemovedPercent`, `latencyMinutes`, `uptime99DayPercent`, `validationMethod` |

## Context URL

```
https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.0/context.jsonld
```

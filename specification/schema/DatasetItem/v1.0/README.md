# DatasetItem — v1.0

Base schema for describing a dataset product in a Beckn catalog. Extends [`schema:Dataset`](https://schema.org/Dataset) with Beckn-specific quality, sensitivity, and delivery attributes.

## Required fields

| Field | Notes |
|---|---|
| `schema:identifier` | Stable ID for the dataset. Buyers reference this in `confirm`. |
| `schema:name` | Human-readable name. |
| `schema:temporalCoverage` | ISO 8601 interval, e.g. `2026-01-01/2026-03-31`. |

## Access methods

`dataset:accessMethod` (enum):

| Value | Meaning | Fulfillment |
|---|---|---|
| `INLINE` | Data is embedded in the beckn message via `dataset:dataPayload`. | Payload arrives in `on_confirm` / `on_status` `performanceAttributes`. |
| `DOWNLOAD` | Consumer fetches from a signed URL. | URL delivered in `DatasetFulfillment.fulfillment:accessUrl`. |
| `DATA_ENCLAVE` | Consumer accesses data inside a secure enclave. | Enclave endpoint and credentials negotiated off-channel. |
| `OFF_CHANNEL` | Delivery arranged outside the beckn network. | Provider and buyer coordinate directly. |

## Catalog example — `DOWNLOAD`

```json
{
  "@context": "https://schema.beckn.io/DatasetItem/v1.0/context.jsonld",
  "@type": "DatasetItem",
  "schema:identifier": "ds-rainprob-maharashtra-march-2026",
  "schema:name": "Rainwater Probability — Maharashtra — March 2026",
  "schema:temporalCoverage": "2026-03-01/2026-03-31",
  "dataset:refreshType": "RECURRING",
  "dataset:refreshFrequency": "P1D",
  "dataset:granularity": "STATION_HOURLY",
  "dataset:sensitivityLevel": "PUBLIC",
  "dataset:accessMethod": "DOWNLOAD"
}
```

## Catalog example — `INLINE`

```json
{
  "@context": "https://schema.beckn.io/DatasetItem/v1.0/context.jsonld",
  "@type": "DatasetItem",
  "schema:identifier": "ds-ami-meter-data-blr-zone-a-q1-2026",
  "schema:name": "AMI Meter Data — Bengaluru Zone A — Q1 2026",
  "schema:temporalCoverage": "2026-01-01/2026-03-31",
  "dataset:accessMethod": "INLINE",
  "dataset:dataPayload": {
    "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld",
    "@type": "MeterData"
  }
}
```

## Quality flags

`dataset:qualityFlags` is a sub-object aggregating standard QA/QC metrics:

| Field | Description |
|---|---|
| `dataset:gapFilledPercent` | Percentage of records gap-filled by imputation. |
| `dataset:outlierRemovedPercent` | Percentage of records removed as outliers. |
| `dataset:latencyMinutes` | Typical latency between observation and availability. |
| `dataset:uptime99DayPercent` | Feed uptime over the trailing 99 days. |
| `dataset:validationMethod` | Standard or algorithm used (e.g. `IS-13731-2024`). |

## Canonical URL

```
https://schema.beckn.io/DatasetItem/v1.0/context.jsonld
```

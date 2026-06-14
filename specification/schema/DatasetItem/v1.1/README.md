# DatasetItem — v1.1

Extends [v1.0](../v1.0/attributes.yaml) with streaming transport access methods and catalog-time stream metadata. Fully backward-compatible — all v1.0 fields and enum values are preserved unchanged.

## What's new in v1.1

### Extended `dataset:accessMethod` enum

Four new values alongside the existing `INLINE`, `DOWNLOAD`, `DATA_ENCLAVE`, `OFF_CHANNEL`:

| Value | Transport | Credentials delivered via |
|---|---|---|
| `MQTT` | MQTT 5.0 broker subscription | `DatasetFulfillment/v1.1` `streamConnection` in `on_confirm` |
| `KAFKA` | Apache Kafka consumer | `DatasetFulfillment/v1.1` `streamConnection` in `on_confirm` |
| `API` | REST API with API key or bearer token | `DatasetFulfillment/v1.1` `streamConnection` in `on_confirm` |
| `DATA_LAKE` | Cloud object storage — S3 / GCS / ADLS | `DatasetFulfillment/v1.1` `streamConnection` in `on_confirm` |

### New `dataset:streamMeta` field

A catalog-time sub-object that describes the stream's topology **without exposing credentials**. Buyers use this to understand what they are purchasing and to configure deserializers before the stream starts.

```json
"dataset:streamMeta": {
  "dataset:streamProtocol": "MQTT",
  "dataset:messageFormat": "JSON",
  "dataset:updateFrequency": "PT15M",
  "dataset:messageSchemaUrl": "https://example.com/schemas/meter-reading-v2.json"
}
```

| Field | Type | Description |
|---|---|---|
| `dataset:streamProtocol` | `MQTT` \| `KAFKA` \| `API` \| `DATA_LAKE` | Informational mirror of `accessMethod` |
| `dataset:messageFormat` | string | Message encoding: `JSON`, `NDJSON`, `Avro`, `Protobuf`, `Parquet`, `CSV`, … |
| `dataset:updateFrequency` | ISO 8601 duration or `REAL_TIME` | How often new data arrives, e.g. `PT15M`, `PT1S`, `REAL_TIME` |
| `dataset:messageSchemaUrl` | URI | URL to the message schema (JSON Schema / Avro / Protobuf / OpenAPI) |

## Beckn handshake flow for streaming transports

```
discover      BAP filters by dataset:accessMethod in [MQTT, KAFKA, API, DATA_LAKE]
on_discover   BPP returns items with dataset:streamMeta — no credentials yet
confirm       BAP confirms and pays
on_confirm    BPP provisions credentials and delivers them in
              performance[].performanceAttributes as DatasetFulfillment/v1.1
              with fulfillment:streamConnection
update        BAP rotates credentials before fulfillment:credentialExpiresAt
on_update     BPP issues fresh fulfillment:streamConnection
```

Credentials never appear in the catalog (`on_discover`). They are provisioned on-demand after `confirm` and delivered in `on_confirm`, scoped to the specific buyer and contract.

## Catalog example

```json
{
  "@context": "https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld",
  "@type": "DatasetItem",
  "schema:identifier": "stream-ami-mqtt-blr-zone-a",
  "schema:name": "AMI Smart Meter Stream — Bengaluru Zone A",
  "schema:temporalCoverage": "2026-05-07/..",
  "dataset:refreshType": "REAL_TIME",
  "dataset:accessMethod": "MQTT",
  "dataset:sensitivityLevel": "CONFIDENTIAL",
  "dataset:streamMeta": {
    "dataset:streamProtocol": "MQTT",
    "dataset:messageFormat": "JSON",
    "dataset:updateFrequency": "PT15M",
    "dataset:messageSchemaUrl": "https://raw.githubusercontent.com/beckn/DEG/main/specification/schema/BecknTimeSeries/v1.0/attributes.yaml"
  }
}
```

See [`/example/v1.1/streaming/`](../../../../example/v1.1/streaming/) for full end-to-end flow examples covering MQTT, Kafka, REST API, and Data Lake.

## Context URL

```
https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld
```

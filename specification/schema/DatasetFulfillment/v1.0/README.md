# DatasetFulfillment v1.0

**Schema ID:** `https://schema.beckn.io/DatasetFulfillment/v1.0`
**Status:** Superseded by [v1.1](../v1.1/)

---

## Overview

Access provisioning details for a fulfilled dataset order, extending [schema.org DataDownload](https://schema.org/DataDownload). Attached via `beckn:deliveryAttributes` and delivered by the BPP in `on_confirm`. Models download-style access with a signed URL, an access window, and optional download quotas.

---

## Files

| File | Description |
|------|-------------|
| [`attributes.yaml`](./attributes.yaml) | OpenAPI 3.1 schema |
| [`context.jsonld`](./context.jsonld) | JSON-LD 1.1 term → IRI mappings |
| [`vocab.jsonld`](./vocab.jsonld) | RDF vocabulary — class and property definitions |

---

## Fields

Required: `fulfillment:accessMethod`, `fulfillment:accessUrl`, `fulfillment:accessStart`, `fulfillment:accessEnd`.

| Field | Type | Description |
|-------|------|-------------|
| `fulfillment:accessMethod` | string | Access method code: `DOWNLOAD`, `API`, `STREAM`, `DATA_ROOM`, `SFTP` |
| `fulfillment:accessUrl` | uri | Signed or time-limited URL for accessing the dataset |
| `fulfillment:accessStart` | date-time | Start of the access window |
| `fulfillment:accessEnd` | date-time | End of the access window |
| `fulfillment:format` | string | Delivered file format (e.g. Parquet, CSV, JSON) |
| `fulfillment:fileSizeBytes` | integer | Approximate delivered file size |
| `fulfillment:maxDownloads` | integer | Maximum number of downloads allowed |
| `fulfillment:downloadsUsed` | integer | Downloads already used by the buyer |
| `fulfillment:supportEmail` | email | Support contact for access issues |
| `fulfillment:termsUrl` | uri | Terms and conditions for dataset use |
| `fulfillment:attributionText` | string | Required attribution text |

## Context URL

```
https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetFulfillment/v1.0/context.jsonld
```

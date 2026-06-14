# DatasetFulfillment — v1.0

Base schema for delivering a dataset to a buyer who has confirmed an order. Extends [`schema:DataDownload`](https://schema.org/DataDownload) with Beckn-specific access-window and download-counter attributes.

Carried by the BPP as `performanceAttributes` (or `fulfillmentAttributes`) in `on_confirm` / `on_status` once the buyer has paid and the BPP is ready to deliver.

## Required fields

| Field | Notes |
|---|---|
| `fulfillment:accessMethod` | One of `DOWNLOAD`, `API`, `STREAM`, `DATA_ROOM`, `SFTP`. |
| `fulfillment:accessUrl` | Signed or time-limited URL for retrieval. |
| `fulfillment:accessStart` | ISO 8601 date-time when access opens. |
| `fulfillment:accessEnd` | ISO 8601 date-time when access closes. |

## Fulfillment example — `DOWNLOAD`

```json
{
  "@context": "https://schema.beckn.io/DatasetFulfillment/v1.0/context.jsonld",
  "@type": "DatasetFulfillment",
  "fulfillment:accessMethod": "DOWNLOAD",
  "fulfillment:accessUrl": "https://bucket.s3.ap-south-1.amazonaws.com/rainprob-mh-march-2026.parquet?X-Amz-Signature=...",
  "fulfillment:accessStart": "2026-04-01T09:00:00Z",
  "fulfillment:accessEnd": "2026-04-08T09:00:00Z",
  "fulfillment:format": "Parquet",
  "fulfillment:fileSizeBytes": 47185920,
  "fulfillment:maxDownloads": 3,
  "fulfillment:downloadsUsed": 0,
  "fulfillment:supportEmail": "support@example.com",
  "fulfillment:termsUrl": "https://example.com/dataset-terms",
  "fulfillment:attributionText": "© 2026 Example Provider. Licensed under CC-BY-4.0."
}
```

## Notes

- `accessUrl` MUST be short-lived. The BPP signs the URL with a window expressed by `accessStart`/`accessEnd`; outside that window the URL returns 403/404.
- `maxDownloads` is an advisory hint; enforcement is at the signing layer.
- Beckn messages are signed but not encrypted — treat `accessUrl` like a bearer token. Don't put credentials in the URL beyond what's needed for the pre-signed mechanism.

## Canonical URL

```
https://schema.beckn.io/DatasetFulfillment/v1.0/context.jsonld
```

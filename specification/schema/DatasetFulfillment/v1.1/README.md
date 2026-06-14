# DatasetFulfillment — v1.1

Extends [v1.0](../v1.0/attributes.yaml) with `fulfillment:streamConnection` — a credential delivery object for streaming transport access methods (MQTT, Kafka, REST API, cloud data lake). Fully backward-compatible — all v1.0 fields remain.

## What's new in v1.1

### Relaxed `required`

Only `fulfillment:accessMethod` is required. `accessUrl`, `accessStart`, and `accessEnd` are still present for `DOWNLOAD` but are no longer required fields — streaming methods use `fulfillment:credentialExpiresAt` instead.

### Extended `fulfillment:accessMethod` enum

Aligned with `DatasetItem/v1.1` to include: `DOWNLOAD`, `API`, `STREAM`, `MQTT`, `KAFKA`, `DATA_LAKE`, `DATA_ROOM`, `SFTP`.

### New `fulfillment:streamConnection`

A polymorphic credential object delivered in `performance[].performanceAttributes` of `on_confirm`. The `@type` field discriminates the shape.

```json
"fulfillment:streamConnection": {
  "@type": "MQTTConnection | KafkaConsumerCredentials | ApiCredential | DataLakeCredential",
  "fulfillment:credentialExpiresAt": "<ISO 8601 datetime>",
  ...transport-specific fields...
}
```

**Security note:** All credentials in `streamConnection` MUST be short-lived. The BPP sets `fulfillment:credentialExpiresAt` and the buyer calls `update` before that timestamp to rotate credentials. Beckn messages are signed but not encrypted — treat credentials as you would an API key in a signed webhook.

---

## Credential shapes

### `MQTTConnection`

For `fulfillment:accessMethod: MQTT`. The buyer connects directly to the BPP-operated broker using these credentials.

```json
"fulfillment:streamConnection": {
  "@type": "MQTTConnection",
  "fulfillment:brokerUri": "mqtts://iotcore.example.com:8883",
  "fulfillment:topic": "energy/meters/zone-a/#",
  "fulfillment:qos": 1,
  "fulfillment:clientId": "buyer-org-001-sub",
  "fulfillment:username": "buyer-org-001",
  "fulfillment:password": "<short-lived JWT>",
  "fulfillment:tlsCaCert": "-----BEGIN CERTIFICATE-----\n...",
  "fulfillment:sessionExpiry": "PT24H",
  "fulfillment:credentialExpiresAt": "2026-06-07T09:00:00Z"
}
```

| Field | Required | Description |
|---|---|---|
| `fulfillment:brokerUri` | yes | MQTT broker URI, e.g. `mqtts://` for TLS |
| `fulfillment:topic` | yes | Topic filter with wildcards, e.g. `energy/meters/zone-a/#` |
| `fulfillment:qos` | yes | QoS level: 0, 1, or 2 |
| `fulfillment:clientId` | yes | Broker-provisioned client ID for this buyer |
| `fulfillment:username` | yes | Short-lived username or JWT subject |
| `fulfillment:password` | yes | Short-lived password or JWT token |
| `fulfillment:tlsCaCert` | recommended | PEM CA certificate for `mqtts://` |
| `fulfillment:sessionExpiry` | recommended | MQTT 5.0 Session Expiry Interval (ISO 8601 duration) |
| `fulfillment:credentialExpiresAt` | yes | Rotate before this timestamp via `update` |

---

### `KafkaConsumerCredentials`

For `fulfillment:accessMethod: KAFKA`. The buyer configures a Kafka consumer with these properties.

```json
"fulfillment:streamConnection": {
  "@type": "KafkaConsumerCredentials",
  "fulfillment:bootstrapServers": "pkc-xyz.ap-south1.gcp.confluent.cloud:9092",
  "fulfillment:topicName": "deg.grid-events.india.v1",
  "fulfillment:consumerGroupId": "buyer-org-001-cg",
  "fulfillment:saslMechanism": "PLAIN",
  "fulfillment:saslUsername": "<API_KEY>",
  "fulfillment:saslPassword": "<API_SECRET>",
  "fulfillment:schemaRegistryUrl": "https://psrc-xyz.ap-south1.gcp.confluent.cloud",
  "fulfillment:schemaRegistryUsername": "<SR_KEY>",
  "fulfillment:schemaRegistryPassword": "<SR_SECRET>",
  "fulfillment:startOffset": "latest",
  "fulfillment:credentialExpiresAt": "2026-06-07T09:00:00Z"
}
```

Map directly to standard Kafka client properties:

| `fulfillment:` field | Kafka property |
|---|---|
| `bootstrapServers` | `bootstrap.servers` |
| `saslMechanism` | `sasl.mechanism` |
| `saslUsername` | `sasl.username` / API key |
| `saslPassword` | `sasl.password` / API secret |
| `schemaRegistryUrl` | `schema.registry.url` |
| `consumerGroupId` | `group.id` |

Security protocol is always `SASL_SSL` when `saslMechanism` is present.

---

### `ApiCredential`

For `fulfillment:accessMethod: API`. The buyer calls the REST API using the provisioned token and can explore endpoints via `apiDocUrl`.

```json
"fulfillment:streamConnection": {
  "@type": "ApiCredential",
  "fulfillment:apiEndpoint": "https://api.example.com/v1",
  "fulfillment:apiDocUrl": "https://api.example.com/v1/openapi.yaml",
  "fulfillment:authScheme": "BEARER",
  "fulfillment:bearerToken": "<short-lived JWT>",
  "fulfillment:rateLimitRpm": 60,
  "fulfillment:credentialExpiresAt": "2026-06-07T09:00:00Z"
}
```

| `fulfillment:authScheme` | Credential field used |
|---|---|
| `BEARER` | `fulfillment:bearerToken` |
| `API_KEY` | `fulfillment:apiKey` (sent as `X-Api-Key` header) |
| `BASIC` | `fulfillment:username` + `fulfillment:password` |
| `OAUTH2_CLIENT_CREDENTIALS` | `fulfillment:apiKey` (client ID) + `fulfillment:apiKey` (client secret) — use a pair |

---

### `DataLakeCredential`

For `fulfillment:accessMethod: DATA_LAKE`. Two sub-types via `fulfillment:accessType`:

**PRESIGNED_URL** — static dataset, single signed GET URL:

```json
"fulfillment:streamConnection": {
  "@type": "DataLakeCredential",
  "fulfillment:cloudProvider": "AWS_S3",
  "fulfillment:accessType": "PRESIGNED_URL",
  "fulfillment:presignedUrl": "https://bucket.s3.region.amazonaws.com/path?X-Amz-Signature=...",
  "fulfillment:credentialExpiresAt": "2026-05-08T09:00:00Z"
}
```

**STS_CREDENTIALS** — live-append dataset, temporary IAM credentials:

```json
"fulfillment:streamConnection": {
  "@type": "DataLakeCredential",
  "fulfillment:cloudProvider": "AWS_S3",
  "fulfillment:accessType": "STS_CREDENTIALS",
  "fulfillment:accessKeyId": "ASIA...",
  "fulfillment:secretAccessKey": "...",
  "fulfillment:sessionToken": "...",
  "fulfillment:bucket": "deg-ami-live-ap-south-1",
  "fulfillment:storagePrefix": "buyer-org-001/blr-zone-a/",
  "fulfillment:storageRegion": "ap-south-1",
  "fulfillment:fileFormat": "Parquet",
  "fulfillment:partitionPattern": "year={yyyy}/month={MM}/day={dd}/",
  "fulfillment:credentialExpiresAt": "2026-05-07T21:00:00Z"
}
```

**SAS_TOKEN** — Azure ADLS:

```json
"fulfillment:streamConnection": {
  "@type": "DataLakeCredential",
  "fulfillment:cloudProvider": "AZURE_ADLS",
  "fulfillment:accessType": "SAS_TOKEN",
  "fulfillment:sasToken": "sv=2022-11-02&ss=b&srt=sco&sp=rl&...",
  "fulfillment:storagePrefix": "https://account.dfs.core.windows.net/container/buyer-org-001/",
  "fulfillment:credentialExpiresAt": "2026-05-14T09:00:00Z"
}
```

---

## Credential rotation via `update`

For all streaming methods, the BPP sets `fulfillment:credentialExpiresAt`. Before that timestamp the buyer sends an `update` action; the BPP responds with a fresh `on_update` containing a new `fulfillment:streamConnection` with updated credentials. The buyer swaps credentials without interrupting the stream.

```
update    →  { reason: "credential_renewal" }
on_update ←  new fulfillment:streamConnection with updated credentials
```

## Context URL

```
https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetFulfillment/v1.1/context.jsonld
```

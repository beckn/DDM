# DatasetFulfillment

Access provisioning details for a fulfilled dataset order, attached via `beckn:deliveryAttributes` / `performance[].performanceAttributes`. Extends [schema.org DataDownload](https://schema.org/DataDownload).

**Canonical IRI:** `https://schema.beckn.io/DatasetFulfillment/v1.1`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v1.1](./v1.1/) | Current | Adds `fulfillment:streamConnection` — polymorphic short-lived credential delivery for MQTT, Kafka, REST API, and cloud data-lake transports, with rotation via `update`. Relaxes `required` to `accessMethod` only. |
| [v1.0](./v1.0/) | Superseded | Initial release — download-style access window (`accessUrl`, `accessStart`, `accessEnd`), download quotas, support and attribution fields. |

---

## Purpose

`DatasetFulfillment` describes **how the buyer accesses the data after purchase**: a signed download URL and access window for one-shot deliveries, or provisioned stream credentials for continuous transports. Credentials are scoped to the specific buyer and contract, delivered only in `on_confirm` / `on_update` — never in the catalog.

## Usage

Delivered by the BPP in `on_confirm` (and refreshed in `on_update` for credential rotation). Pairs with [`DatasetItem`](../DatasetItem/), whose `dataset:accessMethod` announces the transport at catalog time. See the version READMEs for field tables and examples.

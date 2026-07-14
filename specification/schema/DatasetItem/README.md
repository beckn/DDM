# DatasetItem

Metadata for a dataset product listed in a Beckn catalog, attached via `beckn:itemAttributes`. Extends [schema.org Dataset](https://schema.org/Dataset) with marketplace-specific fields: refresh model, granularity, sensitivity, quality metrics, and access method.

**Canonical IRI:** `https://schema.beckn.io/DatasetItem/v1.1`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v1.1](./v1.1/) | Current | Adds streaming transport access methods (`MQTT`, `KAFKA`, `API`, `DATA_LAKE`) and catalog-time `dataset:streamMeta`. Backward-compatible with v1.0. |
| [v1.0](./v1.0/) | Superseded | Initial release — static/recurring datasets with `INLINE`, `DOWNLOAD`, `DATA_ENCLAVE`, `OFF_CHANNEL` access methods. |

---

## Purpose

`DatasetItem` describes **what a buyer is purchasing** at catalog time: coverage (temporal, spatial, vertical), refresh behaviour, size estimates, data quality flags, and how the data will be delivered. Credentials never appear here — for streaming access methods they are provisioned post-`confirm` via [`DatasetFulfillment`](../DatasetFulfillment/).

## Usage

Attached to `Item.itemAttributes` in `on_discover` catalogs. See the version READMEs for field tables, examples, and the Beckn handshake flow.

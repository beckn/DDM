# DatasetFulfillment

Access provisioning details for a fulfilled dataset order — extending [`schema:DataDownload`](https://schema.org/DataDownload) with Beckn-specific attributes for access method, signed URLs, download windows, and (in v1.1+) stream credential delivery.

Carried as `performanceAttributes` or `fulfillmentAttributes` in beckn messages — typically on the BPP side in `on_confirm` / `on_status` once the buyer has confirmed and credentials are ready.

## Versions

| Version | Status | Highlights |
|---|---|---|
| [v1.0](./v1.0) | Stable | Base schema: `accessMethod` (5 values), signed `accessUrl`, access window (`accessStart`/`accessEnd`), download counters, support contact. |
| [v1.1](./v1.1) | Stable | Adds `streamConnection` — polymorphic credential delivery object for `MQTT`, `KAFKA`, `API`, and `DATA_LAKE` access methods. Relaxes required fields so only `accessMethod` is mandatory. Adds `credentialExpiresAt` for short-lived credential rotation via `update`. Fully backward-compatible with v1.0. |

## File layout

Each version folder contains:

- `attributes.yaml` — OpenAPI 3.1 component schema, the canonical structural definition
- `schema.json` — self-contained JSON Schema (draft 2020-12) for runtime validation
- `context.jsonld` — JSON-LD term mappings (each version inherits from the version below)
- `vocab.jsonld` — RDF property declarations
- `README.md` — version notes and examples

Cross-version concerns (namespace prefixes, class IRI mappings, `rdfs:Class` declarations) live in the parent [`schema/context.jsonld`](../context.jsonld) and [`schema/vocab.jsonld`](../vocab.jsonld) and are inherited by each version.

## Canonical URLs (after publish)

```
https://schema.beckn.io/DatasetFulfillment/v1.0/{attributes.yaml,schema.json,context.jsonld,vocab.jsonld}
https://schema.beckn.io/DatasetFulfillment/v1.1/{attributes.yaml,schema.json,context.jsonld,vocab.jsonld}
```

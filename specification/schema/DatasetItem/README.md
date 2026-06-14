# DatasetItem

A dataset product in a Beckn catalog — extending [`schema:Dataset`](https://schema.org/Dataset) with Beckn-specific attributes for refresh cadence, granularity, sensitivity, quality flags, access method, and (in v1.1+) streaming transport metadata.

Carried as `resourceAttributes`, `commitmentAttributes`, or `offerAttributes` in beckn messages where the resource being described is a dataset.

## Versions

| Version | Status | Highlights |
|---|---|---|
| [v1.0](./v1.0) | Stable | Base schema: identifier/name/temporal coverage, quality flags, four access methods (`INLINE`, `DOWNLOAD`, `DATA_ENCLAVE`, `OFF_CHANNEL`), inline `dataPayload`. |
| [v1.1](./v1.1) | Stable | Adds four streaming access methods (`MQTT`, `KAFKA`, `API`, `DATA_LAKE`) and a `dataset:streamMeta` sub-object for catalog-time stream topology metadata. Fully backward-compatible with v1.0. |

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
https://schema.beckn.io/DatasetItem/v1.0/{attributes.yaml,schema.json,context.jsonld,vocab.jsonld}
https://schema.beckn.io/DatasetItem/v1.1/{attributes.yaml,schema.json,context.jsonld,vocab.jsonld}
```

#!/usr/bin/env python3
"""
DDM Postman Collection Generator

Builds Postman collections from example JSON flows for the rain-probability devkit.
Adapted from the DEG generate_postman_collection.py script.

Usage:
  python3 scripts/generate_postman_collection.py --role BAP
  python3 scripts/generate_postman_collection.py --role BPP
"""

import json
import os
import re
import uuid
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

DEVKIT_CONFIG = {
    "domain": "nfh.global/testnet-ddm",
    "bap_id": "bap.example.com",
    "bap_uri": "http://onix-bap:8081/bap/receiver",
    "bpp_id": "bpp.example.com",
    "bpp_uri": "http://onix-bpp:8082/bpp/receiver",
    "bap_adapter_url": "http://localhost:8081/bap/caller",
    "bpp_adapter_url": "http://localhost:8082/bpp/caller",
    "examples_path": "examples/v2",
    "structure": "flat"
}

ROLE_FILTERS = {
    "BAP": [
        r".*-request.*\.json$",
        r"^(discover|select|init|confirm|status|update|track|rating|support|cancel).*\.json$",
        r"^subscribe-.*\.json$"
    ],
    "BPP": [
        r"^(?!cascaded-).*-response.*\.json$",
        r"^on[-_](discover|select|init|confirm|update|track|status|rating|support|cancel).*\.json$",
        r"^publish-.*\.json$"
    ]
}

BAP_ACTIONS = {
    "discover": "discover",
    "select": "select",
    "init": "init",
    "confirm": "confirm",
    "status": "status",
    "update": "update",
    "track": "track",
    "rating": "rating",
    "support": "support",
    "cancel": "cancel",
    "subscribe": "subscribe",
}

BPP_INITIATED_ACTIONS = {
    "publish": "publish",
}

BPP_ACTIONS = {
    "on_discover": "on_discover",
    "on_select": "on_select",
    "on_init": "on_init",
    "on_confirm": "on_confirm",
    "on_status": "on_status",
    "on_update": "on_update",
    "on_track": "on_track",
    "on_rating": "on_rating",
    "on_support": "on_support",
    "on_cancel": "on_cancel",
}

PRE_REQUEST_SCRIPT = """// Pure JS pre-request script to replace moment()
// 1) ISO 8601 timestamp without needing moment
const isoTimestamp = new Date().toISOString();
pm.collectionVariables.set('iso_date', isoTimestamp);
"""


def matches_role_filter(filename: str, role: str) -> bool:
    if role not in ROLE_FILTERS:
        return False
    for pattern in ROLE_FILTERS[role]:
        if re.match(pattern, filename, re.IGNORECASE):
            return True
    return False


def extract_action_from_filename(filename: str, role: str) -> Optional[str]:
    name = filename.replace('.json', '')

    if role == "BAP":
        if name.startswith('subscribe-'):
            return "subscribe"
        if '-request' in name and '-response' not in name:
            match = re.match(r'^([a-z]+)-request', name, re.IGNORECASE)
            if match:
                action = match.group(1)
                if action in BAP_ACTIONS:
                    return action

    elif role == "BPP":
        if name.startswith('publish-'):
            return "publish"
        if '-response' in name and '-request' not in name:
            match = re.match(r'^(on[-_])?([a-z]+)-response', name, re.IGNORECASE)
            if match:
                has_on_prefix = match.group(1) is not None
                action = match.group(2)
                if has_on_prefix:
                    bpp_action = f"on_{action}"
                    if bpp_action in BPP_ACTIONS:
                        return bpp_action
                else:
                    if action in BAP_ACTIONS:
                        return f"on_{action}"

    return None


def load_example_json(filepath: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        if "context" not in data or "message" not in data:
            return None
        return data
    except (json.JSONDecodeError, Exception):
        return None


def replace_context_macros(data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return data

    result = {}
    for key, value in data.items():
        if key == "context" and isinstance(value, dict):
            new_context = {}
            for ctx_key, ctx_value in value.items():
                if ctx_key == "version":
                    new_context[ctx_key] = "{{version}}"
                elif ctx_key in ("domain", "networkId"):
                    new_context[ctx_key] = "{{domain}}"
                elif ctx_key in ("bap_id", "bapId"):
                    new_context[ctx_key] = "{{bap_id}}"
                elif ctx_key in ("bap_uri", "bapUri"):
                    new_context[ctx_key] = "{{bap_uri}}"
                elif ctx_key in ("bpp_id", "bppId"):
                    new_context[ctx_key] = "{{bpp_id}}"
                elif ctx_key in ("bpp_uri", "bppUri"):
                    new_context[ctx_key] = "{{bpp_uri}}"
                elif ctx_key in ("transaction_id", "transactionId"):
                    new_context[ctx_key] = "{{transaction_id}}"
                elif ctx_key in ("message_id", "messageId"):
                    new_context[ctx_key] = "{{$guid}}"
                elif ctx_key == "timestamp":
                    new_context[ctx_key] = "{{iso_date}}"
                elif ctx_key in ("ttl", "action", "schema_context", "schemaContext"):
                    new_context[ctx_key] = ctx_value
                else:
                    new_context[ctx_key] = replace_context_macros(ctx_value) if isinstance(ctx_value, (dict, list)) else ctx_value
            result[key] = new_context
        elif isinstance(value, dict):
            result[key] = replace_context_macros(value)
        elif isinstance(value, list):
            result[key] = [replace_context_macros(item) if isinstance(item, dict) else item for item in value]
        else:
            result[key] = value

    return result


def create_postman_request(json_data, action, endpoint, request_name, adapter_url_var):
    request_body = replace_context_macros(json_data)
    body_raw = json.dumps(request_body, indent=2)

    return {
        "name": request_name,
        "request": {
            "method": "POST",
            "header": [],
            "body": {
                "mode": "raw",
                "raw": body_raw,
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            },
            "url": {
                "raw": f"{{{{{adapter_url_var}}}}}/{endpoint}",
                "host": [f"{{{{{adapter_url_var}}}}}"],
                "path": [endpoint]
            },
            "description": f"{action.capitalize()} request: {request_name}"
        },
        "response": []
    }


def scan_examples(examples_dir: Path, role: str) -> Dict[str, List[Tuple[Path, str]]]:
    actions_map = {}
    if not examples_dir.exists():
        print(f"Error: Examples directory not found: {examples_dir}")
        return actions_map

    for json_file in sorted(examples_dir.glob("*.json")):
        if not matches_role_filter(json_file.name, role):
            continue
        action = extract_action_from_filename(json_file.name, role)
        if action is None:
            continue
        request_name = json_file.name.replace('.json', '')
        if action not in actions_map:
            actions_map[action] = []
        actions_map[action].append((json_file, request_name))

    for action, files in actions_map.items():
        print(f"  Found {len(files)} example(s) for action '{action}'")

    return actions_map


def generate_collection(role: str, repo_root: Path):
    config = DEVKIT_CONFIG
    examples_dir = repo_root / config["examples_path"]

    if role == "BAP":
        action_mapping = BAP_ACTIONS
        adapter_url_var = "bap_adapter_url"
        collection_name = "rain-probability.BAP-DDM"
        desc = "Postman collection for Buyer Application Platform implementing rain-probability DDM APIs based on Beckn Protocol v2"
    else:
        action_mapping = {**BPP_ACTIONS, **BPP_INITIATED_ACTIONS}
        adapter_url_var = "bpp_adapter_url"
        collection_name = "rain-probability.BPP-DDM"
        desc = "Postman collection for Buyer Provider Platform implementing rain-probability DDM APIs based on Beckn Protocol v2"

    print(f"Scanning examples: {examples_dir}")
    print(f"Role: {role}")

    actions_map = scan_examples(examples_dir, role)
    if not actions_map:
        print("No valid examples found.")
        return

    collection_items = []
    all_actions = sorted(set(list(actions_map.keys()) + list(action_mapping.keys())))

    for action in all_actions:
        if action not in action_mapping:
            continue
        endpoint = action_mapping[action]
        files_list = actions_map.get(action, [])

        action_items = []
        for json_file, request_name in sorted(files_list):
            json_data = load_example_json(json_file)
            if json_data is None:
                continue
            request = create_postman_request(json_data, action, endpoint, request_name, adapter_url_var)
            action_items.append(request)

        if action_items:
            collection_items.append({"name": action, "item": action_items})
            print(f"  Created folder '{action}' with {len(action_items)} request(s)")

    variables = [
        {"key": "domain", "value": config["domain"]},
        {"key": "version", "value": "2.0.0"},
        {"key": "bap_id", "value": config["bap_id"]},
        {"key": "bap_uri", "value": config["bap_uri"]},
        {"key": "bpp_id", "value": config["bpp_id"]},
        {"key": "bpp_uri", "value": config["bpp_uri"]},
        {"key": "transaction_id", "value": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002"},
        {"key": "iso_date", "value": ""},
    ]
    if role == "BAP":
        variables.append({"key": "bap_adapter_url", "value": config["bap_adapter_url"]})
    else:
        variables.append({"key": "bpp_adapter_url", "value": config["bpp_adapter_url"]})

    collection = {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": collection_name,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "description": desc
        },
        "item": collection_items,
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": PRE_REQUEST_SCRIPT.split("\n")
                }
            }
        ],
        "variable": variables
    }

    output_dir = repo_root / "postman"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{collection_name}.postman_collection.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

    total_requests = sum(len(item['item']) for item in collection_items)
    print(f"\nGenerated: {output_path}")
    print(f"  Folders: {len(collection_items)}, Requests: {total_requests}")


def main():
    parser = argparse.ArgumentParser(description="Generate Postman collection from DDM example JSONs")
    parser.add_argument("--role", type=str, choices=["BAP", "BPP"], required=True, help="Role: BAP or BPP")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    generate_collection(args.role, repo_root)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check AMM GraphQL server compatibility with AMM_web client queries."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    skipped: bool = False


def gql_request(
    url: str,
    query: str,
    variables: dict[str, Any] | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with httpx.Client(timeout=20.0) as client:
        resp = client.post(
            url,
            json={"query": query, "variables": variables or {}},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()


def run_check(
    *,
    name: str,
    url: str,
    query: str,
    variables: dict[str, Any] | None = None,
    token: str | None = None,
    required_data_key: str | None = None,
    skip_reason: str | None = None,
) -> CheckResult:
    if skip_reason:
        return CheckResult(name=name, ok=True, detail=skip_reason, skipped=True)
    try:
        data = gql_request(url, query, variables=variables, token=token)
    except Exception as exc:
        return CheckResult(name=name, ok=False, detail=str(exc))
    errors = data.get("errors")
    if errors:
        return CheckResult(name=name, ok=False, detail=errors[0].get("message", "GraphQL error"))
    if required_data_key is not None:
        payload = data.get("data") or {}
        if required_data_key not in payload:
            return CheckResult(
                name=name,
                ok=False,
                detail=f"Missing data field '{required_data_key}'",
            )
    return CheckResult(name=name, ok=True, detail="ok")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AMM_core GraphQL compatibility for AMM_web")
    parser.add_argument(
        "--url",
        default=os.getenv("AMM_GRAPHQL_URL", "http://127.0.0.1:8000/graphql"),
        help="GraphQL endpoint URL",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("AMM_ACCESS_TOKEN", ""),
        help="Bearer token for auth-only checks",
    )
    parser.add_argument(
        "--show-json",
        action="store_true",
        help="Output JSON summary in addition to human-readable status",
    )
    args = parser.parse_args()

    token = args.token or None
    checks = [
        run_check(
            name="health.__typename",
            url=args.url,
            query="query ServerHealth { __typename }",
            required_data_key="__typename",
        ),
        run_check(
            name="query.getTracks",
            url=args.url,
            query=(
                "query GetTracks($limit: Int!, $offset: Int!) { "
                "getTracks(limit: $limit, offset: $offset) { total items { id title } } }"
            ),
            variables={"limit": 3, "offset": 0},
            required_data_key="getTracks",
        ),
        run_check(
            name="query.getAlbums",
            url=args.url,
            query=(
                "query GetAlbums($limit: Int!, $offset: Int!) { "
                "getAlbums(limit: $limit, offset: $offset) { total items { id title } } }"
            ),
            variables={"limit": 3, "offset": 0},
            required_data_key="getAlbums",
        ),
        run_check(
            name="query.getTrack",
            url=args.url,
            query="query GetTrack($trackId: Int!) { getTrack(trackId: $trackId) { id title } }",
            variables={"trackId": 1},
            required_data_key="getTrack",
        ),
        run_check(
            name="query.getPersons",
            url=args.url,
            query=(
                "query GetPersons($limit: Int!, $offset: Int!) { "
                "getPersons(limit: $limit, offset: $offset) { total items { id fullName } } }"
            ),
            variables={"limit": 3, "offset": 0},
            required_data_key="getPersons",
        ),
        run_check(
            name="query.getLabels",
            url=args.url,
            query=(
                "query GetLabels($limit: Int!, $offset: Int!) { "
                "getLabels(limit: $limit, offset: $offset) { total items { id name } } }"
            ),
            variables={"limit": 3, "offset": 0},
            required_data_key="getLabels",
        ),
        run_check(
            name="query.playlists",
            url=args.url,
            query="query Playlists { playlists { id name trackIds } }",
            token=token,
            required_data_key="playlists",
            skip_reason=None if token else "skipped (no token)",
        ),
        run_check(
            name="query.queue",
            url=args.url,
            query="query Queue { queue { trackIds } }",
            token=token,
            required_data_key="queue",
            skip_reason=None if token else "skipped (no token)",
        ),
    ]

    ok_count = 0
    fail_count = 0
    skip_count = 0

    for result in checks:
        if result.skipped:
            skip_count += 1
            print(f"SKIP  {result.name}: {result.detail}")
            continue
        if result.ok:
            ok_count += 1
            print(f"PASS  {result.name}")
            continue
        fail_count += 1
        print(f"FAIL  {result.name}: {result.detail}")

    print(f"\nSummary: {ok_count} passed, {fail_count} failed, {skip_count} skipped")

    if args.show_json:
        print(
            json.dumps(
                {
                    "url": args.url,
                    "passed": ok_count,
                    "failed": fail_count,
                    "skipped": skip_count,
                    "results": [result.__dict__ for result in checks],
                },
                indent=2,
            )
        )

    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())


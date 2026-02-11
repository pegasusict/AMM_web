# Audiophiles' Music Manager - AMM

## Web based client

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7dccd15d9b7e468ea76696ea5fe39d66)](https://app.codacy.com/gh/pegasusict/AMM_web/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

__AMM__ is a music management system for very large collections.

It has the following processing capabilities:

* Importing / Parsing
* Fingerprinting
* Silence Trimming
* Converting
* Tag Retrieval
* Art Retrieval
* Lyrics Retrieval
* Tagging
* Renaming / Sorting
* exporting

## Modules

|Module     |Description                |Progress |
|-----------|---------------------------|--------:|
|Core       |Server                     |     90% |
|API Client |API client Interface       |    100% |
|Web        |Web Interface              |     10% |
|TUI        |CLI/Textual User Interface | planned |
|GUI        |Graphical Client           | planned |
|Mobile     |Mobile Client              | planned |

## user login via google oauth, admin approved registration

## Per-user playback

The system has a icecast like playbacksystem which works on a per-user basis.

## Planned capabilities

audiobook support?
crossfading

## Client Connectivity Helpers

- Offline/mock mode for AMM_web:
  - `export AMM_OFFLINE_MODE=1`
  - This lets login/dashboard/search run without a live server.
- GraphQL endpoint override:
  - `export AMM_GRAPHQL_URL=http://127.0.0.1:8000/graphql`

## Server Contract Checklist

Run the integration checks once AMM_core is running:

```bash
.venv/bin/python scripts/server_contract_check.py --url http://127.0.0.1:8000/graphql
```

Include auth-only checks (playlists/queue) with a token:

```bash
AMM_ACCESS_TOKEN="<jwt>" .venv/bin/python scripts/server_contract_check.py
```

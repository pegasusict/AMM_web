from typing import Optional


def graphql_query_script(query: str, variables: Optional[dict] = None) -> str:
    """Return a JS call to graphqlRequest(query, variables)."""
    import json

    variables = variables or {}
    q = json.dumps(query)
    v = json.dumps(variables)
    return f"graphqlRequest({q}, {v})"

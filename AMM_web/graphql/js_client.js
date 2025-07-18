export async function graphqlRequest(query, variables = {}) {
    let token = localStorage.getItem("auth_token");

    const headers = {
      "Content-Type": "application/json",
      "Authorization": token ? `Bearer ${token}` : ""
    };

    let res = await fetch("http://localhost:8000/graphql", {
      method: "POST",
      headers,
      body: JSON.stringify({ query, variables }),
      credentials: "include",  // needed for refresh cookies
    });

    // If token expired, try refresh once
    if (res.status === 401) {
      const refresh = await fetch("http://localhost:8000/auth/refresh", {
        method: "POST",
        credentials: "include"
      });

      if (refresh.ok) {
        const data = await refresh.json();
        localStorage.setItem("auth_token", data.access_token);

        // Retry the original GraphQL request
        headers["Authorization"] = `Bearer ${data.access_token}`;
        res = await fetch("http://localhost:8000/graphql", {
          method: "POST",
          headers,
          body: JSON.stringify({ query, variables }),
          credentials: "include",
        });
      } else {
        window.location.href = "/login";
      }
    }

    return await res.json();
}

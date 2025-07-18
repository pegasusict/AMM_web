export async function get_access_token() {
    let token = localStorage.getItem("auth_token");

    // If missing, try refresh
    if (!token) {
        const res = await fetch("http://localhost:8000/auth/refresh", {
            method: "POST",
            credentials: "include",
        });

        if (res.ok) {
            const data = await res.json();
            localStorage.setItem("auth_token", data.access_token);
            return data.access_token;
        } else {
            window.location.href = "/login";
            return null;
        }
    }

    return token;
}

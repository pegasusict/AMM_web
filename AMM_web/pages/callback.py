import reflex as rx


def callback():
    return rx.script("""
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    if (token) {
        localStorage.setItem("auth_token", token);
        window.location.href = "/";
    } else {
        alert("Login failed");
        window.location.href = "/login";
    }
    """)

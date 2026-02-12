const API_URL = "http://127.0.0.1:8000";

function getToken() {
    return sessionStorage.getItem("access_token");
}

async function apiRequest(endpoint, method = "GET", data = null) {
    const token = getToken();

    const options = {
        method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    const res = await fetch(API_URL + endpoint, options);

    if (!res.ok) {
        const text = await res.text();
        console.error("API error:", text);
        throw new Error(text);
    }

    return res.json();
}
document.querySelector(".menu-btn")?.addEventListener("click", () => {
    document.querySelector(".nav-links")?.classList.toggle("show");
});

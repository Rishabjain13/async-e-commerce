async function login(e) {
    e.preventDefault();

    const emailEl = document.getElementById("emailInput");
    const passwordEl = document.getElementById("passwordInput");

    if (!emailEl || !passwordEl) {
        alert("Login form not found");
        return;
    }

    const email = emailEl.value.trim();
    const password = passwordEl.value.trim();

    try {
        const res = await apiRequest("/auth/login", "POST", {
            email,
            password
        });

        // Store token in sessionStorage
        sessionStorage.setItem("access_token", res.access_token);

        // Redirect to home
        window.location.href = "index.html";
    } catch (err) {
        console.error(err);
        alert("Login failed");
    }
}

async function register(e) {
    e.preventDefault();

    const emailEl = document.getElementById("emailInput");
    const passwordEl = document.getElementById("passwordInput");

    if (!emailEl || !passwordEl) {
        alert("Registration form not found");
        return;
    }

    const email = emailEl.value.trim();
    const password = passwordEl.value.trim();

    try {
        await apiRequest("/auth/register", "POST", {
            email,
            password
        });

        alert("Registration successful");
        window.location.href = "login.html";
    } catch (err) {
        console.error(err);
        alert("Registration failed");
    }
}
function logout(e) {
    if (e) e.preventDefault();
    sessionStorage.removeItem("access_token");
    window.location.href = "login.html";
}

function updateNavbar() {
    const token = sessionStorage.getItem("access_token");
    const loginLink = document.getElementById("loginLink");
    const adminLink = document.querySelector('a[href="admin.html"]');

    if (!token) return;

    const payload = JSON.parse(atob(token.split('.')[1]));
    const role = payload.role;

    // Change Login to Logout
    if (loginLink) {
        loginLink.textContent = "Logout";
        loginLink.onclick = logout;
    }

    // Hide admin link if not admin
    if (adminLink && role !== "admin") {
        adminLink.style.display = "none";
    }
}


document.addEventListener("DOMContentLoaded", updateNavbar);

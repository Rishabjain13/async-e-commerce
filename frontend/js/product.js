let currentPage = 1;
const limit = 8;
let allProducts = [];
let currentSearch = "";

async function loadProducts() {
    try {
        const products = await apiRequest("/products");
        allProducts = products;

        renderProducts();
        loadCartCount();
    } catch (err) {
        console.error("Failed to load products:", err);
    }
}

function renderProducts() {
    const container = document.getElementById("products");
    container.innerHTML = "";

    const filtered = allProducts.filter(p =>
        p.product?.name
            ?.toLowerCase()
            .includes(currentSearch.toLowerCase())
    );

    filtered.forEach(p => {
        const name = p.product?.name || "Unnamed product";
        const description = p.product?.description || "No description";
        const price = p.price ?? 0;
        const rating = p.rating ?? 0;

        const variant = p.variants?.[0];
        const variantId = variant?.id || null;

        const div = document.createElement("div");
        div.className = "product";
        div.innerHTML = `
            <h3>${name}</h3>
            <p>${description}</p>
            <p class="price">₹${price}</p>
            <p class="rating">⭐ ${rating}</p>
            <button onclick="addToCart(${variantId})"
                ${!variantId ? "disabled" : ""}>
                Add to Cart
            </button>
        `;
        container.appendChild(div);
    });

    if (filtered.length === 0) {
        container.innerHTML = "<p>No products found</p>";
    }
}

function searchProducts() {
    const input = document.getElementById("searchInput");
    currentSearch = input.value.trim();
    renderProducts();
}

function nextPage() {
    currentPage++;
    loadProducts();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        loadProducts();
    }
}

async function addToCart(variantId) {
    try {
        const token = sessionStorage.getItem("access_token");

        if (!token) {
            alert("Please login first");
            window.location.href = "login.html";
            return;
        }

        await apiRequest("/cart/items", "POST", {
            variant_id: variantId,
            quantity: 1
        });

        alert("Added to cart");
        loadCartCount();
    } catch (err) {
        console.error(err);
        alert("Failed to add to cart");
    }
}

loadProducts();

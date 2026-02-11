function requireAuth() {
    const token = sessionStorage.getItem("access_token");
    if (!token) {
        window.location.href = "login.html";
    }
}

requireAuth();

function requireAdmin() {
    const token = sessionStorage.getItem("access_token");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));

    if (payload.role !== "admin") {
        alert("Access denied");
        window.location.href = "index.html";
    }
}

requireAdmin();

/* ---------------- PRODUCT CREATION ---------------- */

document.getElementById("productForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
        const productData = {
            name: document.getElementById("name").value,
            description: document.getElementById("description").value,
            price: parseFloat(document.getElementById("price").value),
            rating: parseFloat(document.getElementById("rating").value) || 0,
            variants: [
                {
                    sku: document.getElementById("sku").value,
                    attributes: {
                        additionalProp1: document.getElementById("attr1").value,
                        additionalProp2: document.getElementById("attr2").value,
                        additionalProp3: document.getElementById("attr3").value
                    },
                    quantity: parseInt(document.getElementById("quantity").value),
                    in_stock: true
                }
            ]
        };


        await apiRequest("/admin/products", "POST", productData);

        alert("Product created successfully");
        document.getElementById("productForm").reset();
    } catch (err) {
        console.error(err);
        alert("Failed to create product");
    }
});

/* ---------------- ADMIN STATS ---------------- */
async function loadStats() {
    try {
        const stats = await apiRequest("/admin/stats");

        document.getElementById("statProducts").innerText =
            stats.total_products ?? 0;

        document.getElementById("statOrders").innerText =
            stats.total_orders ?? 0;

        document.getElementById("statRevenue").innerText =
            "₹" + (stats.total_revenue ?? 0);

    } catch (err) {
        console.error("Stats load failed", err);
    }
}



/* ---------------- ADMIN ORDERS ---------------- */
async function loadOrders() {
    try {
        const orders = await apiRequest("/admin/orders");

        const tbody = document.querySelector("#ordersTable tbody");
        tbody.innerHTML = "";

        orders.forEach(o => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${o.id}</td>
                <td>${o.user_id}</td>
                <td>${o.status}</td>
                <td>
                    <button onclick="updateStatus(${o.id}, 'shipped')">
                        Mark Shipped
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("Failed to load orders", err);
    }
}
async function updateStatus(orderId, status) {
    try {
        await apiRequest(`/admin/orders/${orderId}`, "PUT", {
            status: status
        });
        loadOrders();
    } catch (err) {
        alert("Failed to update status");
    }
}


/* ---------------- LOAD PRODUCTS ---------------- */
async function loadProducts() {
    try {
        const products = await apiRequest("/products");

        const tbody = document.querySelector("#productsTable tbody");
        tbody.innerHTML = "";

        products.forEach(p => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${p.product.id}</td>
                <td class="name">${p.product.name}</td>
                <td class="price">₹${p.price}</td>
                <td>
                    <button onclick="editProduct(${p.product.id}, this)">
                        Edit
                    </button>
                    <button onclick="deleteProduct(${p.product.id})">
                        Delete
                    </button>
                </td>
            `;

            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("Failed to load products", err);
    }
}
function editProduct(id, btn) {
    const row = btn.closest("tr");
    const nameCell = row.querySelector(".name");
    const priceCell = row.querySelector(".price");

    const name = nameCell.innerText;
    const price = priceCell.innerText.replace("₹", "");

    nameCell.innerHTML = `<input id="edit-name-${id}" value="${name}">`;
    priceCell.innerHTML = `<input id="edit-price-${id}" value="${price}">`;

    btn.textContent = "Save";
    btn.onclick = () => saveProduct(id, row);
}

async function saveProduct(id, row) {
    const name = document.getElementById(`edit-name-${id}`).value;
    const price = document.getElementById(`edit-price-${id}`).value;

    try {
        await apiRequest(`/admin/products/${id}`, "PUT", {
            name,
            price
        });

        alert("Product updated");
        loadProducts();
    } catch (err) {
        console.error(err);
        alert("Update failed");
    }
}

async function deleteProduct(id) {
    if (!confirm("Delete this product?")) return;

    try {
        await apiRequest(`/admin/products/${id}`, "DELETE");
        loadProducts();
    } catch (err) {
        console.error(err);
        alert("Delete failed");
    }
}

loadProducts();
loadOrders();

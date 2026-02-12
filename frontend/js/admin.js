/* ================= AUTH ================= */

function requireAuth() {
    const token = sessionStorage.getItem("access_token");
    if (!token) window.location.href = "login.html";
}

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

requireAuth();
requireAdmin();

/* ================= GLOBAL STATE ================= */

let editMode = false;
let editingProductId = null;

/* ================= FORM SUBMIT (ADD + EDIT) ================= */

document.getElementById("productForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

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
                quantity: parseInt(document.getElementById("quantity").value)
            }
        ]
    };

    try {

        if (!editMode) {
            // 🟢 ADD PRODUCT
            await apiRequest("/admin/products", "POST", productData);
            alert("Product created successfully");
        } else {
            // 🔵 UPDATE PRODUCT
            await apiRequest(`/admin/products/${editingProductId}`, "PUT", productData);
            alert("Product updated successfully");
        }

        resetForm();
        loadProducts();

    } catch (err) {
        console.error(err);
        alert("Operation failed");
    }
});

/* ================= EDIT MODE ================= */

window.editProduct = async function (id) {

    try {
        const data = await apiRequest(`/products/${id}`);

        document.getElementById("name").value = data.product.name || "";
        document.getElementById("description").value = data.product.description || "";
        document.getElementById("price").value = data.price || "";
        document.getElementById("rating").value = data.rating || 0;

        if (data.variants.length > 0) {
            const v = data.variants[0];

            document.getElementById("sku").value = v.sku || "";
            document.getElementById("quantity").value = v.quantity || 0;

            document.getElementById("attr1").value = v.attributes?.additionalProp1 || "";
            document.getElementById("attr2").value = v.attributes?.additionalProp2 || "";
            document.getElementById("attr3").value = v.attributes?.additionalProp3 || "";
        }

        // Switch to edit mode
        editMode = true;
        editingProductId = id;

        document.querySelector(".admin-card h3").textContent = "Edit Product";
        document.querySelector("#productForm button").textContent = "Update Product";

        window.scrollTo({ top: 0, behavior: "smooth" });

    } catch (err) {
        console.error("Edit failed:", err);
        alert("Failed to load product");
    }
};

/* ================= RESET FORM ================= */

function resetForm() {

    document.getElementById("productForm").reset();

    editMode = false;
    editingProductId = null;

    document.querySelector(".admin-card h3").textContent = "Add Product";
    document.querySelector("#productForm button").textContent = "Create Product";
}

/* ================= LOAD PRODUCTS ================= */

async function loadProducts() {
    try {
        const products = await apiRequest("/products");

        const tbody = document.querySelector("#productsTable tbody");
        tbody.innerHTML = "";

        products.forEach(p => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${p.product.id}</td>
                <td>${p.product.name}</td>
                <td>₹${p.price}</td>
                <td>
                    <button onclick="editProduct(${p.product.id})">
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

/* ================= DELETE PRODUCT ================= */

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

/* ================= ADMIN STATS ================= */

async function loadStats() {
    try {
        const stats = await apiRequest("/admin/stats");

        document.getElementById("statProducts").innerText = stats.total_products ?? 0;
        document.getElementById("statOrders").innerText = stats.total_orders ?? 0;
        document.getElementById("statRevenue").innerText = "₹" + (stats.total_revenue ?? 0);

    } catch (err) {
        console.error("Stats load failed", err);
    }
}

/* ================= ADMIN ORDERS ================= */

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
        await apiRequest(`/admin/orders/${orderId}`, "PUT", { status });
        loadOrders();
    } catch {
        alert("Failed to update status");
    }
}

/* ================= INIT ================= */

document.addEventListener("DOMContentLoaded", () => {
    loadProducts();
    loadOrders();
});

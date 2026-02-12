function requireAuth() {
    const token = sessionStorage.getItem("access_token");
    if (!token) {
        window.location.href = "login.html";
    }
}

requireAuth();

async function loadOrders() {
    try {
        const response = await apiRequest("/orders/");

        // ✅ Normalize API response
        const orders = Array.isArray(response)
            ? response
            : response.data || response.orders || [];

        const table = document.getElementById("ordersTable");
        const tbody = table.querySelector("tbody");
        const container = document.querySelector(".container");

        // Cleanup
        tbody.innerHTML = "";
        container.querySelectorAll(".mobile-card").forEach(e => e.remove());
        table.style.display = "table";

        if (orders.length === 0) {
            tbody.innerHTML = "<tr><td colspan='3'>No orders yet</td></tr>";
            return;
        }

        // 📱 Mobile view → cards
        if (window.innerWidth <= 600) {
            table.style.display = "none";

            orders.forEach(o => {
                const card = document.createElement("div");
                card.className = "mobile-card";
                card.innerHTML = `
                    <strong>Order #${o.id}</strong>
                    <p>Status: ${o.status}</p>
                    <button onclick="toggleItems(${o.id}, this)">
                        View Items
                    </button>
                    <div id="items-container-${o.id}" style="display:none">
                        Loading...
                    </div>
                `;
                container.appendChild(card);
            });

            return;
        }

        // 💻 Desktop / Tablet → table
        orders.forEach(o => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${o.id}</td>
                <td>${o.status}</td>
                <td>
                    <button onclick="toggleItems(${o.id}, this)">
                        View Items
                    </button>
                </td>
            `;
            tbody.appendChild(row);

            const detailRow = document.createElement("tr");
            detailRow.id = `items-${o.id}`;
            detailRow.style.display = "none";
            detailRow.innerHTML = `
                <td colspan="3">
                    <div id="items-container-${o.id}">
                        Loading...
                    </div>
                </td>
            `;
            tbody.appendChild(detailRow);
        });

    } catch (err) {
        console.error("Failed to load orders", err);
    }
}

async function toggleItems(orderId, btn) {
    let container = document.getElementById(`items-container-${orderId}`);
    let detailRow = document.getElementById(`items-${orderId}`);

    const isMobile = window.innerWidth <= 600;

    // Toggle visibility
    if (isMobile) {
        const visible = container.style.display === "block";
        container.style.display = visible ? "none" : "block";
        btn.innerText = visible ? "View Items" : "Hide Items";
        if (visible) return;
    } else {
        const open = detailRow.style.display === "table-row";
        detailRow.style.display = open ? "none" : "table-row";
        btn.innerText = open ? "View Items" : "Hide Items";
        if (open) return;
    }

    try {
        const response = await apiRequest(`/orders/${orderId}`);
        const order = response.data || response;

        const items = order.items || [];

        if (items.length === 0) {
            container.innerHTML = "No items found";
            return;
        }

        // 📱 Mobile items
        if (isMobile) {
            container.innerHTML = items.map(i => `
                <div class="mobile-card">
                    <strong>${i.product_name}</strong>
                    <p>Qty: ${i.quantity}</p>
                    <p>₹${i.price}</p>
                </div>
            `).join("") + `
                <div class="mobile-card">
                    <strong>Total: ₹${order.total_amount}</strong>
                </div>
            `;
            return;
        }

        // 💻 Desktop items
        let html = `
            <div class="table-wrapper">
                <table class="table">
                    <tr>
                        <th>Product</th>
                        <th>Qty</th>
                        <th>Price</th>
                    </tr>
        `;

        items.forEach(i => {
            html += `
                <tr>
                    <td>${i.product_name}</td>
                    <td>${i.quantity}</td>
                    <td>₹${i.price}</td>
                </tr>
            `;
        });

        html += `
                <tr>
                    <td colspan="2"><strong>Total</strong></td>
                    <td><strong>₹${order.total_amount}</strong></td>
                </tr>
                </table>
            </div>
        `;

        container.innerHTML = html;

    } catch (err) {
        container.innerHTML = "Failed to load items";
        console.error(err);
    }
}

// Reload on resize so layout stays correct
window.addEventListener("resize", () => {
    loadOrders();
});

loadOrders();

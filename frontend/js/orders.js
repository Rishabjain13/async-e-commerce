function requireAuth() {
    const token = sessionStorage.getItem("access_token");
    if (!token) {
        window.location.href = "login.html";
    }
}

requireAuth();

async function loadOrders() {
    try {
        const orders = await apiRequest("/orders/");

        const tbody = document.querySelector("#ordersTable tbody");
        tbody.innerHTML = "";

        if (!orders || orders.length === 0) {
            tbody.innerHTML = "<tr><td colspan='3'>No orders yet</td></tr>";
            return;
        }

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

            // hidden row for items
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
    const row = document.getElementById(`items-${orderId}`);
    const container = document.getElementById(`items-container-${orderId}`);

    if (row.style.display === "none") {
        row.style.display = "table-row";
        btn.innerText = "Hide Items";

        try {
            const order = await apiRequest(`/orders/${orderId}`);

            let html = `
                <table class="table">
                    <tr>
                        <th>Product</th>
                        <th>Qty</th>
                        <th>Price</th>
                    </tr>
            `;

            order.items.forEach(i => {
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
            `;

            html += "</table>";
            container.innerHTML = html;

        } catch (err) {
            container.innerHTML = "Failed to load items";
        }
    } else {
        row.style.display = "none";
        btn.innerText = "View Items";
    }
}


loadOrders();

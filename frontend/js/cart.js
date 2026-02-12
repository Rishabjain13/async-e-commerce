function requireAuth() {
    const token = sessionStorage.getItem("access_token");
    if (!token) {
        window.location.href = "login.html";
    }
}

async function loadCart() {
    requireAuth();

    try {
        const cart = await apiRequest("/cart/");
        const items = cart.items || [];

        const tbody = document.querySelector("#cartTable tbody");
        tbody.innerHTML = "";

        if (items.length === 0) {
            tbody.innerHTML = "<tr><td colspan='4'>Cart is empty</td></tr>";
            return;
        }

        items.forEach(i => {
            const name = i.product?.name || "Product";
            const price = i.price || 0;
            const quantity = i.quantity || 1;

            // 📱 Mobile
            if (window.innerWidth <= 600) {
                const card = document.createElement("div");
                card.className = "mobile-card";
                card.innerHTML = `
                    <strong>${name}</strong>
                    <p>Qty: ${quantity}</p>
                    <p>₹${price}</p>
                    <button onclick="removeItem(${i.item_id})">Remove</button>
                `;
                tbody.parentElement.appendChild(card);
                return;
            }

            // 💻 Desktop
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${name}</td>
                <td>
                    <button onclick="changeQuantity(${i.item_id}, ${quantity - 1})">−</button>
                    <span style="margin: 0 10px;">${quantity}</span>
                    <button onclick="changeQuantity(${i.item_id}, ${quantity + 1})">+</button>
                </td>
                <td>₹${price}</td>
                <td>
                    <button onclick="removeItem(${i.item_id})">Remove</button>
                </td>
            `;
            tbody.appendChild(row);
        });


    } catch (err) {
        console.error("Cart load failed:", err);
    }
}

async function updateQuantity(id, quantity) {
    await apiRequest(`/cart/${id}`, "PUT", {
        quantity: Number(quantity)
    });
    loadCart();
}
async function changeQuantity(id, newQty) {
    if (newQty < 1) return;

    try {
        await apiRequest(`/cart/items/${id}`, "PUT", {
            quantity: newQty
        });
        loadCart();
    } catch (err) {
        console.error(err);
    }
}


async function removeItem(id) {
    try {
        await apiRequest(`/cart/items/${id}`, "DELETE");
        loadCart();
    } catch (err) {
        console.error(err);
        alert("Failed to remove item");
    }
}

async function checkout() {
    try {
        await apiRequest("/orders/", "POST");
        alert("Order placed successfully!");
        loadCart();
    } catch {
        alert("Checkout failed");
    }
}

loadCart();

// Cart data structure in localStorage
let cart = {
    items: [], // Array of products
    count: 0   // Total number of items
};

// Initialize cart from localStorage
function initCart() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
    updateCartCounter();
    updateOrderSummary(); // Add this to update summary on init
}

// Save cart to localStorage
function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter();
    updateOrderSummary(); // Add this to update summary on save
}

// Update cart counter in UI
function updateCartCounter() {
    const counter = document.getElementById('shopping-contador');
    if (counter) {
        counter.textContent = cart.count;
    }
}

// Add product to cart
function agregarAlCarro(productId) {
    const existingItem = cart.items.find(item => item.id === productId);
    
    const productElement = document.getElementById(`producto-${productId}`);
    const productData = {
        id: productId,
        nombre: productElement.querySelector('h2').textContent,
        marca: productElement.querySelector('h1').textContent,
        precio: parseInt(productElement.querySelector('h3').textContent.replace('$', '')),
        imagen: productElement.querySelector('img').src,
        cantidad: 1
    };

    if (existingItem) {
        if (existingItem.cantidad < 100) {
            existingItem.cantidad++;
            existingItem.precioTotal = existingItem.precio * existingItem.cantidad;
            cart.count++;
        }
    } else {
        productData.precioTotal = productData.precio;
        cart.items.push(productData);
        cart.count++;
    }

    saveCart();
    actualizarOffcanvas();
    updateOrderSummary(); // Add this to update summary when adding items
}

// Update offcanvas cart display
function actualizarOffcanvas() {
    const container = document.getElementById('d-products');
    if (!container) return;

    container.innerHTML = '';
    let totalCart = 0;

    if (cart.items.length === 0) {
        container.innerHTML = '<div class="offcanva-msg">Tu carrito está vacío</div>';
        return;
    }

    cart.items.forEach(item => {
        const productHTML = `
            <div class="product">
                <div class="product-container">
                    <div class="product-desc">
                        <h2>${item.nombre}</h2>
                        <img src="${item.imagen}" alt="Producto">
                        <button onclick="eliminarDelCarro(${item.id})" class="product-remove">Eliminar</button>
                    </div>
                    <div class="product-desc-2">
                        <div class="product-price">
                            <span class="precio">Precio:</span>
                            <span class="precio-2">$${item.precioTotal}</span>
                        </div>
                        <div class="product-add">
                            <button onclick="actualizarCantidad(${item.id}, -1)" class="product-menos">-</button>
                            <span class="product-contador">${item.cantidad}</span>
                            <button onclick="actualizarCantidad(${item.id}, 1)" class="product-mas">+</button>
                        </div>
                    </div>
                </div>
                <hr>
            </div>`;

        container.insertAdjacentHTML('beforeend', productHTML);
        totalCart += item.precioTotal;
    });

    const totalElement = document.getElementById('producto-total');
    if (totalElement) {
        totalElement.textContent = `Total a pagar: $${totalCart}`;
    }
}

// Update order summary display
function updateOrderSummary() {
    const container = document.getElementById('productos-container');
    const totalElement = document.getElementById('resumen-total');
    
    if (!container || !totalElement) return;

    container.innerHTML = '';
    let totalCart = 0;

    cart.items.forEach(item => {
        const productHTML = `
            <div class="producto-r">
                <div class="product-desc">
                    <h3>${item.nombre}</h3>
                    <img src="${item.imagen}" alt="Producto">
                </div>
                <div class="product-desc-2">
                    <div class="product-price">
                        <span class="precio">Precio:</span>
                        <span class="precio-2">$${item.precioTotal}</span>
                    </div>
                    <div class="product-count">
                        <span class="product-condesc">Cantidad:</span>
                        <span class="product-contador">${item.cantidad}</span>
                    </div>
                </div>
                <hr>
            </div>`;

        container.insertAdjacentHTML('beforeend', productHTML);
        totalCart += item.precioTotal;
    });

    totalElement.textContent = `$${totalCart}`;
}

// Update item quantity
function actualizarCantidad(productId, change) {
    const item = cart.items.find(item => item.id === productId);
    if (!item) return;

    const newQuantity = item.cantidad + change;
    if (newQuantity >= 1 && newQuantity <= 100) {
        item.cantidad = newQuantity;
        item.precioTotal = item.precio * newQuantity;
        cart.count += change;
        saveCart();
        actualizarOffcanvas();
        updateOrderSummary(); // Add this to update summary when changing quantity
    }
}

// Remove item from cart
function eliminarDelCarro(productId) {
    const index = cart.items.findIndex(item => item.id === productId);
    if (index !== -1) {
        cart.count -= cart.items[index].cantidad;
        cart.items.splice(index, 1);
        saveCart();
        actualizarOffcanvas();
        updateOrderSummary(); // Add this to update summary when removing items
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initCart();
    
    // Update offcanvas when it's opened
    const offcanvas = document.getElementById('offcanvasRight');
    if (offcanvas) {
        offcanvas.addEventListener('show.bs.offcanvas', actualizarOffcanvas);
    }
});

// Validate and handle payment steps
async function validaPasos(paso) {
    switch (paso) {
        case 1:
            if (validaPaso1()) {
                // Ocultar el paso 1 y mostrar el paso 2
                document.getElementById('paso-compra-1').hidden = true;
                document.getElementById('paso-compra-2').hidden = false;
                document.getElementById("title-paso").textContent = "Método de entrega";
            }
            break;
        case 2:
            if (validaPaso2()) {
                // Ocultar el paso 2 y mostrar el paso 3
                document.getElementById('paso-compra-2').hidden = true;
                document.getElementById('paso-compra-3').hidden = false;
                document.getElementById("title-paso").textContent = "Método de pago";
            }
            break;
        case 3:
            if (validaPaso3()) {
                try {
                    await importCarro();
                    
                    const form = document.getElementById('pasos-container');
                    if (form) {
                        form.submit();
                    }
                } catch (error) {
                    console.error("Error al procesar el pago:", error);
                    showError("paso-msg-3", "Error al procesar el pago. Por favor intente nuevamente.");
                }
            }
            break;
        default:
            console.error("Paso no reconocido:", paso);
    }
}


// Validate first step - check if fields are not empty
function validaPaso1() {
    const correo = document.getElementById("correo-paso").value.trim();
    const telefono = document.getElementById("telefono-paso").value.trim();
    const direccion = document.getElementById("direccion-paso").value.trim();
    
    if (!correo) {
        showError("paso-msg-1", "Por favor ingrese su correo");
        return false;
    }
    
    if (!telefono) {
        showError("paso-msg-1", "Por favor ingrese su teléfono");
        return false;
    }
    
    if (!direccion) {
        showError("paso-msg-1", "Por favor ingrese su dirección");
        return false;
    }
    
    return true;
}

function validaPaso2() {
    const retiro = document.getElementById('metodo-entrega-1');
    const despacho = document.getElementById('metodo-entrega-2');
    
    if (!retiro.checked && !despacho.checked) {
        showError("paso-msg-2", "Por favor seleccione un método de entrega");
        return false;
    }
    
    return true;
}

function validaPaso3() {
    const transferencia = document.getElementById('metodo-pago-1');
    const webpay = document.getElementById('metodo-pago-2');
    
    if (!transferencia.checked && !webpay.checked) {
        showError("paso-msg-3", "Por favor seleccione un método de pago");
        return false;
    }
    return true;
}

// Show error message
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.innerHTML = `
            <div class="alert alert-danger">
                ${message}
            </div>
        `;
        
        // Auto-hide error after 3 seconds
        setTimeout(() => {
            errorElement.innerHTML = '';
        }, 3000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Reset error messages
    document.getElementById("paso-msg-1").innerHTML = '';
    document.getElementById("paso-msg-2").innerHTML = '';
    document.getElementById("paso-msg-3").innerHTML = '';
    
    // Reset title
    document.getElementById("title-paso").textContent = "Datos";
});

async function importCarro() {
    // Recuperar el carrito desde LocalStorage
    let carrito = localStorage.getItem("cart");
    if (!carrito) {
        console.error("El carrito está vacío");
        return;
    }

    // Convertir a objeto JSON
    carrito = JSON.parse(carrito);

    try {
        const response = await fetch("http://127.0.0.1:8000/load_carrito", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getToken()
            },
            body: JSON.stringify(carrito)
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        return await response.json();
    } catch (error) {
        console.error("Error al cargar el carrito:", error);
    }
}
  
function getToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : null;
};

function vaciarCarro() {
    // Se elimina el carrito del localStorage

    localStorage.removeItem("cart");
    window.location.href = "/";
};
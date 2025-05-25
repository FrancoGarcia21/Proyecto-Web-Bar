const carrito = [];

function agregarAlCarrito(producto) {
  const index = carrito.findIndex(p => p.id === producto.id);
  if (index >= 0) {
    carrito[index].cantidad += producto.cantidad;
  } else {
    carrito.push(producto);
  }
  renderCarrito();
}

function quitarDelCarrito(id) {
  const index = carrito.findIndex(p => p.id === id);
  if (index >= 0) {
    carrito.splice(index, 1);
    renderCarrito();
  }
}

function actualizarCantidad(id, delta) {
  const producto = carrito.find(p => p.id === id);
  if (producto) {
    producto.cantidad += delta;
    if (producto.cantidad <= 0) quitarDelCarrito(id);
    else renderCarrito();
  }
}

function renderCarrito() {
  const tbody = document.querySelector('#tabla-carrito tbody');
  tbody.innerHTML = '';

  let total = 0;

  carrito.forEach(p => {
    total += p.precio * p.cantidad;

    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${p.nombre}</td>
      <td>${p.cantidad}</td>
      <td>$${(p.precio * p.cantidad).toFixed(2)}</td>
      <td>
        <button onclick="actualizarCantidad(${p.id}, 1)">+</button>
        <button onclick="actualizarCantidad(${p.id}, -1)">-</button>
      </td>
    `;
    tbody.appendChild(fila);
  });

  document.getElementById('total-carrito').textContent = total.toFixed(2);
}

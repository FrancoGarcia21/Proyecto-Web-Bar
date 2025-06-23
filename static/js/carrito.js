const carrito = [];

function agregarAlCarrito(producto) {
  const index = carrito.findIndex((p) => p.id === producto.id);
  if (index >= 0) {
    carrito[index].cantidad += producto.cantidad;
  } else {
    carrito.push(producto);
  }
  renderCarrito();
}

function quitarDelCarrito(id) {
  const index = carrito.findIndex((p) => p.id === id);
  if (index >= 0) {
    carrito.splice(index, 1);
    renderCarrito();
  }
}

function actualizarCantidad(id, delta) {
  const producto = carrito.find((p) => p.id === id);
  if (producto) {
    producto.cantidad += delta;
    if (producto.cantidad <= 0) quitarDelCarrito(id);
    else renderCarrito();
  }
}

function renderCarrito() {
  const $tbody = $("#tbodyCarrito");
  $tbody.empty();

  let total = 0;

  carrito.forEach((p) => {
    total += p.precio * p.cantidad;

    const $fila = $(`
      <tr>
        <td class="truncate max-w-[150px]">${p.nombre}</td>
        <td class="text-center">${p.cantidad}</td>
        <td class="text-right">$${(p.precio * p.cantidad).toFixed(2)}</td>
        <td class="text-center">
          <div class="boton-mas-menos">
          <button 
          class="boton-mas"
          type="button" onclick="actualizarCantidad(${p.id}, 1)">+</button>
          <button 
          class="boton-menos"
          type="button" onclick="actualizarCantidad(${p.id}, -1)">-</button>
        </td>
      </tr>
    `);

    $tbody.append($fila);
  });

  $("#total-carrito").text(total.toFixed(2));
}

/*  Función escuchadora para mandar los datos a la base, formateo lo que esta en el carrito, solo mando id y cantidad */
document.addEventListener("DOMContentLoaded", () => {
  const finalizar = document.getElementById("finalizar-venta");

  finalizar.addEventListener("click", () => {
    if (carrito.length === 0) {
      mensajes("Alerta", "No hay productos en el carrito", "warning");
      return;
    }

    var venta = [];
    for (const item of carrito) {
      venta.push({
        id: item.id,
        cantidad: item.cantidad,
      });
    }
    console.log(venta);

    fetch("/venta/crear-venta", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(venta),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error del servidor: " + response.status);
        }
        return response.json(); // solo si la respuesta fue válida
      })
      .then((data) => {
        if (data.success) {
          mensajes("Éxito", "Venta realizada con éxito", "success");
          // cargo

          // Limpio el carrito
          carrito.length = 0;
          renderCarrito();
        } else {
          mensajes(
            "Error",
            data.message || "No se pudo realizar la venta",
            "error"
          );
        }
      })
      .catch((error) => {
        console.error("Error al enviar la venta:", error);
        mensajes(
          "Error",
          "No se pudo procesar la venta. Intenta nuevamente.",
          "error"
        );
      });
  });
});

/* Mensajes con sweetalert genericos segun el response*/
function mensajes(tittle, text, icon) {
  Swal.fire({
    title: tittle,
    text: text,
    icon: icon,
    confirmButtonText: "Aceptar",
  });
}

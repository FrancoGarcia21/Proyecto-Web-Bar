/* Escuchador principal */
document.addEventListener("DOMContentLoaded", () => {
  inicializarEventosProductos();
  const botones = document.querySelectorAll(".btn-categoria");

  botones.forEach((boton) => {
    boton.addEventListener("click", (e) => {
      const idCategoria = e.target.dataset.id;

      fetch(`/venta/buscar-categoria/${idCategoria}`)
        .then((res) => res.text())
        .then((html) => {
          document.getElementById("productos").innerHTML = html;
          inicializarEventosProductos();
        })
        .catch((err) => console.error("Error al cargar productos:", err));
    });
  });
});


/* funcion que crea los botones con un dataset del carrito*/
function inicializarEventosProductos() {
  document.querySelectorAll(".btn-producto").forEach((boton) => {
    boton.addEventListener("click", () => {
      const id = parseInt(boton.dataset.id);
      const nombre = boton.dataset.nombre;
      const precio = parseFloat(boton.dataset.precio);

      cantidad = 1;

      /* aca agregar que si el producto ya no tiene stock no deje agregar mas al carrito y cambie de color el boton, hice un estilo para eso 
        o dejar que lo haga el que cargue todos los items y cuando envie la peticion de carga decirle que no hay stock
      */
      
      if (!isNaN(cantidad) && cantidad > 0) {
        agregarAlCarrito({ id, nombre, precio, cantidad });
      }
    });
  });
}

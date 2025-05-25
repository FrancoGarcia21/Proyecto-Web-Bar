/* document.addEventListener("DOMContentLoaded", function () {
  const flashScript = document.getElementById("flash-data");
  if (flashScript) {
    try {
      const flashData = JSON.parse(flashScript.textContent);
      flashData.forEach(msg => {
        Swal.fire({
          icon: msg.category === "success" ? "success" : "error",
          title: msg.category === "success" ? "Éxito" : "Error",
          text: msg.message,
          confirmButtonText: "Aceptar"
        });
      });
    } catch (e) {
      console.error("Error parsing flash messages:", e);
    }
  }
}); */

document.addEventListener("DOMContentLoaded", function () {
  const flashScript = document.getElementById("flash-data");
  if (flashScript) {
    try {
      const flashData = JSON.parse(flashScript.textContent);
      flashData.forEach(msg => {
        Swal.fire({
          icon: msg.category === "success" ? "success" : "error",
          title: msg.category === "success" ? "✅ Éxito" : "⚠️ Error",
          text: msg.message,
          confirmButtonText: "Aceptar",
          background: "#1a1a1a",                // Fondo gris oscuro
          color: "#d3d3d3",                     // Texto gris claro
          confirmButtonColor: "#420c14",        // Bordó (como tus botones)
          customClass: {
            popup: "rounded-lg shadow-lg font-serif"
          }
        });
      });
    } catch (e) {
      console.error("Error parsing flash messages:", e);
    }
  }
});




/* document.addEventListener("DOMContentLoaded", function () {
  if (window.flashMessages) {
    window.flashMessages.forEach(function ([category, message]) {
      Swal.fire({
        icon: category === "success" ? "success" : "error",
        title: category === "success" ? "Éxito" : "Error",
        text: message,
        confirmButtonText: "Aceptar"
      });
    });
  }
}); */

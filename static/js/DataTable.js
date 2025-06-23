$(document).ready(function () {
  $(".dataTable").each(function () {
    if (!$.fn.DataTable.isDataTable(this)) {
      $(this).DataTable({
        language: {
          search: "Buscar:",
          lengthMenu: "Mostrar _MENU_ registros por página",
          zeroRecords: "No se encontraron productos",
          info: "Mostrando página _PAGE_ de _PAGES_",
          infoEmpty: "No hay registros disponibles",
          infoFiltered: "(filtrado de _MAX_ registros totales)",
          paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior",
          },
        },
        pageLength: 10
      });
    }
  });
});

(function ($) {
    //    "use strict";


    /*  Data Table
    -------------*/

    $('#bootstrap-data-table').DataTable({
        lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "Todos"]],
        language: {
            "url": "https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-AR.json"
        }
    });

    $('#dataTable-export').DataTable({
		dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excel',
                split: ['excel', 'pdf', 'print'],
            }
        ],
        pageLength: 15,
        language: {
            "url": "https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-AR.json"
        }
    });

	$('#row-select').DataTable({
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "Todos"]],
        initComplete: function () {
            this.api().columns().every(function () {
                var column = this;
                var select = $('<select class="form-control"><option value=""></option></select>')
                    .appendTo($(column.footer()).empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });

                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        },
        language: {
            "url": "https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-AR.json"
        }
    });

})(jQuery);

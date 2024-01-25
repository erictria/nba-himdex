function clearTable() {
    $('#himdex_table').DataTable()
        .clear()
        .draw();
}

function loadTable(data) {
    $('#himdex_table').DataTable({
        "data": data,
        "columns": [
            { "data": "season_year"},
            { "data": "team_abbreviation"},
            { "data": "player_name"},
            { "data": "average_min"},
            { "data": "total_plus_minus"},
            { "data": "avg_bucket_contribution_rate"},
            { "data": "avg_stop_contribution_rate"},
            { "data": "avg_tmt_bucket_uplift_contribution_rate"},
            { "data": "avg_tmt_stop_uplift_contribution_rate"},
        ],
        paging: true,
        searching: true,
        lengthMenu: [10, 25, 50, 100],
        dom: 'Bfrtip',
        buttons: [{ extend: 'excelHtml5', className: 'btn btn-datatable'}],
        destroy: true,
        order: [[0, 'asc']],
        bSort: true
    }

    );
}; 
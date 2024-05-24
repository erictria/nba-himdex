var $table = $('#himdex_table')
var $season_dropdown = $('#season_dropdown')
var $search_players = $('#search_players')
var $player_dropdown = $('#player_dropdown')
var $search_him_players = $('#search_him_players')

function listSeasons() {
    const obj = {};
    const myJSON = JSON.stringify(obj);
    $.ajax({
        type: 'POST',
        url: '/api/get_seasons',
        contentType: 'application/json; charset=utf-8',
        data: myJSON,
        success: function (response, textStatus, xhr) {
            seasons = response['seasons']
            console.log('Success: ' + textStatus)

            // init drop down
        },
        error: function (xhr, XMLHttpRequest, textStatus) {
            console.log("Error: " + textStatus)
            console.log(xhr.responseText);
        },
    });
}

function listPlayers(season_year) {
    const obj = {"season_year": season_year};
    const myJSON = JSON.stringify(obj);

    $.ajax({
        type: 'POST',
        url: '/api/get_season_players',
        contentType: 'application/json; charset=utf-8',
        data: myJSON,
        success: function (response, textStatus, xhr) {
            players = response[season_year];
            console.log('Success: ' + textStatus);

            var player_select = $('#player_dropdown'); 

            // Clear existing options
            player_select.empty();

            // Add a default 'Select Player' option
            player_select.append(new Option('Select Player', ''));

            // Populate the dropdown with new options
            for(var i = 0; i < players.length; i++) {
                var player = players[i];
                // var el = new Option(player['player_name'], player['player_id']);
                var el = document.createElement('option');
                el.text = player['player_name'];
                el.value = player['player_id'];
                player_select.append(el);
            }

            // Refresh the Select2 dropdown
            player_select.trigger('change');
        },
        error: function (xhr, XMLHttpRequest, textStatus) {
            console.log("Error: " + textStatus);
            console.log(xhr.responseText);
        },
    });
}

function listHimPlayers(season_year, player_id) {
    const obj = {"season_year": season_year, "player_id": player_id};
    const myJSON = JSON.stringify(obj);
    $.ajax({
        type: 'POST',
        url: '/api/get_himdex_cluster',
        contentType: 'application/json; charset=utf-8',
        data: myJSON,
        success: function (response, textStatus, xhr) {
            him_players = response['him_players']
            console.log('Success: ' + textStatus)

            // load table
            loadTable(him_players)
        },
        error: function (xhr, XMLHttpRequest, textStatus) {
            console.log("Error: " + textStatus)
            console.log(xhr.responseText);
        },
    });
}   

// const backup_img = "https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png"

function loadTable(data) {
    var table = $('#himdex_table').DataTable({
        "data": data,
        "columns": [
            { "data": "team_abbreviation", "width": "20%"},
            { 
                "data": "team_logo",
                "render": function(data, type, row) {
                    return '<img src="' + data + '" />';
                },
                "width": "20%"
            },
            { "data": "player_name", "width": "30%"},
            { 
                "data": "player_headshot",
                "render": function(data, type, row) {
                    return '<img src="' + data + '" alt="Image Unavailable" class="table-image" onerror="this.src=\'https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png\';" />';
                },
                "width": "30%"
            }
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

    $('#himdex_table tbody').off('click', 'tr'); // Remove existing event handlers
    // Handle row click event
    $('#himdex_table tbody').on('click', 'tr', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            var rowData = row.data();
            var hiddenData = '<div>' +
                             '<b>' + rowData.player_name + ', ' + rowData.team_abbreviation + '</b><br>' + 
                             'Minutes Per Game: ' + rowData.average_min.toFixed(2) + '<br>' +
                             'Total Plus Minus: ' + rowData.total_plus_minus + '<br>' +
                             'Average Bucket Contribution Rate: ' + rowData.avg_bucket_contribution_rate.toFixed(2) + '% <br>' +
                             'Average Stop Contribution Rate: ' + rowData.avg_stop_contribution_rate.toFixed(2) + '% <br>' +
                             'Average Teammate Bucket Boost Contribution Rate: ' + rowData.avg_tmt_bucket_uplift_contribution_rate.toFixed(4) + '% <br>' +
                             'Average Teammate Stop Boost Contribution Rate: ' + rowData.avg_tmt_stop_uplift_contribution_rate.toFixed(4) + '% <br>' +
                             '</div>';
            row.child(hiddenData).show();
            tr.addClass('shown');
        }
    });
}; 

$(document).ready(function() {
    $('#player_dropdown').select2({
        placeholder: 'Select Player',
        allowClear: true
    });
});

$(document).ready(function() {
    $('#season_dropdown').select2({
        placeholder: 'Select Season',
        allowClear: true
    });
});

$search_players.click(function () {
    season = $season_dropdown.val()
    console.log('here')
    console.log(season)
    listPlayers(season)
})

$search_him_players.click(function () {
    season = $season_dropdown.val()
    player_id = $player_dropdown.val()
    console.log('here')
    console.log(season)
    listHimPlayers(season, player_id)
})
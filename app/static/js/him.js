var $table = $('#himdex_table')
var $season_dropdown = $('#season_dropdown')
var $search_players = $('#search_players')
var $player_dropdown = $('#player_dropdown')
var $search_him_players = $('#search_him_players')
var $search_spinner = $('#search_spinner')

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

function listHimPlayers(season_year, player_id, team_id) {
    const obj = {"season_year": season_year, "player_id": player_id, "team_id": team_id};
    const myJSON = JSON.stringify(obj);
    $.ajax({
        type: 'POST',
        url: '/api/get_himdex_cluster',
        contentType: 'application/json; charset=utf-8',
        data: myJSON,
        beforeSend: function() {
            $("div.spanner").addClass("show");
            $("div.overlay").addClass("show");
        },
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
        complete: function() {
          $("div.spanner").removeClass("show");
          $("div.overlay").removeClass("show");
        }
    });
}   

// const backup_img = "https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png"

function loadTable(data) {
    var table = $('#himdex_table').DataTable({
        "data": data,
        "columns": [
            { "data": "team_abbreviation", "width": "10%"},
            { 
                "data": "team_logo",
                "render": function(data, type, row) {
                    return '<img src="' + data + '" class="table-image" />';
                },
                "width": "40%"
            },
            { "data": "player_name", "width": "10%"},
            { 
                "data": "player_headshot",
                "render": function(data, type, row) {
                    return '<img src="' + data + '" alt="Image Unavailable" class="table-image" onerror="this.src=\'https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png\';" />';
                },
                "width": "40%"
            },
            { "data": "sort_order", "visible": false}
        ],
        paging: true,
        searching: true,
        lengthMenu: [10, 25, 50, 100],
        dom: 'Bfrtip',
        destroy: true,
        order: [[4, 'asc']],
        bSort: true,
        columnDefs: [
            { className: "dt-center", targets: [1, 3] }
        ]
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
                             'Season: ' + rowData.season_year + '<br>' +
                             'Minutes Per Game: ' + rowData.average_min.toFixed(2) + '<br>' +
                             'Total Plus Minus: ' + rowData.total_plus_minus + '<br>' +
                             'Average Bucket Contribution Rate: ' + rowData.avg_bucket_contribution_rate.toFixed(2) + '% <br>' +
                             'Average Stop Contribution Rate: ' + rowData.avg_stop_contribution_rate.toFixed(2) + '% <br>' +
                             'Average Teammate Bucket Boost Contribution Rate: ' + rowData.avg_tmt_bucket_uplift_contribution_rate.toFixed(4) + '% <br>' +
                             'Average Teammate Stop Boost Contribution Rate: ' + rowData.avg_tmt_stop_uplift_contribution_rate.toFixed(4) + '% <br>' +
                             'HIMdex Score: <b>' + rowData.himdex_score.toFixed(2) + '</b><br>' +
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

$search_him_players.click(function () {
    $search_spinner.css('display', 'block')
    season = $season_dropdown.val()
    val_id = $player_dropdown.val()
    id_split = val_id.split("-")
    player_id = id_split[0]
    team_id = id_split[1]
    console.log('here')
    console.log(season)
    listHimPlayers(season, player_id, team_id)
    $search_spinner.css('display', 'none')
})

function loadPlayers(_) {
    $player_dropdown.prop('disabled', false)
    season = $season_dropdown.val()
    listPlayers(season)
}

function activateButton(_) {
    $search_him_players.prop('disabled', false)
}

// rankings
var $rankings_table = $('#himdex_rankings_table')
var $season_dropdown_rnk = $('#season_dropdown_rnk')
var $search_rankings = $('#search_rankings')
var $search_spinner_rnk = $('#search_spinner_rnk')

function listRankings(season_year) {
    const obj = {"season_year": season_year};
    const myJSON = JSON.stringify(obj);
    $.ajax({
        type: 'POST',
        url: '/api/get_himdex_rankings',
        contentType: 'application/json; charset=utf-8',
        data: myJSON,
        beforeSend: function() {
            $("div.spanner").addClass("show");
            $("div.overlay").addClass("show");
        },
        success: function (response, textStatus, xhr) {
            him_players = response['him_rankings']
            console.log('Success: ' + textStatus)

            // load table
            loadRankingsTable(him_players)
        },
        error: function (xhr, XMLHttpRequest, textStatus) {
            console.log("Error: " + textStatus)
            console.log(xhr.responseText);
        },
        complete: function() {
          $("div.spanner").removeClass("show");
          $("div.overlay").removeClass("show");
        }
    });
}   

// const backup_img = "https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png"

function loadRankingsTable(data) {
    var table = $('#himdex_rankings_table').DataTable({
        "data": data,
        "columns": [
            { "data": "himdex_ranking", "width": "10%"},
            { "data": "team_abbreviation", "width": "10%"},
            { 
                "data": "team_logo",
                "render": function(data, type, row) {
                    return '<img src="' + data + '" class="table-image" />';
                },
                "width": "30%"
            },
            { "data": "player_name", "width": "10%"},
            { 
                "data": "player_headshot",
                "render": function(data, type, row) {
                    return '<img src="' + data + '" alt="Image Unavailable" class="table-image" onerror="this.src=\'https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png\';" />';
                },
                "width": "30%"
            },
            { "data": "himdex_score", "width": "10%"}
        ],
        paging: true,
        searching: true,
        lengthMenu: [10, 25, 50, 100],
        dom: 'Bfrtip',
        destroy: true,
        order: [[0, 'asc']],
        bSort: true,
        columnDefs: [
            { className: "dt-center", targets: [2, 4] }
        ]
    }

    );

    $('#himdex_rankings_table tbody').off('click', 'tr'); // Remove existing event handlers
    // Handle row click event
    $('#himdex_rankings_table tbody').on('click', 'tr', function () {
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
                             'Season: ' + rowData.season_year + '<br>' +
                             'HIMdex Score: <b>' + rowData.himdex_score.toFixed(2) + '</b><br>' +
                             'Total Plus Minus Percentile: ' + rowData.plus_minus_percentile + '<br>' +
                             'Average Bucket Contribution Rate Percentile: ' + rowData.avg_bucket_contribution_rate_percentile + '<br>' +
                             'Average Stop Contribution Rate Percentile: ' + rowData.avg_stop_contribution_rate_percentile + '<br>' +
                             'Average Teammate Bucket Boost Contribution Rate Percentile: ' + rowData.avg_tmt_bucket_uplift_contribution_rate_percentile + '<br>' +
                             'Average Teammate Stop Boost Contribution Rate Percentile: ' + rowData.avg_tmt_stop_uplift_contribution_rate_percentile + '<br>' +
                             '</div>';
            row.child(hiddenData).show();
            tr.addClass('shown');
        }
    });
}; 

$(document).ready(function() {
    $('#season_dropdown_rnk').select2({
        placeholder: 'Select Season',
        allowClear: true
    });
});

$search_rankings.click(function () {
    $search_spinner_rnk.css('display', 'block')
    season = $season_dropdown_rnk.val()
    console.log('here')
    console.log(season)
    listRankings(season)
    $search_spinner_rnk.css('display', 'none')
})

function activateRankingsButton(_) {
    $search_rankings.prop('disabled', false)
}
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
            players = response[season_year]
            console.log('Success: ' + textStatus)

            var player_select = document.getElementById("player_dropdown"); 

            for(var i = 0; i < players.length; i++) {
                var player = players[i];
                var el = document.createElement('option');
                el.text = player['player_name'];
                el.value = player['player_id'];
                player_select.add(el);
            }

            // load drop down
        },
        error: function (xhr, XMLHttpRequest, textStatus) {
            console.log("Error: " + textStatus)
            console.log(xhr.responseText);
        },
    });
}

// function listPlayers(season_year) {
//     const obj = {"season_year": season_year};
//     const myJSON = JSON.stringify(obj);
//     $.ajax({
//         type: 'POST',
//         url: '/api/get_players',
//         contentType: 'application/json; charset=utf-8',
//         data: myJSON,
//         success: function (response, textStatus, xhr) {
//             players = response['players']
//             console.log('Success: ' + textStatus)

//             var player_select = document.getElementById("player_dropdown"); 

//             for(var i = 0; i < players.length; i++) {
//                 var player = players[i];
//                 var el = document.createElement('option');
//                 el.text = player['player_name'];
//                 el.value = player['player_id'];
//                 player_select.add(el);
//             }

//             // load drop down
//         },
//         error: function (xhr, XMLHttpRequest, textStatus) {
//             console.log("Error: " + textStatus)
//             console.log(xhr.responseText);
//         },
//     });
// }   

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

function loadTable(data) {
    $('#himdex_table').DataTable({
        "data": data,
        "columns": [
            { "data": "team_abbreviation"},
            { "data": "team_logo",
              "render": function(data, type, row) {
                return '<img src="' + data + '" />';
            }},
            { "data": "player_name"},
            { "data": "player_headshot",
              "render": function(data, type, row) {
                return '<img src="' + data + '" />';
            }}
            // { "data": "average_min"},
            // { "data": "total_plus_minus"},
            // { "data": "avg_bucket_contribution_rate"},
            // { "data": "avg_stop_contribution_rate"},
            // { "data": "avg_tmt_bucket_uplift_contribution_rate"},
            // { "data": "avg_tmt_stop_uplift_contribution_rate"},
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
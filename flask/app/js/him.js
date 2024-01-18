var $table = $('#himdex_table')
// var $approve = $('#approve')
// var selections = []
// var jobs = []

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
        url: '/api/get_players',
        contentType: 'application/json; charset=utf-8',
        data: myJSON,
        success: function (response, textStatus, xhr) {
            players = response['players']
            console.log('Success: ' + textStatus)

            // load drop down
        },
        error: function (xhr, XMLHttpRequest, textStatus) {
            console.log("Error: " + textStatus)
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
        success: function (response, textStatus, xhr) {
            him_players = response['him_players']
            console.log('Success: ' + textStatus)

            // load table
        },
        error: function (xhr, XMLHttpRequest, textStatus) {
            console.log("Error: " + textStatus)
            console.log(xhr.responseText);
        },
    });
}   
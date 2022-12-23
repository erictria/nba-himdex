from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

def get_players():
    p = players.get_players()
    return p

def get_player_stats(player_id):
    player_stats = playercareerstats.PlayerCareerStats(player_id = player_id)
    return player_stats.get_data_frames()[0]

if __name__ == '__main__':
    #p = get_players()
    #print(p)
    stats = get_player_stats('203076')
    breakpoint()
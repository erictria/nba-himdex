
def get_player_headshot(player_id: int):
    '''
    PURPOSE: adds the link to a player's current headshot
             formatted as https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png
             backup format: https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png
             source - https://medium.com/@avinash.sarguru/getting-nba-player-pictures-for-you-application-6106d5530943

    INPUTS:
    player_id - int player id

    OUTPUTS:
    player_headshot - str link to player headshot photo
    '''

    # player_headshot = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
    player_headshot = f'https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png'

    return player_headshot

def get_team_logo(team_id: int):
    '''
    PURPOSE: adds the link to a team's main logo
             formatted as https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg

    INPUTS:
    team_id - int team id

    OUTPUTS:
    team_logo - str link to team primary logo
    '''

    team_logo = f'https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg'

    return team_logo

def get_pictures(data: dict):
    '''
    PURPOSE: adds the links for player and team photos

    INPUTS:
    data - dict of data; must include 'team_id' and 'player_id'

    OUTPUTS:
    data - dict with pictures included
    '''

    team_id = data['team_id']
    player_id = data['player_id']

    team_logo = get_team_logo(team_id = team_id)
    player_headshot = get_player_headshot(player_id = player_id)

    data['team_logo'] = team_logo
    data['player_headshot'] = player_headshot

    return data



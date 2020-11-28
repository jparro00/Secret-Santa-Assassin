from django import template
from django.urls import reverse

from ssa import constants

register = template.Library()

def get_player(user, arg):
    query_set = user.player_set.all()
    player = query_set.get(game=arg)
    return player

def get_display_name(user):
    name = user.username
    profile = user.profile
    if profile is not None:
        handle = profile.handle
        if handle is not None and handle != '':
            name = handle
    return name

def get_player_icon(player):
    profile = player.profile
    return profile.profile.image.url

def get_game_row_class(game):
    row_class = ''
    if game.get_state() == constants.GAME_STATE_ACTIVE:
        row_class = 'table-row'

    return row_class

def get_game_row_href(game, user):
    href = ''
    player = get_player(user, game)
    status = player.status

    if status == constants.KILLED:
        href = '/ssa/game-status/' + str(game.id)
    else:
        href = '/ssa/my-game/' + str(game.id)

    return href

def get_status_badge(status):
    badge_class = ""
    if status == constants.ALIVE:
        badge_class = 'badge-success'
    elif status == constants.PENDING:
        badge_class = 'badge-warning'
    elif status == constants.KILLED:
        badge_class = 'badge-danger'
    elif status == constants.WINNER:
        badge_class = 'badge-success'

    return 'badge-secondary'
    #return badge_class

register.filter('get_player', get_player)
register.filter('get_player_icon', get_player_icon)
register.filter('get_status_badge', get_status_badge)
register.filter('get_display_name', get_display_name)
register.filter('get_game_row_class', get_game_row_class)
register.filter('get_game_row_href', get_game_row_href)

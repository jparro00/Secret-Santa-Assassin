from django import template

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
            #name = handle
            pass
    return name

def get_player_icon(player):
    profile = player.profile
    return profile.profile.image.url

def get_status_badge(status):
    badge_class = ""
    if status == constants.ALIVE:
        badge_class = 'badge-success'
    elif status == constants.PENDING:
        badge_class = 'badge-warning'
    elif status == constants.KILLED:
        badge_class = 'badge-danger'

    return 'badge-danger'
    #return badge_class

register.filter('get_player', get_player)
register.filter('get_player_icon', get_player_icon)
register.filter('get_status_badge', get_status_badge)
register.filter('get_display_name', get_display_name)

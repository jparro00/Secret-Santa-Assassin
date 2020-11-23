from django import template

register = template.Library()

def get_player(user, arg):
    query_set = user.player_set.all()
    player = query_set.get(game=arg)
    return player

def get_player_icon(player):
    profile = player.profile
    return profile.profile.image.url


register.filter('get_player', get_player)
register.filter('get_player_icon', get_player_icon)

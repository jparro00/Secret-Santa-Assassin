from django import template

register = template.Library()

def get_player(user, arg):
    query_set = user.player_set.all()
    player = query_set.get(game=arg)
    return player


register.filter('get_player', get_player)
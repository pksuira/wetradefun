from django import template

register = template.Library()
from trades.models import *

@register.filter
def lookup(d, key):
    if key not in d:
        return None
    return d[key]

@register.filter
def lookup_game_image(d, key):
  if key not in d:
    return None
  return d[key].sender_game.image_url

@register.filter
def lookup_game_id(d, key):
  if key not in d:
    return None
  return d[key].sender_game.giant_bomb_id

@register.filter
def lookup_game_platform(d, key):
  if key not in d:
    return None
  return d[key].sender_game.platform
  



"""
Module that currently holds all of the search functions 
"""

import urllib2 #open urls
import json
import socket
socket.setdefaulttimeout(30)
#api_key is needed for access to the GB database
api_key = '?api_key=308d89c435a454c3943316fb25c73ceba1f8bf72'
searchStart = 'http://api.giantbomb.com/search/' + api_key 
specificGame = 'http://api.giantbomb.com/game/' 


def getList(searchQuery, offset, *params):
  """ Returns a nested dictionary based on the string passed in as searchQuery
  currently the outer dictionary uses the game name as a key and the inner uses
  the param associated with it as a key.

  params is a varible arugment of strings that are used to filter the resutls.
  what can be used as a param
  'name' : the name of the game
  'original_release_date' : when the game came out
  'aliases' : what else the games are know as
  'deck' : a short discription of the game
  'id' : the  games id
  'platform' : not implemented yet
  'image' : for now it returns multiple image urls.

  example
    import search as s
    x = s.getList('halo', 'name', 'id')
    x.keys() #prints out all the keys
    y = x['Halo 4'] #gets the nested halo 4 dict
    y['id'] #gets the id of Halo 4
    x['Halo 4']['id'] #access inner dictionary id value

  """
  #makes the params entered in the proper filter format
  filters = buildFilterStr(params)
  # searchString = searchStart + '&resources=game&query='+ searchQuery + filters + '&limit=10' +'&offset=' + offset
  searchString = searchStart + '&resources=game&query='+ searchQuery + filters + '&limit=10&format=json' + '&offset=' + str(offset) 
  # print searchString

  #queries the video game database
  file = urllib2.urlopen(searchString, timeout = 30)
  #make the dictionary
  gameList = []
  gameList = parseFieldsJson(file, params)
  return gameList

def parseFieldsJson(file, params):
  data = json.load(file)
  if data['number_of_page_results'] == 0:
    return None
  data = data['results']
  #todo, parse image, get platform and genre.
  getGen = 0
  getPlat = 0
  if 'genres' in params:
    getGen = 1
  if 'platforms' in params:
    getPlat = 1
  for x in data:
    x['genres'] = []
    x['platforms'] = []
    if 'image' in params and x['image'] != None:
      x['image'] = x['image']['icon_url']
    #get the platform and genre
    if getGen and getPlat:
      game = getGameDetsById(str(x['id']), 'platforms', 'genres')
      x['genres'] = game ['genres']
      x['platforms'] = game['platforms']
      #x['genres'] = getGenre(game['genres'])
      #x['platforms'] = getPlatform(game['platforms'])
    elif getGen:
       game = getGameDetsById(str(x['id']), 'genres')
       x['genres'] = game ['genres']
    elif getPlat:
      game = getGameDetsById(str(x['id']), 'platforms')          
      x['platforms'] = game['platforms']
    # for y in game['genres']:
    #   # print y['name']
    #   x['genre'].append(y['name'])
    # print x['genre']  
    # print x['platform']  
    # print game['results']['genres'][0]['name']
    # print game['results']['platforms'][0]['name']
  return data

def getGameDetsById(gameId, *params):
  """ returns a dict with the details on a specific game
  gameId is the id of the game you want details on
  params is a varible arugment of strings that are used to filter the resutls.
  what can be used as a param
  
  'name' : the name of the game
  'original_release_date' : when the game came out
  'aliases' : what else the games are know as
  'deck' : a short discription of the game
  'id' : the  games id
  'platform' : not implemented yet
  'image' : for now it returns multiple image urls.
  example
    x = getGameDetsById(2600)
    x['name'] #returns the game's name
    x['image'] #return a urls of the main image 
  """
  filters = buildFilterStr(params)
  searchString = specificGame + gameId +'/' + api_key + filters + '&format=json'
  file = urllib2.urlopen(searchString, timeout = 30)
  #game = parseFieldsSpecific(file)
  game = json.load(file)
  game = game['results']
  if 'genres' in params:
    game['genres'] = getGenre(game['genres'])
  if 'platforms' in params:
    game['platforms'] = getPlatform(game['platforms'])
  if 'image' in params and game['image'] != None:
    game['image'] = game['image']['super_url']
  return game


def getPlatform(platformNode):
  """ Platform nodes have to be parse differently
  """
  platList = []
  for x in platformNode:
    platList.append(x['name'])
  return platList

def getGenre(genreNode):
  """
  """
  genreList = []
  for x in genreNode:
    # print y['name']
    genreList.append(x['name'])
  return genreList
  
def buildFilterStr(params):
  """converts the parmas passed in to the syntax of the GB database query
  """
  filters = '&field_list='
  for x in params:
    filters += x + ','

  return filters  





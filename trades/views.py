from django.contrib.auth.decorators import login_required
import datetime, random, sha
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib import messages
from user.forms import RegistrationForm
from user.models import UserProfile
from trades.models import *
from trades import giantbomb
import json
from django.core.exceptions import ObjectDoesNotExist
import re
import search as s
import datetime
import urllib2

# import mails

def game_details(request, game_id):
  # Is the game in wishlist?
  in_wishlist = False
  if request.user.is_authenticated():
    try:
      wish_game = Game.objects.get(giant_bomb_id = game_id, platform = '')
      if Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = wish_game):
        in_wishlist = True
    except Game.DoesNotExist:
      pass

  game = s.getGameDetsById(game_id, 'id','name', 'original_release_date', 'image', 'deck', 'genres', 'platforms', 'site_detail_url')
  try:
      platforms_listed = Game.objects.filter(giant_bomb_id = game_id).exclude(num_of_listings = 0).values_list('platform')
      platforms_count = {}
      if platforms_listed:
        for k in platforms_listed:
          v = Game.objects.get(giant_bomb_id = game_id, platform = k[0]).num_of_listings
          platforms_count[k[0]] = v
  except Currentlist.DoesNotExist:
      games_listed = 0
  return render(request,'game_page.html', {'game': game, 'listings': platforms_count, 'in_wishlist': in_wishlist,})


def search(request):
  if request.GET:
    query = request.GET['term']
    offset = request.GET['offset']
  else:
    return HttpResponseRedirect("/")


  # Replace all runs of whitespace with a single +
  # query = re.sub(r"\s+", '+', query)
  query = urllib2.quote(query)
  results = s.getList(query, offset,  'name', 'image', 'original_release_date', \
    'deck', 'id', 'site_detail_url')
  if results == None:
    return render_to_response('staticpages/no_game_found.html')
  for x in results:
    x['number_of_listing'] = Currentlist.objects.filter(giantBombID=x['id'], status = 'open').count()
  if x['number_of_listing'] == None:
    x['number_of_listing'] = 0
    
  previous=int(int(offset)-10)
  if previous == -10:
    previous=-1;
  
  next=int(int(offset)+10)
  if len(results) != 10:
    next=-1;
  
  return render(request, 'search_page.html', 
  {'results':results,
  'query':query,
  'previous':previous,
  'next':next
  })

@login_required(login_url='/users/sign_in/')
def add_to_wish_list(request):
  if request.is_ajax():
    # get game from table or add if not there
    game_id = request.GET.get('game_id')
    game = get_game_table_by_id(game_id, '') #CHANGE PLEASE
    # Check that is not already in wishlist
    if (not Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = game)):
      user_id = request.GET.get('user_id')
      userprofile = request.user.get_profile()
      user_name= userprofile.user.username
      game_id = request.GET.get('game_id')
      wishlist = Wishlist.objects.create(user = userprofile, wishlist_game = game)
      wishlist.save()
      message = user_name + " added " + game.name + " to their wish list"
    else:
      message = "already in wishlist"
  else:
    message = "Not AJAX"
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def remove_from_wish_list(request):
  if request.is_ajax():
    game_id = request.GET.get('game_id')
    game = get_game_table_by_id(game_id, '')
    game_in_wishlist = Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = game)
    if (game_in_wishlist.count() == 1):
      message = request.user.get_profile().user.username + " deleted " + game_in_wishlist[0].wishlist_game.name + " from their wish list"      
      game_in_wishlist[0].delete()
    else:
      message = "game not in wishlist"
  else:
    message = "Not AJAX"

  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def accept_offer(request):
  already_accepted = False

  if request.is_ajax():
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    other_trans = Transaction.objects.filter(current_listing = transaction.current_listing)
    r_message = request.GET.get('accept_comment')
    if (transaction != None):

      for ot in other_trans:
        if (ot.pk != transaction.pk and ot.status == "accepted"):
          already_accepted = True
          messages.error(request, "You have already accepted a trade offer for that listing")

      if (transaction.status == "offered" and already_accepted == False):
        transaction.status = "accepted"
        transaction.receiver_message = r_message
        messages.success(request, "You have successfully accepted the trade offer")
        transaction.save()

        for ot in other_trans:
          if (ot.pk != transaction.pk and ot.status == "offered"):
            ot.status = "deferred"
            ot.save()

        # mails.send(
        #       'Someone has accepted an offer you done!',
        #       'We Trade Fun Team', 'wetradefun.webmaster@gmail.com',
        #       transaction.sender.user.username, 
        #       transaction.sender.user.email, 
        #       'Good news! '+request.user.get_profile().user.username+
        #       ' has accepted the offer you made for ' + transaction.current_listing.game_listed.name + 
        #       '\n\n http://wetradefun.appspot.com'
        #       )

      message= "Offer accepted"
    else:
      message = "No such trade exists"
  else:
    message="Not AJAX"
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def confirm_offer(request):
  if request.is_ajax():
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    senders_game = transaction.sender_game
    userprofile = request.user.get_profile()
    users_other_offers = Transaction.objects.filter(sender = userprofile, sender_game = senders_game)
    if (transaction != None):
      if (transaction.status == "accepted"):
        transaction.status = "confirmed"
        transaction.dateTraded = datetime.datetime.now()
        message = "Congratulations, you have completed your transaction"
        transaction.save()

        # mails.send(
        #       'Congrats! Your transaction has been completed!',
        #       'We Trade Fun Team', 'wetradefun.webmaster@gmail.com',
        #       transaction.current_listing.user.user.username, 
        #       transaction.current_listing.user.user.email, 
        #       'Good news! Your transaction for '+ transaction.current_listing.game_listed.name +
        #       ' has been completed by '+request.user.get_profile().user.username+
        #       '. Here is the contact email: '+ request.user.get_profile().user.email + 
        #       '\n\n http://wetradefun.appspot.com'
        #       )

        currentlisting = Currentlist.objects.get(pk = transaction.current_listing.pk)
        # currentlisting_user = currentlisting.user
        listing_other_offers = Transaction.objects.filter(current_listing = currentlisting)
        currentlisting.status = "closed"
        game = get_game_table_by_id(currentlisting.game_listed.giant_bomb_id, currentlisting.game_listed.platform)
        game.num_of_listings -= 1
        game.save()
        currentlisting.save()

        # to delete other tranactions where the sender offered the same game too but confirmed
        for othertransactions in users_other_offers:
          if othertransactions.current_listing.game_listed == transaction.current_listing.game_listed:
            if othertransactions != transaction:
              othertransactions.delete()

        #deletes the offer from the listings
        for otheroffers in listing_other_offers:
          if otheroffers != transaction:
            otheroffers.delete()

      else:
        message = "This trade is no longer available or has already been confirmed"
        message = str(transaction.pk)
    else:
      message = "No such trade exists"
  else:
    message = "Not AJAX"
  messages.success(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def decline_offer(request):
  if request.is_ajax():
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    userprofile = request.user.get_profile()
    if transaction != None:
      if (transaction.status == "offered" and userprofile == transaction.current_listing.user) or (transaction.status == "accepted" and userprofile == transaction.sender):
        transaction.status = "declined"
        message = userprofile.user.username + "declined the offer"
        transaction.save()
      else:
        message="This trade is no longer available or has already been accepted"
    else:
      message = "No such trade exists"
  else:
    message="Not AJAX"
  messages.error(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def delete_offer(request):
  message = ""

  if request.is_ajax():
    userprofile = request.user.get_profile()    
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    all_trans = Transaction.objects.filter(current_listing = transaction.current_listing)
    
    if transaction != None:
      if ((userprofile == transaction.sender) and ((transaction.status == "offered") or (transaction.status == "accepted") or (transaction.status == "deffered"))): 
        for ot in all_trans:
          if (ot.pk != transaction.pk and ot.status == "deferred"):
            ot.status = "offered"
            ot.save() 

        transaction.delete()
        message = userprofile.user.username + " deleted the offer"        
      else:
        message="This trade is no longer available or has already been confirmed"
    else:
      message = "This trade does not exist"
    message = 'This trade has been deleted'
  else:
    message="Not AJAX"
  messages.error(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def remove_listing(request):
  alreadyaccepted = False
  if request.is_ajax():
    listing = Currentlist.objects.get(pk = request.GET.get('listing_id'))
    if (listing != None):
      trans = Transaction.objects.filter(current_listing = listing)
      for s in trans:
        if (s.status == "accepted" or s == "confirmed"):
          alreadyaccepted = True
      if alreadyaccepted == False:
        for t in trans:
          t.delete()
        
        game_listed = listing.game_listed
        game_listed.num_of_listings -= 1
        game_listed.save()
        message = "You have deleted your listing for " + listing.game_listed.name
        listing.delete()
      else:
        message = "You cannot remove this listing because you have already accepted an offer for it"
    else:
      message = "This listing does not exist"
  else:
    message="Not AJAX"
  messages.error(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def make_offer(request):
  message = ""

  if request.user.is_authenticated():
    if request.is_ajax():
      userprofile = request.user.get_profile()
      user_name = userprofile.user.username
      r_platform = request.GET.get('r_platform')
      s_platform = request.GET.get('s_platform')
      s_game = get_game_table_by_id(request.GET.get('game1_id'), s_platform) # sender game / game offered
      r_game = get_game_table_by_id(request.GET.get('game2_id'), r_platform) # receiver game / game listed
      s_message = request.GET.get('offer_comment')
      
      if (s_game == r_game):
        messages.error(request, "You cannot offer the same game for the same platform")
      else:
        for listing in Currentlist.objects.filter(game_listed = r_game, status = "open"):
          if (listing.user == userprofile):
            message = "You cannot offer a game to your own listing"
            messages.error(request,"You can't offer a game to yourself. Your offer was made to the other listings.")
          else:
            if (Transaction.objects.filter(current_listing = listing, status = "deferred").count() != 0):
              transaction = Transaction.objects.create(status = "deferred", sender = userprofile, sender_game = s_game, current_listing = listing, sender_message = s_message)
              message += "DEFERRED\n"
              transaction.save()
            else:
              transaction = Transaction.objects.create(status = "offered", sender = userprofile, sender_game = s_game, current_listing = listing, sender_message = s_message)
              message += "OFFERED\n"
              transaction.save()

            # mails.send(
            #   'Someone has made an offer for your game!',
            #   'Webmaster', 'wetradefun.webmaster@gmail.com',
            #   listing.user.user.email, 
            #   listing.user.user.email, 
            #   'Good news! Someone has made an offer for your game ' + listing.game_listed.name + 
            #   '\n\n http://wetradefun.appspot.com')

        messages.success(request, "You have made an offer for " + r_game.name + " (" + r_game.platform + ")")
    else:
      message = "Not AJAX"
  else:
    message = "Not logged in"

  return HttpResponse(message)  

@login_required(login_url='/users/sign_in/')
def add_listing(request):
  if request.is_ajax():
    userprofile = request.user.get_profile()
    user_name = userprofile.user.username
    game_id = request.GET.get('game_id')
    platform = request.GET.get('platform')
    game = get_game_table_by_id(game_id, platform)
    currentlist = Currentlist.objects.create(user = userprofile, giantBombID = game_id, game_listed = game, status = "open")
    game.num_of_listings += 1
    game.save()
    currentlist.save()
    message  = "You have created a listing for " + game.name
  else:
    message = "Not AJAX"
  messages.success(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def rate_user(request):
  if request.is_ajax():
    message = ""
    added_rating = request.GET.get('desired_rating')
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    userprofile = request.user.get_profile()
    if (userprofile == transaction.sender or userprofile == transaction.current_listing.user):
      if (userprofile == transaction.sender):
        if (transaction.receiver_has_been_rated == None):
          userrating = transaction.current_listing.user
          transaction.receiver_has_been_rated = True
          transaction.save()
        else:
          message = "Error, You have already rated that user!"

      elif (userprofile == transaction.current_listing.user):
        if (transaction.sender_has_been_rated == None):
          userrating = transaction.sender
          transaction.sender_has_been_rated = True
          transaction.save()
        else:
          message = "Error, You have already rated that user!"

      totalRatings = userrating.num_of_ratings * userrating.rating
      userrating.num_of_ratings += 1
      totalRatings += float(added_rating)
      userrating.rating = float(totalRatings / userrating.num_of_ratings)
      message = "You have rated " + str(userrating.user.username) + " a rating of " + str(added_rating)
      userrating.save()
    else:
      message = "This trade does not exist"


  else:
    message = "Not AJAX"
  messages.success(request, message)
  return HttpResponse(message)

def get_request(request):
  if request.is_ajax():
    inputString=urllib2.quote(request.GET.get('term'))
    games = s.getList(inputString, 0, 'id', 'name')
    results = []
    for game in games:
      game_json={}
      game_json['id']=game['id']
      game_json['value']=game['name'] 
      game_json['label']=game['name']
      results.append(game_json)
    message=json.dumps(results)
  else:
    message="Not AJAX"
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def get_platform(request, game_id):  
  if request.is_ajax(): 
    gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
    id=request.GET.get('id')
    results = s.getGameDetsById(game_id, 'platforms')
    platforms = results['platforms']
    results = []
    for platform in platforms:
      results.append(platform)
    message=json.dumps(results)
    return HttpResponse(message)

def put_in_game_table(id, platform):
  game = s.getGameDetsById(id, 'platforms', 'image', 'name', 'id')
  game = Game.objects.create(platform = platform, image_url = game['image'], \
    name = game['name'], num_of_listings = 0, giant_bomb_id = game['id'])
  game.save()
  return game

def get_game_table_by_id(id, platform):
  try:
    game = Game.objects.get(giant_bomb_id = id, platform = platform)
  except Game.DoesNotExist:
    game = put_in_game_table(id, platform)
  return game


def add_message(request):
  if request.is_ajax():
    if request.method == 'POST': # If the form has been submitted..
      transaction = Transaction.objects.filter(transaction_id = request.GET.get('transaction_id'))
      userprofile = request.user.get_profile()
      usermessage = Message(content = request.POST)
      usermessage.save()
      if transaction.receiver == userprofile:
        transaction.receiver_message = usermessage
      elif transaction.sender == userprofile:
        transaction.receiver_message = usermessage
      message = "Your message has been successfully sent"
    else:
      message = "Error"
  else:
    message="Not AJAX"
  return HttpResponse(message)

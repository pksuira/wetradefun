from django.template import Context, loader
# from polls.models import Poll
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import Http404
from forms import ContactForm
from django.contrib import messages

import search as s
from django.db.models import Avg, Max, Min, Count

from trades.models import *
from user.sort import *
# def index(request):
#     latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#     return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})

def searchresults(request):
    return HttpResponse("You're looking at the search results.")

# This big pro homepage should have (ideally):

#1.most traded games: all time
#2.hot wish-list item: the game that appears on the most wish-lists
#3.hot current listing: (how many current listings have that game)
#4.hot current listing: (the current listing with the most trade offers on it)
def homepage(request):
    mostTradedGames = getMostTradedGames()
    mostWishlistedGames = getMostWishlistedGames()
    mostListedGames = getMostListedGames()
    return render(request, 'homepage.html', {
        'most_traded_games': mostTradedGames,
        'most_wishlisted_games': mostWishlistedGames,
        'most_listed_games': mostListedGames,
        'username':request.user.username,
        })

def how_to_use(request):
    return render(request, 'staticpages/how_to_use.html')

def contact_us(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            # mails.send('Contacting', name, email, 'Webmaster', 'wetradefun.webmaster@gmail.com', text)
            messages.add_message(request, messages.SUCCESS, 'Thanks for contacting!')
    else:
        form = ContactForm()
    return render_to_response('staticpages/contact_us.html', {
      'form': form,
    },
    context_instance=RequestContext(request))

def no_game_found(request):
    return render(request, 'staticpages/no_game_found.html')

def getMostTradedGames():
    i = 0
    orderedTransaction = []
    if Transaction.objects.all().count() != 0:
        orderedTransactionTmp = Transaction.objects.all()
        for transactionobjects in orderedTransactionTmp:
            if transactionobjects.status == "confirmed":
                orderedTransaction.append(transactionobjects.sender_game)
                orderedTransaction.append(transactionobjects.current_listing.game_listed)

    sort(orderedTransaction, 'name', 'desc')
    prevorderedTransactionSize = len(orderedTransaction)
    topRatedGames = []

    i = 0
    while ((len(topRatedGames) != 4 and i < prevorderedTransactionSize) and (len(orderedTransaction) != 0)):
        j = 0
        maxCount = 0
        startIndex = 0
        tmp = 0
        while (j < len(orderedTransaction)):
            tmp = 1
            while (j != len(orderedTransaction) - 1) and (orderedTransaction[j] == orderedTransaction[j+1]):

                tmp = tmp + 1
                j = j + 1

                if j == len(orderedTransaction) - 1:
                    break

            if (tmp >= maxCount):
                maxCount = tmp
                startIndex = j - maxCount + 1

            j = j + 1
   
        topRatedGames.append(orderedTransaction[startIndex])

        while (maxCount != 0):
            orderedTransaction.remove(orderedTransaction[startIndex])
            maxCount = maxCount - 1


        i = i + 1
    return topRatedGames

def getMostWishlistedGames():

    orderedWishlist = []
    if Wishlist.objects.count() != 0:
        orderedWishlistTmp = Wishlist.objects.all()
        for wishlistobjects in orderedWishlistTmp:
            orderedWishlist.append(wishlistobjects.wishlist_game)

    sort(orderedWishlist, 'name', 'desc')
    prevorderedWishlistSize = len(orderedWishlist)
    topRatedWishlist = []

    m = 0
    while ((len(topRatedWishlist) != 4 and m < prevorderedWishlistSize) and (len(orderedWishlist) != 0)):
        n = 0
        maxCount = 0
        startIndex = 0
        tmp = 0
        while (n < len(orderedWishlist)):
            tmp = 1

            while (n != len(orderedWishlist) - 1) and (orderedWishlist[n] == orderedWishlist[n+1]):

                tmp = tmp + 1
                n = n + 1

            # if n == len(orderedWishlist) - 1:
            

            if (tmp >= maxCount):
                maxCount = tmp
                startIndex = n - maxCount + 1

            n = n + 1

        topRatedWishlist.append(orderedWishlist[startIndex])

        while (maxCount != 0):
            orderedWishlist.remove(orderedWishlist[startIndex])
            maxCount = maxCount - 1

        m = m + 1

    return topRatedWishlist

def getMostListedGames():

    list_of_ids = Currentlist.objects.values_list('giantBombID', flat=True)

    dict_of_number_of_ids = {}
    for game_id in list_of_ids:
      dict_of_number_of_ids[game_id] = Currentlist.objects.filter(giantBombID = game_id, status = 'open').count()

    import operator
    sorted_x = sorted(dict_of_number_of_ids.iteritems(), key=operator.itemgetter(1))
    sorted_x.reverse()

    topRatedListings = []
    counter = 0
    for tup in sorted_x:
      if counter == 4:
        break
      game = Game.objects.filter(giant_bomb_id = tup[0])[0]
      topRatedListings.append(game)
      counter += 1
      
    return topRatedListings

    # orderedListing = []
    # k = 0
    # if Game.objects.count() != 0:
    #     orderedListing = list(Game.objects.all())
    #     while (k < len(orderedListing)):
    #         for listing in orderedListing:
    #             if listing.name == orderedListing[k].name and orderedListing[k] != listing:
    #                 orderedListing[k].num_of_listings += listing.num_of_listings
    #                 orderedListing.remove(listing)
    #         k += 1
    #     sort(orderedListing, 'num_of_listings', 'desc')

    # topRatedListings = []
    # j = 0

    # while (j < len(orderedListing) and j != 4):
    #     if orderedListing[j].num_of_listings != 0:
    #         topRatedListings.append(orderedListing[j])
    #     j = j + 1

    # return topRatedListings


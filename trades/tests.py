"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
from django.utils import unittest
from trades.models import *
from user.models import *
from django.db.models import *
from datetime import *
import sys
from itertools import chain
from user.sort import *




class Test1(unittest.TestCase):
    def setUp(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        allen = User.objects.create_user('allen', 'allen@allen.com', 'allenpassword')
        allen.save()

        bob = User.objects.create_user('bob', 'bob@bob.com', 'bobpassword')
        bob.save()

        cathy = User.objects.create_user('cathy', 'cathy@cathy.com', 'cathypassword')
        cathy.save()

        doris = User.objects.create_user('doris', 'doris@doris.com', 'dorispassword')
        doris.save()

        edward = User.objects.create_user('edward', 'edward@edward.com', 'edwardpassword')
        edward.save()

        fred = User.objects.create_user('fred', 'fred@fred.com', 'fredpassword')
        fred.save()

        graves = User.objects.create_user('graves', 'graves@graves.com', 'gravespassword')
        graves.save()

        self.allenProfile = UserProfile.objects.create(user=allen, address="allenroad", rating=3)
        self.bobProfile = UserProfile.objects.create(user=bob, address="bobroad", rating=3)
        self.cathyProfile = UserProfile.objects.create(user=cathy, address="cathyroad", rating=3)    
        self.dorisProfile = UserProfile.objects.create(user=doris, address="dorisroad", rating=3)
        self.edwardProfile = UserProfile.objects.create(user=edward, address="edwardroad", rating=3)
        self.fredProfile = UserProfile.objects.create(user=fred, address="fredroad", rating=3)
        self.gravesProfile = UserProfile.objects.create(user=graves, address="gravesroad", rating=3)

        self.HaloGame = Game.objects.create(platform="XBOX", image_url="", name="Halo", giant_bomb_id=2600, num_of_listings=0)
        self.StarcraftGame = Game.objects.create(platform="PC", image_url="", name="Starcraft", giant_bomb_id=13062, num_of_listings=0)
        self.CallOfDutyGame = Game.objects.create(platform="XBOX", image_url="", name="CallOfDuty", giant_bomb_id=1629, num_of_listings=0)
        self.PortalGame = Game.objects.create(platform="PC", image_url="", name="Portal", giant_bomb_id=21170, num_of_listings=0)
        self.AssassinsCreedGame = Game.objects.create(platform="XBOX", image_url="", name="AssassinsCreed", giant_bomb_id=2950, num_of_listings=0)


#allen, bob, cathy, and doris all make offers for gameID=11 which are listed by edward, fred, and graves. 

        self.transaction1 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction2 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 11, 11), dateTraded=datetime(2012, 11, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction3 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 12, 12), dateTraded=datetime(2012, 11, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction4 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction5 = Transaction.objects.create(status="offered", dateRequested=datetime(2011, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction6 = Transaction.objects.create(status="offered", dateRequested=datetime(2012, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction7 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction8 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction9 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction10 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction11 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction12 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)


#graves makes an offer to everybody else's listing of gameID=12
        self.transaction13 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.allenProfile, receiver_game=self.PortalGame)
        self.transaction14 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.bobProfile, receiver_game=self.PortalGame)
        self.transaction15 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.cathyProfile, receiver_game=self.PortalGame)
        self.transaction16 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.dorisProfile, receiver_game=self.PortalGame)
        self.transaction17 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.edwardProfile, receiver_game=self.PortalGame)
        self.transaction18 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.PortalGame)

#to check the most traded game of all time is gameID=1
        self.transaction19 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.PortalGame, receiver=self.allenProfile, receiver_game=self.StarcraftGame)
        self.transaction20 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.CallOfDutyGame, receiver=self.bobProfile, receiver_game=self.PortalGame)
        self.transaction21 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.allenProfile, receiver_game=self.HaloGame)
        self.transaction22 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.CallOfDutyGame)
        self.transaction23 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded=datetime(2012, 11, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.gravesProfile, receiver_game=self.CallOfDutyGame)

#to check most wishlisted game of all time is gameID=101
        self.wishlist1 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.HaloGame, datePosted=datetime(2010, 10, 10))
        self.wishlist2 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.StarcraftGame, datePosted=datetime(2010, 10, 10))
        self.wishlist3 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime(2010, 10, 10))
        self.wishlist4 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.CallOfDutyGame, datePosted=datetime(2010, 10, 10))
        self.wishlist5 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.PortalGame, datePosted=datetime(2010, 10, 10))

        self.wishlist6 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.HaloGame, datePosted=datetime(2010, 10, 10))
        self.wishlist7 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.StarcraftGame, datePosted=datetime(2010, 10, 10))
        self.wishlist8 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime(2010, 10, 10))
        self.wishlist9 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.CallOfDutyGame, datePosted=datetime(2010, 10, 10))

        self.wishlist10 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.HaloGame, datePosted=datetime(2010, 10, 10))
        self.wishlist11 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.StarcraftGame, datePosted=datetime(2010, 10, 10))
        self.wishlist12 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime(2010, 10, 10))

        self.wishlist13 = Wishlist.objects.create(user=self.dorisProfile, wishlist_game=self.HaloGame, datePosted=datetime(2010, 10, 10))
        self.wishlist14 = Wishlist.objects.create(user=self.dorisProfile, wishlist_game=self.StarcraftGame, datePosted=datetime(2010, 10, 10))

        self.wishlist15 = Wishlist.objects.create(user=self.edwardProfile, wishlist_game=self.HaloGame, datePosted=datetime(2010, 10, 10))

    # def test1(self):
    #     #q = Transaction.objects.all().filter(sender.user="allen").order_by('-sender_game')


    #     q = Transaction.objects.filter(sender=self.allenProfile).order_by('dateRequested')
    #     r = Transaction.objects.filter(sender=self.bobProfile).order_by('dateRequested')
    #     s = list(chain(q, r))

#1.most traded games: all time
#2.hot wish-list item: the game that appears on the most wish-lists
#3.hot current listing: (how many current listings have that game)
#4.hot current listing: (the current listing with the most trade offers on it)

    
    # def test1(self):

    #     orderedTransaction = []
    #     orderedTransaction2 = []

    #     orderedTransactionTmp = Transaction.objects.all()
    #     for transactionobjects in orderedTransactionTmp:
    #         if transactionobjects.status == "confirmed":
    #             orderedTransaction.append(transactionobjects)
    #             orderedTransaction2.append(transactionobjects)

    #     sort(orderedTransaction, 'receiver_game', 'desc')
    #     sort(orderedTransaction2, 'sender_game', 'desc')

    #     topRatedGames1 = []
    #     topRatedGames2 = []

    #     i = 0
    #     while (i != 3):
    #         j = 0
    #         maxCount = 0
    #         startIndex = 0
    #         tmp = 0
    #         while (j < len(orderedTransaction) - 1):
    #             tmp = 1
    #             while (orderedTransaction[j].receiver_game == orderedTransaction[j+1].receiver_game):

    #                 tmp = tmp + 1
    #                 j = j + 1

    #                 if j == len(orderedTransaction) - 1:
    #                     break

    #             if (tmp > maxCount):
    #                 maxCount = tmp
    #                 startIndex = j - maxCount + 1

    #             j = j + 1
       
    #         topRatedGames1.append(orderedTransaction[startIndex].receiver_game.name)

    #         while (maxCount != 0):
    #             orderedTransaction.remove(orderedTransaction[startIndex])
    #             maxCount = maxCount - 1

    #         k = 0
    #         startIndex = 0
    #         tmp = 0

    #         while (k < len(orderedTransaction2) - 1):
    #             tmp = 1
    #             while (orderedTransaction2[k].sender_game == orderedTransaction2[k+1].sender_game):

    #                 tmp = tmp + 1
    #                 k = k + 1

    #                 if k == len(orderedTransaction2) - 1:
    #                     break

    #             if (tmp > maxCount):
    #                 maxCount = tmp
    #                 startIndex = k - maxCount + 1

    #             k = k + 1
       
    #         topRatedGames2.append(orderedTransaction2[startIndex].sender_game.name)

    #         while (maxCount != 0):
    #             orderedTransaction2.remove(orderedTransaction2[startIndex])
    #             maxCount = maxCount - 1

    #         i = i + 1
   

    #     self.assertEquals(topRatedGames1[0], "CallOfDuty")
    #     self.assertEquals(topRatedGames1[1], "Portal")
    #     self.assertEquals(topRatedGames1[2], "Starcraft")

    #     self.assertEquals(topRatedGames2[0], "Starcraft")
    #     self.assertEquals(topRatedGames2[1], "AssassinsCreed")
    #     self.assertEquals(topRatedGames2[2], "Portal") 


    def test2(self):

        orderedTransaction = []

        orderedTransactionTmp = Transaction.objects.all()
        for transactionobjects in orderedTransactionTmp:
            if transactionobjects.status == "confirmed":
                orderedTransaction.append(transactionobjects.sender_game)
                orderedTransaction.append(transactionobjects.receiver_game)


        #orderedTransaction.order_by('name')
        sort(orderedTransaction, 'name', 'desc')


        topRatedGames = []

        i = 0
        while (i != 4):
            j = 0
            maxCount = 0
            startIndex = 0
            tmp = 0
            while (j < len(orderedTransaction) - 1):
                tmp = 1
                while (orderedTransaction[j] == orderedTransaction[j+1]):

                    tmp = tmp + 1
                    j = j + 1

                    if j == len(orderedTransaction) - 1:
                        break

                if (tmp > maxCount):
                    maxCount = tmp
                    startIndex = j - maxCount + 1

                j = j + 1
       
            topRatedGames.append(orderedTransaction[startIndex].name)

            while (maxCount != 0):
                orderedTransaction.remove(orderedTransaction[startIndex])
                maxCount = maxCount - 1


            i = i + 1
   

        self.assertEquals(topRatedGames[0], "Starcraft")
        self.assertEquals(topRatedGames[1], "CallOfDuty")
        self.assertEquals(topRatedGames[2], "Portal")
        self.assertEquals(topRatedGames[3], "Halo")

        

    def test3(self):

        orderedWishlist = []
        orderedWishlistTmp = Wishlist.objects.all()
        #orderedWishlistTmp.order_by('wishlist_game')
        #orderedWishlist = list(orderedWishlistTmp)
        for wishlistobjects in orderedWishlistTmp:
            orderedWishlist.append(wishlistobjects.wishlist_game)

        sort(orderedWishlist, 'name', 'desc')

        topRatedWishlist = []

        m = 0
        while (m != 5):
            n = 0
            maxCount = 0
            startIndex = 0
            tmp = 0
            while (n < len(orderedWishlist) - 1):
                tmp = 1
                while (orderedWishlist[n] == orderedWishlist[n+1]):

                    tmp = tmp + 1
                    n = n + 1

                    if n == len(orderedWishlist) - 1:
                        break

                if (tmp > maxCount):
                    maxCount = tmp
                    startIndex = n - maxCount + 1

                n = n + 1

            topRatedWishlist.append(orderedWishlist[startIndex])

            while (maxCount != 0):
                orderedWishlist.remove(orderedWishlist[startIndex])
                maxCount = maxCount - 1

            m = m + 1

        self.assertEquals(topRatedWishlist[0].name, "Halo")
        self.assertEquals(topRatedWishlist[1].name, "Starcraft")
        self.assertEquals(topRatedWishlist[2].name, "AssassinsCreed")
        self.assertEquals(topRatedWishlist[3].name, "CallOfDuty")
        self.assertEquals(topRatedWishlist[4].name, "Portal")

 
<<<<<<< HEAD
    def test4(self):

        orderedListing = []
        orderedListing = Game.objects.all()
        sort(orderedListing, 'num_of_listings', 'desc')
        topRatedGames = []
        j = 0

        while (j < len(orderedListing) - 1):
            
            topRatedGames.append(orderedListing[j].name)
            j = j + 1
   
        self.assertEquals(topRatedGames[0], "Portal")
        self.assertEquals(topRatedGames[1], "Halo")
=======
    # def test4(self):

    #     orderedListing = []
    #     orderedListing = Game.objects.all()
    #     sort(orderedListing, 'num_of_listings', 'desc')
    #     topRatedGames = []
    #     j = 0

    #     while (j < len(orderedListing) - 1):
            
    #         topRatedGames.append(orderedListing[j].name)
    #         j = j + 1
   
    #     self.assertEquals(topRatedGames[0], "Portal")
    #     self.assertEquals(topRatedGames[1], "Halo")
>>>>>>> 10b5a2234b90dd73881aa653cae8106561d20a98

    
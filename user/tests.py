"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from trades.models import *
from user.models import *
from django.db.models import *
from user import sort

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

        self.transaction1 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction2 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2012, 10, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction3 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2011, 10, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction4 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2013, 10, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction5 = Transaction.objects.create(status="pending", dateTraded=datetime.date(2015, 10, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction6 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2014, 10, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction7 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction8 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction9 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction10 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction11 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction12 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)


#graves makes an offer to everybody else's listing of gameID=12
        self.transaction13 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.allenProfile, receiver_game=self.PortalGame)
        self.transaction14 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.bobProfile, receiver_game=self.PortalGame)
        self.transaction15 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.cathyProfile, receiver_game=self.PortalGame)
        self.transaction16 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.dorisProfile, receiver_game=self.PortalGame)
        self.transaction17 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.edwardProfile, receiver_game=self.PortalGame)
        self.transaction18 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.PortalGame)

#to check the most traded game of all time is gameID=1
        self.transaction19 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.allenProfile, receiver_game=self.PortalGame)
        self.transaction20 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.bobProfile, receiver_game=self.PortalGame)
        self.transaction21 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.allenProfile, receiver_game=self.CallOfDutyGame)
        self.transaction22 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.CallOfDutyGame)
        self.transaction23 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.gravesProfile, receiver_game=self.CallOfDutyGame)
        self.transaction24 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.PortalGame, receiver=self.fredProfile, receiver_game=self.StarcraftGame)

#to check most wishlisted game of all time is gameID=101
        self.wishlist1 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist2 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist3 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist4 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.CallOfDutyGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist5 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.PortalGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist6 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist7 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist8 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist9 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.CallOfDutyGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist10 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist11 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist12 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist13 = Wishlist.objects.create(user=self.dorisProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist14 = Wishlist.objects.create(user=self.dorisProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist15 = Wishlist.objects.create(user=self.edwardProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))

    def test_sort_desc(self):
        h = list(Transaction.objects.filter(sender=self.allenProfile))
        bob_h = list(Transaction.objects.filter(sender=self.bobProfile))
        h.extend(bob_h)

        print "\n*** Unsorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        sort.sort(h, 'dateTraded', "desc")

        print "\n*** Desc Sorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        self.assertFalse(1) # True = see print stmts

    def test_sort_asc(self):
        h = list(Transaction.objects.filter(sender=self.allenProfile).order_by('-dateTraded'))
        bob_h = list(Transaction.objects.filter(sender=self.bobProfile).order_by('-dateTraded'))
        h.extend(bob_h)

        print "\n*** Unsorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        sort.sort(h, 'dateTraded', "asc")

        print "\n*** Asc Sorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        self.assertFalse(0) # True = see print stmts

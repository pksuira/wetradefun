python manage.py runserver

Sign Up
http://127.0.0.1:8000/#signUp
Search Game
http://127.0.0.1:8000/trades/search_game/
Make Offer
http://127.0.0.1:8000/trades/search_game/

Ajax, JQuery, and GET
http://127.0.0.1:8000/trades/search_game/
http://cy-database.appspot.com/trades/search_game/
POST and JSON
http://127.0.0.1:8000/trades/search_form/
http://cy-database.appspot.com/trades/search_form/

Save User
http://127.0.0.1:8000/trades/save/[name]
Load User
http://127.0.0.1:8000/trades/load/[id]

python manage.py shell
from trades.models import Users, Userratings
u1=Users(name="AAA")
u2=Users(name="BBB")
u1.save()
u2.save()
u1.id
u1.name
u2.id
u2.name
r=Userratings(rating=5,senderID=u1,receiverID=u2)
r.save()
r.id
r.rating
r.senderID.id
r.senderID.name
r. receiverID.id
r. receiverID.name
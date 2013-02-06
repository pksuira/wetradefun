from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^search/$','trades.views.search' ),
    url(r'^game/(?P<game_id>\d+)/$', 'trades.views.game_details'),
    url(r'^add_to_wish_list/$', 'trades.views.add_to_wish_list'),
    url(r'^remove_from_wish_list/$', 'trades.views.remove_from_wish_list'),
    url(r'^make_offer/$', 'trades.views.make_offer'),
    url(r'^add_listing/$', 'trades.views.add_listing'),
    url(r'^remove_listing/$', 'trades.views.remove_listing'),
    url(r'^accept_offer/$', 'trades.views.accept_offer'),
    url(r'^confirm_offer/$', 'trades.views.confirm_offer'),
    url(r'^decline_offer/$', 'trades.views.decline_offer'),
    url(r'^delete_offer/$', 'trades.views.delete_offer'),
    url(r'^get_request/$', 'trades.views.get_request'),
    url(r'^get_platform/(?P<game_id>\d+)/$', 'trades.views.get_platform'),
    url(r'^rate_user/$', 'trades.views.rate_user'),
)
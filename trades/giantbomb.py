import urllib2

try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        try:
            from django.utils import simplejson
        except:
            raise Exception("GiantBomb wrapper requires the simplejson library (or Python 2.6) to work. http://www.undefined.org/python/")


class GiantBombError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Api:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.giantbomb.com/'

    @staticmethod

    def defaultRepr(obj):
        return unicode("<%s: %s>" % (obj.id, obj.name)).encode('utf-8')

    def checkResponse(self, resp):
        if resp['status_code'] == 1:
            return resp['results']
        else:
            raise GiantBombError('Error code %s: %s' % (resp['status_code'], resp['error']))

    def search(self, query, offset=0):
        results = simplejson.load(urllib2.urlopen(self.base_url + "/search/?api_key=%s&resources=game&query=%s&field_list=id,name,image&offset=%s&format=json" % (self.api_key, urllib2.quote(query), offset)))
        return [SearchResult.NewFromJsonDict(x) for x in self.checkResponse(results)]


class SearchResult:
    def __init__(self,
                 id=None,
                 name=None,
                 api_detail_url=None,
                 image=None):

        self.id = id
        self.name = name
        self.api_detail_url = api_detail_url
        self.image = image

    @staticmethod
    def NewFromJsonDict(data):
        print data
        if data:
            return SearchResult(id=data.get('id'),
                                name=data.get('name', None),
                                api_detail_url=data.get('api_detail_url', None),
                                image=data.get('image', None))
        return None

    def __repr__(self):
        return Api.defaultRepr(self)

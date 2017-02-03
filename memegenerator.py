#!/usr/bin/env python
import urllib
import sys
import json

# API Values
API_URL = 'http://version1.api.memegenerator.net/Instance_Create?'
USERNAME = 'UsIjFolf2'
PASSWORD = 'Quohyib0'

# Known memes with its corresponding background images
memes = {
    'Notsureif'     : { 'generatorID': 305,   'imageID' : 84688 },
    'Philosoraptor' : { 'generatorID': 17,    'imageID' : 984 },
    'Toad'          : { 'generatorID': 3,     'imageID' : 203 },
    'Foreveralone'  : { 'generatorID': 116,   'imageID' : 142442 },
    'Winpenguin'    : { 'generatorID': 29,    'imageID' : 983 },
    'Pedobear'      : { 'generatorID': 235,   'imageID' : 564288 },
    'Trollface'     : { 'generatorID': 26298, 'imageID' : 1182094 },
    'Yaoming'       : { 'generatorID': 1610,  'imageID' : 458071 },
    'Yuno'          : { 'generatorID': 2,     'imageID' : 166088 },
    'Successkid'    : { 'generatorID': 121,   'imageID' : 1031 },
    'Yodawg'        : { 'generatorID': 79,    'imageID' : 108785 },
    'Awyeah'        : { 'generatorID': 211112,'imageID' : 1778013 },
    'Chicken'       : { 'generatorID': 747,   'imageID' : 473733 }
}

def create_meme(meme, t0, t1):
    data = {
        'username' : 'UsIjFolf2',
        'password' : 'Quohyib0',
        'languageCode': 'es',
    }

    # Build the request
    url = API_URL   + 'username=' + data['username'] + '&'                       \
                    + 'password=' + data['password'] + '&'                       \
                    + 'languageCode=' + data['languageCode'] + '&'               \
                    + 'generatorID=' + str(memes[meme]['generatorID']) + '&'     \
                    + 'imageID=' + str(memes[meme]['imageID']) + '&'             \
                    + 'text0=' + urllib.quote_plus(t0) + '&'                     \
                    + 'text1=' + urllib.quote_plus(t1)

    response = urllib.urlopen(url).read()
    imageurl = json.loads(response).get('result').get('instanceImageUrl')
    return imageurl

def list_memes():
    print 'Available memes:'
    print
    for m in memes:
        print m
    print

if __name__ == '__main__':

    list_memes()

    if len(sys.argv) != 4:
        print('Usage meme text0 text1')
        sys.exit(1)
    print "creating: %s %s %s" % (sys.argv[1], sys.argv[2], sys.argv[3])
    print create_meme(sys.argv[1], sys.argv[2], sys.argv[3])

#!/usr/bin/env python
import urllib
import sys
import json

class Memegenerator:
    """
    Memegenerator class, generates a glorious meme using the memegenerator.net api.
    """

    # Data fields
    api_loc = 'http://version1.api.memegenerator.net/Instance_Create?'
    username = ''
    password = ''
    
    # A dictionary of known memes with its corresponding background images
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

    def __init__(self, user, passw):
        """
        Initialize the memegenerator class with password and username for the api
        """
        self.username = user
        self.password = passw

    def create_meme(self, meme, t0, t1):
        """
        Create a meme using the internal meme dictionary. 
        Text t0 and t1 can be of arbitrary size.
        """
        # Some API data
        data = {
            'username' : self.username,
            'password' : self.password,
            'languageCode': 'es',
            'generatorID': str(self.memes[meme]['generatorID']),
            'imageID': str(self.memes[meme]['imageID']),
            'text0': t0,
            'text1': t1
        }

        # Build the request
        url = self.api_loc + urllib.urlencode(data)

        # Call api and get html back (json)
        response = urllib.urlopen(url).read()
        # Get the url from the json object
        imageurl = json.loads(response).get('result').get('instanceImageUrl')

        return imageurl

    def list_memes(self):
        """
        List all known memes
        """
        print
        print "Available memes:"
        print
        for m in self.memes:
            print m
        print

def main():

    USERNAME = 'UsIjFolf2'
    PASSWORD = 'Quohyib0'

    m = Memegenerator(USERNAME,PASSWORD)

    if len(sys.argv) != 4:
        print("Usage: %prog [options] memename text0 text1")
        m.list_memes()
        sys.exit(1)
    
    print "creating: %s %s %s" % (sys.argv[1], sys.argv[2], sys.argv[3])
    print m.create_meme(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()

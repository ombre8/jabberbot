#!/usr/bin/env python
import urllib
import sys
import json
import re

class Issue:
    """
    Gets the issue url
    """

    username = ''
    password = ''

    def __init__(self, user=None, passw=None):
        """
        Initialize the issue class with password and username for the api
        """
        self.username = user
        self.password = passw

    def get_url(self, issue):
        """
        Converts issue number into url
        """
        url = 'https://redmine.puzzle.ch/issues/%d' % int(re.sub('#', '', issue))
        return url

    def get_title(self, issue):
        """
        Gets title of issue
        """
        if self.username is None or self.password is None:
            print("Username and password are needed for basic auth")
            exit(1)

        url = self.get_url(issue)
        # TODO: http request and parse for title
        return url

def main():
    t = Issue()
    print(t.get_url('#1234'))

if __name__ == '__main__':
    main()

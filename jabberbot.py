#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import sys
import logging
import getpass
import sleekxmpp
import re

from optparse import OptionParser
from modules.memegenerator import Memegenerator
from modules.issue import Issue

# set proper encoding
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

class MUCBot(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will greets those
    who enter the room, and acknowledge any messages
    that mentions the bot's nickname.
    """

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # set globals
        self.room = room
        self.nick = nick

        # add callbacks
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)


    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        Whenever the bot's nickname is mentioned, respond to
        the message.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        This handler will reply to messages that mention
        the bot's nickname.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """

        issue = re.search(r'#\d{3,5}', msg['body'])
        # "parse" body and choose correct callback
        # Just debugging! This needs to be done properly via event handler!
        if msg['mucnick'] != self.nick and "meme" in msg['body']:
             self.onMemeRequested(msg)
        elif msg['mucnick'] != self.nick and "Tagesverantwortung"  in msg['body']:
             self.onTVRequested(msg)
        elif msg['mucnick'] != self.nick and "morge" in msg['body']:
             self.onMorge(msg)
        elif msg['mucnick'] != self.nick and issue:
             self.onIssueRequested(msg, issue.group())
        elif msg['mucnick'] != self.nick and self.nick in msg['body']:
             self.onSysbotMentioned(msg)


    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'], presence['muc']['nick']),
                              mtype='groupchat')
        """

    # ---- Callback functions ahead
    def onSysbotMentioned(self, msg):
            self.send_message(mto=msg['from'].bare,
                              mbody="I heard that, %s. But I'm stupid now, waiting for your Pullrequest at https://github.com/ombre8/jabberbot" % msg['mucnick'],
                              mtype='groupchat')

    def onMemeRequested(self, msg):
        m = Memegenerator("UsIjFolf2", "Quohyib0")
        self.send_message(mto=msg['from'].bare,
                          mbody="Look at this: %s" % m.create_meme("Successkid", "Sysbot", "Now supports memes"),
                          mtype='groupchat')

    def onTVRequested(self, msg):
        self.send_message(mto=msg['from'].bare,
                          mbody="Not yet available",
                          mtype='groupchat')
    def onMorge(self, msg):
        self.send_message(mto=msg['from'].bare,
                          mbody="Hello %s, I wish you a wonderfull day!" % msg['mucnick'],
                          mtype='groupchat')

    def onIssueRequested(self, msg, issue):
        self.send_message(mto=msg['from'].bare,
                          mbody=Issue().get_url(issue),
                          mtype='groupchat')



if __name__ == '__main__':
    # Setup the command line arguments
    optp = OptionParser()

    # Output verbosity options
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")
    opts, args = optp.parse_args()

    # Setup logging
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = raw_input("MUC nickname: ")

    # Setup the MUCBot and register plugins
    xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas
    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

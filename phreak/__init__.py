#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

import webbrowser
import appindicator

import argparse
import pkg_resources
import signal
import os
try:
    import pynotify
except ImportError:
    pynotify = None

from producthunt import ProductHunt

class PHreak:
    
    ABOUT_URL = "http://captnemo.in/phreak/"
    icon_filename = os.path.abspath(pkg_resources.resource_filename('phreak.data', 'phreak.png'))

    def __init__(self, args):
        # create an indicator applet
        self.ind = appindicator.Indicator("PHreak", "phreak", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon(PHreak.icon_filename)
        self.db = set()

        # create a menu
        self.menu = gtk.Menu()

        # create items for the menu - refresh, quit and a separator
        menuSeparator = gtk.SeparatorMenuItem()
        menuSeparator.show()
        self.menu.append(menuSeparator)

        btnAbout = gtk.MenuItem("About")
        btnAbout.show()
        btnAbout.connect("activate", self.showAbout)
        self.menu.append(btnAbout)

        btnRefresh = gtk.MenuItem("Refresh")
        btnRefresh.show()
        #the last parameter is for not running the timer
        btnRefresh.connect("activate", self.refresh, True)
        self.menu.append(btnRefresh)

        btnQuit = gtk.MenuItem("Quit")
        btnQuit.show()
        btnQuit.connect("activate", self.quit)
        self.menu.append(btnQuit)

        self.menu.show()

        if pynotify:
            pynotify.init("phreak")

        self.refresh()
        self.ind.set_menu(self.menu)


    def showAbout(self, widget):
        """Handle the about btn"""
        webbrowser.open(PHreak.ABOUT_URL)

    #ToDo: Handle keyboard interrupt properly
    def quit(self, widget, data=None):
        gtk.main_quit()

    def run(self):
        signal.signal(signal.SIGINT, self.quit)
        gtk.main()
        return 0

    def open(self, widget, event=None, data=None):
        """Opens the link in the web browser"""
        #We disconnect and reconnect the event in case we have
        #to set it to active and we don't want the signal to be processed
        if not widget.get_active():
            widget.disconnect(widget.signal_id)
            widget.set_active(True)
            widget.signal_id = widget.connect('activate', self.open)

        self.db.add(widget.item_id)
        webbrowser.open(widget.url)
        webbrowser.open(widget.discussion_url)

    def addItem(self, item):
        """Adds an item to the menu"""

        i = gtk.CheckMenuItem(
            "(" + str(item['votes_count']).zfill(3) + "/" + str(item['comments_count']).zfill(3) + ")    " + item['name'])

        visited = item['id'] in self.db

        i.set_active(visited)
        i.url = item['redirect_url']
        i.item_id = item['id']
        i.discussion_url = item['discussion_url']
        tooltip = "{tagline}\nPosted by {user}".format(tagline=item['tagline'], user=item['user']['name'])
        i.set_tooltip_text(tooltip)
        i.signal_id = i.connect('activate', self.open)
        self.menu.prepend(i)
        i.show()

    def refresh(self, widget=None, no_timer=False):
        """Refreshes the menu """

        old_hunts = self.posts_to_set(ProductHunt.posts)

        data = list(reversed(ProductHunt.getPosts()))
        
        #Remove all the current stories
        for i in self.menu.get_children():
            if hasattr(i, 'url'):
                self.menu.remove(i)

        #Add back all the refreshed news

        for index, item in enumerate(data):
            self.addItem(item)

        # Send notifications if needed
        if pynotify:
            new_hunts = self.posts_to_set(ProductHunt.posts)

            difference = new_hunts - old_hunts

            if len(difference) > 0:
                pynotify.Notification("Product Hunt", str(len(difference))+" new hunts", PHreak.icon_filename).show()

        if not no_timer:
            gtk.timeout_add(10 * 30 * 1000, self.refresh, widget, no_timer)

    def posts_to_set(self, posts):
        result = set()
        for index, item in enumerate(posts):
            result.add(item['id'])
        return result

def main():
    parser = argparse.ArgumentParser(description='Product Hunt in your System Tray')
    parser.add_argument('-v','--version', action='version', version=pkg_resources.require("phreak")[0].version)
    args = parser.parse_args()
    indicator = PHreak(args)
    indicator.run()

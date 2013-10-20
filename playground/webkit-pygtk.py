# -*- coding: utf-8 -*-

import sys
from gi.repository import Gtk, Gdk, WebKit2 as WebKit


class NobixClientApp(object):

    def __init__(self, url=None):
        self._initial_url = url
        Gtk.init(sys.argv)
        self.setup_ui()

    def setup_ui(self):
        self.webview = WebKit.WebView()
        scrolled = Gtk.ScrolledWindow()
        scrolled.add(self.webview)

        self.window = Gtk.Window()
        self.window.add(scrolled)
        self.window.set_size_request(800, 600)

        self.window.connect("destroy", self.quit)

    def run(self):
        self.window.show_all()
        if self._initial_url:
            self.webview.load_uri(self._initial_url)
        Gtk.main()

    def quit(self, *args, **kwargs):
        Gtk.main_quit()

    def open(self, url):
        self.webview.load_uri(url)

def main():
    #app = NobixClientApp('file:///home/augusto/dev/code/nbs_client_init/index.html')
    #app = NobixClientApp('http://localhost:5000/dashboard')
    app = NobixClientApp('http://localhost:5000/pos')
    #app = NobixClientApp('file:///home/augusto/dev/src/live-git/jquery-hotkeys/test-static-05.html')
    #app = NobixClientApp('file:///home/augusto/pos.html')
    app.run()

if __name__ == '__main__':
    main()

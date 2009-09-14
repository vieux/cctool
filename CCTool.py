#!/usr/bin/env python2.6

import pygtk
pygtk.require('2.0')
import gtk

from winD import winD

def main():
    windows = winD()
    windows.show_all()

    gtk.main()

if __name__ == '__main__':
    main()

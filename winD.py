import pygtk
pygtk.require('2.0')
import gtk

import defines
import file360
import persos

class edit(gtk.Entry):
    def __init__(self, max, active=True):
        super(edit, self).__init__(max)
        self.set_width_chars(max)
        if not active: 
            self.set_text("0000000000000000")
            self.set_state(gtk.STATE_INSENSITIVE)

class winD(gtk.Window):
    def __init__(self):
        super(winD, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_size(640, 480)
        self.set_title(defines.APP_NAME)
        self.connect("delete_event", lambda w,e: gtk.main_quit())
        self.__file = None
        self.iters = []

        #menu
        self.UI = gtk.UIManager()
        agr = self.UI.get_accel_group()
        self.add_accel_group(agr)
        menuActions = gtk.ActionGroup("Menu")
        menuActions.add_actions([('Quit', gtk.STOCK_QUIT, '_Quit', None,  'Quit', gtk.main_quit),
                                 ('OpenF', gtk.STOCK_OPEN, '_Open File...', '<control>O', 'Open a file', self.openFile),
                                 ('CloseF', gtk.STOCK_CLOSE, 'Close File', None, 'Close a file', self.closeFile),
                                 ('About', None, '_About...', '<control>A', 'Open about box', self.showAbout),
                                 ('Help', None, '_Help'),
                                 ('File', None, '_File')])

        self.UI.insert_action_group(menuActions, 0)
        self.UI.add_ui_from_file('ui.xml')
        self.bigbox = gtk.HBox(False, 0)
        vbox = gtk.VBox(False, 0)
        self.bigbox.pack_start(vbox, True, True, 0)
        self.add(self.bigbox)
        
        vbox.pack_start(self.UI.get_widget("/ui/menubar"), False, False, 0)
        
        #Generel infos
        IDBoxs = gtk.HBox(False, 10)
        IDBoxs.pack_start(gtk.Label("Current Profile : "), False, False, 10)
        self.PEdit = edit(16, False)
        IDBoxs.pack_start(self.PEdit, False, False, 0)        
        IDBoxs.pack_start(gtk.Label("CC offset : "), False, False, 10)
        self.MEdit = edit(10, False)
        IDBoxs.pack_start(self.MEdit, False, False, 0)
        vbox.pack_start(IDBoxs, False, False, 10)

        #Global infos
        GOLDBox = gtk.HBox(False, 10)
        GOLDBox.pack_start(gtk.Label("Current GOLD : "), False, False, 10)
        self.GOLDEdit = edit(8, True)
        GOLDBox.pack_start(self.GOLDEdit, False, False, 0)
        vbox.pack_start(GOLDBox, False, False, 10)

        self.liststore = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str, str, str, str, str)
        for i in range (0, len(persos.persos)):
            self.iters.append(self.liststore.append((gtk.gdk.pixbuf_new_from_file('imgs/%s' % persos.persos[i][1]), persos.persos[i][0], 0, 0, "0/32", "0/32" ,"0/32" ,"0/32")))

        cell = gtk.CellRendererText()
        colimg = gtk.TreeViewColumn("Pic", gtk.CellRendererPixbuf(), pixbuf=0)
        col0 = gtk.TreeViewColumn("Character", cell, text=1)
        col1 = gtk.TreeViewColumn("Level", cell, text=2)
        col2 = gtk.TreeViewColumn("XP", cell, text=3)
        col3 = gtk.TreeViewColumn("Strengh", cell, text=4)
        col4 = gtk.TreeViewColumn("Defense", cell, text=5)
        col5 = gtk.TreeViewColumn("Magic", cell, text=6)
        col6 = gtk.TreeViewColumn("Agility", cell, text=7)
        self.tree = gtk.TreeView(self.liststore)
        self.tree.append_column(colimg)
        self.tree.append_column(col0)
        self.tree.append_column(col1)
        self.tree.append_column(col2)
        self.tree.append_column(col3)
        self.tree.append_column(col4)
        self.tree.append_column(col5)
        self.tree.append_column(col6)
        treeB = gtk.ScrolledWindow()
        treeB.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        treeB.add(self.tree)
        vbox.pack_start(treeB, True, True, 10)
        
        self.Bsave = gtk.Button("Save")
        self.Bsave.connect("clicked", self.save)
        vbox.pack_start(self.Bsave, False, True, 10)
        

    def showAbout(self, foo):
        about =  gtk.AboutDialog()
        about.set_name(defines.APP_NAME)
        about.set_version(defines.VERSION)
        about.set_authors(defines.AUTHORS)
        about.set_logo(gtk.gdk.pixbuf_new_from_file('imgs/logo.png'))
        about.run()
        about.destroy()
        
    def openFile(self, foo):
        wFS = gtk.FileChooserDialog("Open...",
                                    self,
                                    gtk.FILE_CHOOSER_ACTION_OPEN,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                     gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        if(wFS.run() == gtk.RESPONSE_OK):
            f = wFS.get_filename();
            self.__file = file360.profile(f, self)
        wFS.destroy()

    def closeFile(self, foo = None):
        if self.__file:
            self.__file.close()
            self.__file = None
            for i in range(0, len(persos.persos)):
                self.liststore.set(self.iters[i], 2, 0)
                self.liststore.set(self.iters[i], 3, 0)
                self.liststore.set(self.iters[i], 4, "0/25")
                self.liststore.set(self.iters[i], 5, "0/25")
                self.liststore.set(self.iters[i], 6, "0/25")
                self.liststore.set(self.iters[i], 7, "0/25")

            self.GOLDEdit.set_text("")
            self.MEdit.set_text("000000000000000")
            self.PEdit.set_text("000000000000000")

    def save(self, foo = None):
        if self.__file:
            if self.__file.save():
                self.closeFile()
            else:
                m = gtk.MessageDialog(self, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "An error occured, please check values")
                m.run()
                m.destroy()
        

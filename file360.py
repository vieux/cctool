import mmap
import gtk
from struct import unpack, pack
from hashlib import sha1
import consts
import defines

class profile:
    def __init__(self, filename, win):
        self.__f = open(filename, "r+")
        self.__map = mmap.mmap(self.__f.fileno(), 0)
        self.__win = win
        win.PEdit.set_text(filename.split("/")[-1]);
        self.__offset = self.__map.find(defines.CC_MAGIC) + 1
        win.MEdit.set_text("%#x" % self.__offset)
        win.GOLDEdit.set_text("%d" % self.getShort(self.__offset + consts.GOLD))
        self.fillPersos(win)

    def fillPersos(self, win):
        for i in range(0, len(win.iters)):
            win.liststore.set(win.iters[i], 2, "%d" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.LVL)) + 1))
            win.liststore.set(win.iters[i], 3, self.getShort(self.__offset + 120 + i * 24 + consts.XP))
            win.liststore.set(win.iters[i], 4, "%d/25" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.FORCE))))
            win.liststore.set(win.iters[i], 5, "%d/25" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.DEFENSE))))
            win.liststore.set(win.iters[i], 6, "%d/25" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.MAGIE))))
            win.liststore.set(win.iters[i], 7, "%d/25" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.AGILITE))))
            win.liststore.set(win.iters[i], 8, "%d" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.POTIONS))))
            win.liststore.set(win.iters[i], 9, "%d" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.BOMBES))))
            win.liststore.set(win.iters[i], 10, "%d" % (ord(self.getByte(self.__offset + 120 + i * 24 + consts.SANDWITCHS))))
            win.liststore.set(win.iters[i], 11, self.done(i))

    def done(self, i):
        val = ord(self.getByte(self.__offset + 120 + i * 24 + consts.DONE))
        if val == 0 : return "No"
        elif val == 1 : return "Yes"
        else : return "Insane"

    def getByte(self, pos = None):
        if pos: self.__map.seek(pos)
        return self.__map.read_byte()

    def getShort(self, pos = None, rev = False):
        if pos: self.__map.seek(pos)
        if rev: return unpack('<h', self.__map.read(2))[0]
        return unpack('>h', self.__map.read(2))[0]

    def getInt(self, pos = None):
        if pos: self.__map.seek(pos)
        return unpack('>L', self.__map.read(4))[0]

    def close(self):
        self.__map.close()
        self.__f.close()


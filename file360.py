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
        self.__offset = self.__map.find(defines.CC_MAGIC)
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

    def getByte(self, pos = None):
        if pos: self.__map.seek(pos)
        return self.__map.read_byte()

    def getShort(self, pos = None, rev = False):
        if pos: self.__map.seek(pos)
        if rev: return unpack('<h', self.__map.read(2))[0]
        return unpack('>h', self.__map.read(2))[0]

    def putShort(self, data, pos = None):
        if pos: self.__map.seek(pos)
        self.__map.write(pack('>h', int(data)))

    def getInt(self, pos = None):
        if pos: self.__map.seek(pos)
        return unpack('>L', self.__map.read(4))[0]

    def getHash(self, pos):
        self.__map.seek(pos)
        hash = "%08x%08x%08x%08x%08x" % (self.getInt(), self.getInt(), self.getInt(), self.getInt(), self.getInt())
        return hash

    def getPic(self, pic, pos, size):
        self.__map.seek(pos)
        file = open("_pic", "w")
        file.write(self.__map.read(size))
        file.close()
        if pic: pic.set_from_file("_pic")

    def save(self):
        if self.check_errors():
            self.putShort(self.__win.GOLDEdit.get_text(), self.__offset + consts.GOLD)
            return True
        return False

    def close(self):
        self.__map.close()
        self.__f.close()

    def check_errors(self):
        gold = self.__win.GOLDEdit.get_text()
        if not gold.isdigit() : return False
        if int(gold) >= 0 and  int(gold) < 65535:
            return True
        return False

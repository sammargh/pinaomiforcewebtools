import io
import os
import hashlib

class NAOMIGame(object):
    def __get_name(self):
        'Get game names from NAOMI and ATOMISWAVE rom file.'
        try:
            fp = open(self.filepath, 'rb')
            fp.seek(65280)
            naomicheck = fp.read(12).decode('utf-8').upper()
            if naomicheck == 'SYSTEM_X_APP':
                fp.seek(65328)
                self.name = fp.read(32).decode('utf-8').rstrip(' ').lstrip(' ')
            else:
                naomicheck = 'true'
            fp.close()
        except Exception:
            print(self.filename + " not Atomiswave going to try NAOMI ")
            naomicheck = 'true'
        if naomicheck == 'true':
            try:
                fp = open(self.filepath, 'rb')
                fp.seek(0x30, os.SEEK_SET)
                self.name = fp.read(32).decode('utf-8').rstrip(' ').lstrip(' ')
                fp.close()
            except Exception:
                print("__get_names(): Error reading names from" + self.filename)
        print(self.name)


    def __init__(self, filepath, skip_checksum = False):
        self.name = ''
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.status = None
        self.__get_name()

        if not skip_checksum:
            self.checksum = self.__checksum();

        try:
            self.size = os.stat(filepath).st_size
        except Exception:
            self.size = 0

    def __checksum(self):
        with open(self.filepath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
                
            return m.hexdigest()

    def __hash__(self):
        return hash((self.name, self.filepath, self.size)) & 0xffffffff


def is_naomi_game(filename):
    'Determine (loosely) if a file is a valid NAOMI netboot game'
    try:
        fp = open(filename, 'rb')
        fp.seek(65280)
        header_magic = fp.read(12).decode('utf-8').upper()
#        fp.close()
#        fp = open(filename, 'rb')
#        fp.seek(65328)
#        game_title = fp.read(32).decode('utf-8')
        fp.close()
        if header_magic == "SYSTEM_X_APP":
#            print("Game title should be " + game_title)
            header_magic = 'NAOMI'
            return header_magic == 'NAOMI'

    except Exception:
        print("This is not an Atomiswave game.")

    try:
        fp = open(filename, 'rb')
        header_magic = fp.read(5).decode('utf-8').upper()
        fp.close()
        if header_magic == 'NAOMI':
            return header_magic == 'NAOMI'

    except Exception:
        print("is_naomi_game(): Could not open " + filename )
        return False


def get_game_name(filename):
    'Read game name from NAOMI rom file.'
    print("Trying to get name of game from " + filename)
    try:
        fp = open(filename, 'rb')
        naomicheck = fp.read(5).decode('utf-8').upper()
        if naomicheck == "NAOMI":
            fp.seek(0x30, os.SEEK_SET)
            title = fp.read(32).decode('utf-8').strip(' ')
        else:
            fp.seek(65328)
            title = fp.read(32).decode('utf-8').upper()

#        '''
#        Dangit Darksoft lmao
#        Also, I didn't quite do my research, and ended up lifting this bit from some dude who forked off.
#        Hi ldindon! Keep at it :)
#        '''
#        if title == "AWNAOMI":
#                fp.seek(0xFF30)
#                title = fp.read(32).decode('utf-8').strip(' ')
        fp.close()
        print ("we think the title is " + title)
        return filename

    except Exception:
        print("get_game_name(): Error reading game name.")
        return ''

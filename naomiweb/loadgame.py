from time import sleep
import threading
from configparser import *
import RPi.GPIO as GPIO
from naomigame import *
import naomiboot



'''
A job sends a game to the NetDIMM. Each job has an associated thread (based on tiforce_tools) that sends a game's data over the network to the NetDIMM. A transfer is started with the start() method. Status of the transfer can be checked with finished().
'''

#TODO: rework status messaging to not be so gross.
class loadjob:
    _game = None
    _configuration = None
    _status = 0
    _message = None

    _game_file = None
    _thread = None


    def __init__(self, naomigame, configuration):
        self._game = naomigame
        self._configuration = configuration

    def loadgame(self):
        '''
        thread worker for job.
        '''
        if self._configuration.get('Main', 'gpio_reset') == 'True':
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(40, GPIO.OUT)
            GPIO.output(40,1)
            sleep(0.4)
            GPIO.output(40,0)
            sleep(2.0)

        game_path = self._game.filepath
        self._message = "Connecting to " + self._configuration.get('Network', 'ip')
        
        print("Uploading " + game_path + " to " + self._configuration.get('Network', 'ip'))

        try:
            naomiboot.connect(self._configuration.get('Network', 'ip'), 10703)
        except:
            self._status = 1
            self._message = "Connection Error"
            naomiboot.disconnect()
            return

        try:
            naomiboot.HOST_SetMode(0, 1)
            # disable encryption by setting magic zero-key
            naomiboot.SECURITY_SetKeycode("\x00" * 8)

            self._message = "Uploading " + game_path
            # uploads file. Also sets "dimm information" (file length and crc32)
            naomiboot.DIMM_UploadFile(game_path)
            
            self._message = "Booting game"
            
            # restart host, this will boot into game
            naomiboot.HOST_Restart()

            # set time limit to 10h. According to some reports, this does not work.

            naomiboot.TIME_SetLimit(10*60*1000)
            naomiboot.disconnect()
        except:
            self._status = 2
            self._message = "Error loading game on NAOMI"
            return

        self._status = 0
        self._message = "Done"

    def start(self):
        '''
        start the data transfer thread to send a game to the NetDIMM.

        Precondition: _game and _configuration point to valid objects. 
        Postcondition: process for loading game will be created and data will begin to be transfered to the NetDIMM.

        Return value: Always true

        '''

        game_path = self._game.filename
        self._status = 0
        self._message = "Loading {}...".format(game_path)

        self._thread = threading.Thread(target=self.loadgame)
        self._thread.start()

        return True

    def finished(self):
        '''
        Return value: True if there is no process associated with the job or the associated thread has ended.
        '''
        if self._status == 0:
            self._message = "Idle"

        if self._thread == None:
            return True

        if self._thread.isAlive():
            return False

        return True

    def status(self):
        return self._status

    def message(self):
        return self._message

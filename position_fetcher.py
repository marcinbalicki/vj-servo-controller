import logging
import logging.config
import re
import serial
import threading

# Serial communication with Arduino
SERIAL_NAME = '/dev/ttyUSB0'
# Regex for a message
REGEX_MSG = '^#[0-9]+ [0-9]$'
MSG_TRUE = '1'


class PositionFetcher(object):
    def __init__(self):
        self.log = logging.getLogger("positionFetcher")
        self.serial_port = None
        self.fetcher_thread = None
        self.current_position = None
        self.is_end = None
        self.msg_pattern = re.compile(REGEX_MSG)

        try:
            # Start logger thread
            self.fetcher_thread = threading.Thread(target=self.fetch_data)

            # Init Serial port
            self.serial_port = serial.Serial(SERIAL_NAME, timeout=1, baudrate=115200)
            self.serial_port.flushInput()
            self.serial_port.flushOutput()
            self.serial_lock = threading.Lock()
        except OSError, error:
            self.serial_port = None
            self.log.error("Cannot initialize. Reason: %s", error)
        except serial.serialutil.SerialException, error:
            self.serial_port = None
            self.log.error("Cannot initialize. Reason: %s", error)

        self.log.debug("Serial: %s", self.serial_port)

    def fetch_data(self):
        msg = ""
        while self.serial_port:
            self.serial_port.flushInput()
            while self.serial_port.read() != '#':
                pass
            msg = "#" + self.serial_port.readline().strip()
            if msg:
                self.log.debug("Received: %s", msg)
                self.store_data(msg)
        self.log.error("Position fetcher stopped")

    def store_data(self, msg):
        if self.msg_pattern.match(msg):
            data = msg.lstrip('#').split(" ")
            self.current_position = int(data[0])
            self.is_end = data[1] == MSG_TRUE
        else:
            self.log.info("Cannot store data for message: %s! Not matching the pattern.", msg)

    def start(self):
        self.fetcher_thread.start()

    def stop(self):
        # Close serial port
        self.log.info("Close serial port")
        if self.serial_port is not None and self.serial_port.isOpen():
            self.serial_port.close()
            self.serial_port = None

    def get_current_position(self):
        return self.current_position, self.is_end

if __name__ == "__main__":
    logging.config.fileConfig('log.ini')
    tester = PositionFetcher()
    tester.start()
    try:
        while True:
            pass
    finally:
        tester.stop()

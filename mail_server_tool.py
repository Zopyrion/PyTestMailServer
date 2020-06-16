import asyncore
import string
import random
import os
from datetime import datetime
from smtpd import SMTPServer
from config import HOST, PORT, MESSAGE_DIR


class TestMailServer(SMTPServer):
    count = 0  # Number of emails received

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        """
        Process a message when it is received.
        Writes the contents to a txt file in MESSAGE_DIR.
        """
        self.count += 1

        # Create filename to guarantee filename uniqueness
        filename = '%s[#%d](%s).txt' % (datetime.now().strftime('%Y-%m-%d %H;%M;%S'), self.count, rand_str())

        # Write raw data to file
        f = open(MESSAGE_DIR + '/' + filename, 'w')
        f.write(str(data))
        f.close()


def rand_str(length=6):
    """
    Generate a random string of length 6.
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def run_server(host, port):
    # Start the SMTP server on host:port
    os.makedirs(MESSAGE_DIR, exist_ok=True)  # Make directory if it does not exist
    TestMailServer((host, port), None)
    asyncore.loop()


if __name__ == '__main__':
    print("Server started ...")
    run_server(HOST, PORT)

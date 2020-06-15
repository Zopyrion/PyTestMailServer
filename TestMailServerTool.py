from datetime import datetime
from smtpd import SMTPServer
import asyncore
from config import HOST, PORT


class TestMailServer(SMTPServer):
    count = 0  # Number of emails received

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        self.count += 1
        filename = '%s-%d.txt' % (datetime.now().strftime('%Y%m%d%H%M%S'), self.count)

        # Write raw data to file
        f = open("messages/" + filename, 'w')
        f.write(str(data))
        f.close()

        print(str(self.count) + ": " + str(data))


def run(host, port):
    # start the SMTP server on host:port
    TestMailServer((host, port), None)
    asyncore.loop()
    print("Server started ...")


if __name__ == '__main__':
    run(HOST, PORT)

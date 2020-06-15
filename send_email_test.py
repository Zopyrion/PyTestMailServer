import smtplib
import multiprocessing
from email.message import EmailMessage
from config import HOST, PORT
from enum import Enum


def email_worker(num_emails, worker, mode):
    """
    An instance of an email worker to processing sending a test email.
    :param num_emails: Number of enails to send.
    :param worker: Worker number.
    :param mode: Singlethreaded or multuthreaded.
    :return:
    """
    server = smtplib.SMTP(HOST, PORT)

    for i in range(num_emails):

        # Create message
        msg = EmailMessage()
        msg['From'] = "Email Sender"
        msg['To'] = "Email Receiver"
        if mode == Mode.SINGLETHREAD:
            msg['Subject'] = "Single Threaded Test: Count #" + str(i)
            msg.set_content("This email was sent on a single thread.")
        elif mode == Mode.MULTITHREAD:
            msg['Subject'] = "Multi Threaded Test: Worker #" + str(worker) + " Count #" + str(i)
            msg.set_content("This email was sent on multiple threads.")

        server.send_message(msg)
    server.quit()


class EmailSender:

    @staticmethod
    def send_single_threaded_test(num_emails=1):
        """
        Sends *num_emails* amount of emails using a single thread.
        """
        email_worker(num_emails, 1, Mode.SINGLETHREAD)

    @staticmethod
    def send_multi_threaded_test(num_emails=1, num_threads=1):
        """
        Sends *num_emails* amount of emails by dividing workload across *num_threads* workers.
        """
        num_to_send = num_emails // num_threads

        for i in range(0, num_threads - 1):
            p = multiprocessing.Process(target=email_worker, args=(num_to_send, i + 1, Mode.MULTITHREAD))
            p.start()
        remaining = num_to_send + (num_emails % num_threads)
        p = multiprocessing.Process(target=email_worker, args=(remaining, num_threads, Mode.MULTITHREAD))
        p.start()


class Mode(Enum):
    SINGLETHREAD = 0
    MULTITHREAD = 1


if __name__ == '__main__':
    emailSender = EmailSender()
    emailSender.send_single_threaded_test(num_emails=50)
    emailSender.send_multi_threaded_test(num_emails=50, num_threads=4)

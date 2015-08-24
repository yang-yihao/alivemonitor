__author__ = 'house'

from urllib.request import urlopen
import logging
import smtplib
import time
from email.mime.text import MIMEText
from logging.handlers import RotatingFileHandler

from app import conf

# serices structure:
#   {
#       'url1': { 'available_last_time': True },
#       'url2': { 'available_last_time': False, 'retry_times': 1 }
#   }
services = dict()


class ServiceUnavailableError(Exception):
    def __init__(self, reason):
        self.reason = reason


def log_exception_elegantly(exception):
    reason = 'Exception'
    if hasattr(exception, 'reason'):
        reason = exception.reason
    logging.error(str(reason) + '\n')
    # logging.error('======== EXCEPTION STACK BEGINS ========')
    # logging.exception(exception)
    # logging.error('======== EXCEPTION STACK ENDS ========\n')


def send_email(receivers, title, url, reason, detail=''):
    logging.debug('Going to send mail.')
    content = \
        """
        URL: %s

        REASON: %s

        DETAIL: %s
        """ % (url, reason, detail)

    server_url = 'smtp.qq.com'
    sender = 'sysadmin@sietai.com'
    password = 'ovSE1s<s'
    server = smtplib.SMTP(server_url)
    # server.set_debuglevel(1)
    server.login(sender, password)
    msg = MIMEText(_text=content, _charset="utf-8")
    msg['subject'] = title
    msg['from'] = 'sysadmin@sietai.com'
    msg['to'] = ','.join(receivers)
    server.sendmail(sender, receivers, msg.as_string())
    server.quit()
    logging.info('Alert Mail [%s] sent to [%s].' % title, ', '.join(receivers))


def test_service_available(url, alert_receivers):
    global services
    service_available = True
    reason = ''
    try:
        logging.debug('monitoring ' + url)
        with urlopen(url, timeout=10) as f:
            if not f.getcode() == 200:
                service_available = False
                raise ServiceUnavailableError(f.getcode)
        logging.debug('status: OK')
    except Exception as e:
        log_exception_elegantly(e)
        service_available = False
        if hasattr(e, 'reason'):
            reason = e.reason
        else:
            reason = str(type(e))
    finally:
        s = services.get(url, None)
        if service_available is False:
            if s is None or s['available_last_time'] is True:
                # send_email(
                #     alert_receivers, 'Service Unavailable',
                #     url, reason, reason
                # )
                ns = {url: {'available_last_time': False, 'retry_times': 0}}
                services.update(ns)
            else:   # s is not None or s['available_last_time'] is False
                ns = {url: {
                    'available_last_time': False,
                    'retry_times': s['retry_times']+1}}
                services.update(ns)
                if s['retry_times'] == conf.RETRY_TIMES_FOR_DOWN:
                    logging.warning(url + ' is DOWN!')
                    send_email(
                        alert_receivers, 'Service Unavailable',
                        url, reason, reason
                    )
        else:   # service_available is True
            # TODO fix bug here
            if s is not None and \
                    s['available_last_time'] is False:
                if s['retry_times'] >= conf.RETRY_TIMES_FOR_DOWN:
                    logging.warning(url + " is UP again! YES, it's REVIVED!")
                    send_email(
                        alert_receivers, 'Service Available',
                        url, 'Service Available', 'Service Recovered.'
                    )
                else:
                    logging.warning(
                        url + " is not really dead, it's recovered again.")
                ns = {url: {'available_last_time': True, 'retry_times': 0}}
                services.update(ns)


def test_alive():
    """

    :return:
    """

    log_format = '[%(asctime)s %(levelname)s] - %(name)s - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    fmt = logging.Formatter(fmt=log_format, datefmt=datefmt)
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format, datefmt=datefmt)
    log_file_handler = \
        RotatingFileHandler(
            'logs/monitor.log',
            mode='a', encoding='utf-8',
            maxBytes=1024*1024,
            backupCount=10
        )
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(fmt=fmt)
    logging.getLogger().addHandler(log_file_handler)

    global services
    while True:
        logging.info('services status: ' + str(services))
        for item in conf.ALERTS:
            test_service_available(item['url'], item['alert_receiver'])
        time.sleep(conf.MONITOR_INTERVAL)


def start():
    """ Module entry

    :return: None
    """
    test_alive()

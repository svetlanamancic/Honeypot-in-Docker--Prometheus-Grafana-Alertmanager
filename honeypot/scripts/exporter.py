import time
from prometheus_client import start_http_server, REGISTRY
import random
from pygtail import Pygtail
import re
import os.path
from prometheus_client.core import CounterMetricFamily

class HoneypotMetricsExporter(object):
    def __init__(self):
        self._base_path = '/var/log/'
        self._log_file_path = self._base_path + 'auth.log'
        self._successful_login_file_path = self._base_path + 'successful-login.log'
        self._failed_login_file_path = self._base_path + 'failed-login.log'
        self._usernames_dict_file_path = self._base_path + 'usernames-dictionary.txt'
        self._passwords_dict_file_path = self._base_path + 'passwords-dictionary.txt'
        self._login_attempts = 0
        self._successful_login = 0
        self._failed_login = 0
        self._usernames_tried = 0
        self._passwords_tried = 0

    def collect(self):
        self.get_log_content()
        yield CounterMetricFamily('honeypot_login_attempts_total',
                                  'How many login attempts were made',
                                  self._login_attempts)
        yield CounterMetricFamily('honeypot_usernames_tried_total',
                                  'How many different usernames have been used',
                                  self._usernames_tried)
        yield CounterMetricFamily('honeypot_passwords_tried_total',
                                  'How many different passwords have been used',
                                  self._passwords_tried)
        yield CounterMetricFamily('honeypot_successful_logins_total',
                                  'How many times login has been successful',
                                  self._successful_login)
        yield CounterMetricFamily('honeypot_failed_logins_total',
                                  'How many times login has failed',
                                  self._failed_login)
        
    def increment_counter(self, path):
        if path == self._usernames_dict_file_path:
            self._usernames_tried = self._usernames_tried + 1
        else:
            self._passwords_tried += 1

    def check_for_credentials(self, term, path):
        try:
            found = False
            with open(path, 'r+') as dict:
                for line in dict:
                    if term in line:
                        found = True
                        break
                if not found:
                    dict.write(term+'\n')
                    self.increment_counter(path)
        except FileNotFoundError:
            with open(path,'w+') as dict:
                dict.write(term+'\n')
                self.increment_counter(path)


    def append_logs(self, line, path):
        with open(path, 'a') as file:
            file.write(line)

    def get_log_content(self):
        if os.path.exists(self._log_file_path):

            for line in Pygtail(self._log_file_path):
                m = re.search(".*Accepted (.*) for (.*) from (.*) port.*", line)
                if m:
                    self.append_logs(line, self._successful_login_file_path)
                    self._successful_login +=1
                    self._login_attempts += 1

                m = re.search(".* Username: (.*), Password: (.*)", line)
                if m:
                    username = m.group(1)
                    password = m.group(2)
                    self._failed_login += 1
                    self._login_attempts += 1

                    self.check_for_credentials(username, self._usernames_dict_file_path)
                    self.check_for_credentials(password, self._passwords_dict_file_path)

                    self.append_logs(line, self._failed_login_file_path)
        

if __name__ == "__main__":
    start_http_server(8000)
    REGISTRY.register(HoneypotMetricsExporter())
    while True:
        time.sleep(10)


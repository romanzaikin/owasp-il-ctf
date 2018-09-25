#!/usr/bin/python
from PIL import Image, PngImagePlugin, ImageFile

import requests
import pytesseract
import string
import re
import numexpr


def fix_captcha():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    png_file = PngImagePlugin.Image.open('captcha.png')
    width, height = png_file.size

    for i in xrange(height):
        # change captcha colors to work better with tesseract
        for k in xrange(width):
            ab = png_file.getpixel((k, i))
            if ab[0] != 255 or ab[1] != 255 or ab[2] != 255:
                png_file.putpixel((k, i), (255, 255, 255))
            else:
                png_file.putpixel((k, i), (0, 0, 0))

    png_file.save("captcha2.png")

    text = pytesseract.image_to_string(Image.open('captcha2.png'))

    # clean bad characters from captcha for example (space, backtick and so)
    return "".join(map(lambda data: data if data in string.ascii_letters or data in string.digits else "", text))


def get_captcha():
    response = requests.get(captcha_url, cookies=cookies)

    if response.status_code == 200:
        with open("captcha.png", 'wb') as f:
            f.write(response.content)


def get_number(response=None):
    if not response:
        response = requests.get(number_url, stream=True)

    for line in response.iter_lines():
        if "math_question" in line:
            re_value = re.search(">(.*?)=", line).group(1)
            return numexpr.evaluate(re_value).item()

#
# Global Configurations
#
number_url = 'http://challenges.owaspil.ctf.today:8085/'
captcha_url = "http://challenges.owaspil.ctf.today:8085/captcha.php"
cookies = dict(PHPSESSID="d2b86e03ba22bb52b850a6670da284ac")
headers = {'content-type': 'application/x-www-form-urlencoded'}

number = get_number()

while True:
    get_captcha()
    captcha = fix_captcha()

    response = requests.post(number_url,
                      cookies= cookies,
                      data= "captcha={0}&math_captcha={1}&submit=".format(captcha, number),
                      headers= headers,
                      stream= True)

    if "Oh snap! you are wrong!" in response.text:
        print "[-] Bad captcha!"
    elif "Correct!" in response.text:
        print "[+] Correct!"
    else:
        flag = re.search("{(.+?)}", response.text).group(1)
        print "[*] FLAG: OWASP-IL{{{0}}}".format(flag)

        raw_input("[*] Done!")


    # set new number
    number = get_number(response)

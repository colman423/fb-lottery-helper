import time
from urllib.parse import urlparse


def get_input(text, valid_value=[]):
    while True:
        command = input(text)
        try:
            if(command in valid_value or valid_value == []):
                return command
            else:
                raise ValueError
        except ValueError:
            print("pls enter valid option")


def get_clean_url(url):
    # print(url)
    o = urlparse(url)
    # print(o.scheme, o.netloc, o.path)
    # clean = o.scheme + "://" + o.netloc + o.path
    clean = o.path
    if o.path == "/profile.php":
        id = o.query.split('&')[0]
        clean += '?'+id
    # print(clean)
    return clean

def full_to_half(s): 
    n = []
    # s = s.decode('utf-8') 
    for char in s: 
        num = ord(char) 
        if num == 0x3000: 
            num = 32 
        elif 0xFF01 <= num <= 0xFF5E: 
            num -= 0xfee0 
        num = chr(num) 
        n.append(num) 
    return ''.join(n)
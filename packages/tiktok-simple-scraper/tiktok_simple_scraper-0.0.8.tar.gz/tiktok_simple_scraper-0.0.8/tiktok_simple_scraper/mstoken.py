import base64
import os
import random
from http import cookies
from json import dumps
from random import randint
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from time import time

import requests

from tiktok_simple_scraper.x_bogus import USERAGENT


class MsTokenTikTok:
    REFERER = "https://www.tiktok.com/"
    HEADERS = {"Origin": REFERER[:-1], "Referer": REFERER, "user-agent": USERAGENT}
    API = "https://mssdk.tiktokw.us/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "3ZupDP37y+4Kyc0U9G3Mh/CMaHlAUVC/kX18BspqRG+ISe8G2GZkbPlm5P2YzanhYaeT6u9AKB9BX2HX20SYpgfwea7fmUysF"
                   "lqR7HyWZKpfZTeLvi38zog1p3slqQ45rNrzHWh2HuFxuql6bAGYFHhFC6Rvj8nR/eCLYC62AGEH3WdQ/VLESxzeSAHqS5wP1b"
                   "uBmreS8DtIMssZtrt8YQRgmmxH+6hZqut3WLDtImFnz9YISD8A7MUFZ9Djti32ny4L6v70R9vE6DlwJ0SJDceZgI52FiKADJ4"
                   "64qRRiuUBrVdwx/8+g53tOKbhHOPNEi/zUmqcOPrrjXL8OnHBis6/G7kkE//LMRPa1LtBfQUVeSACknbl+wycWBo5TXbir+dH"
                   "Qxe5BI94CnibgUo4QnK7VEebkAJPwB2T2LiyfIpn5BCJQGaZJVAahTeI+SjTlsx7Hqtq6ECahAc5VQRJsGDI6XE7DvVKDOGAN"
                   "3I+cAeEksuCO7o90F8pT+xK9QuKUW/0/etSSDk3Zw+RL9fG5KcRldnw9zRSynGwCnJigxFWm8DtttFeI7zCnM/+KSppb4rJ8s"
                   "gw2YDQ113OroCjpRcZRJCa29mj8CiBAMGj0NWtQvoFWQszQd3ilBlVHAAO4Ci4GEyjO+XtBOOGYqjCCWZElhrwrFL8f2QTaNE"
                   "aNsXsDNWPmdQBEuHhx2iFFU0/e1uJ+AKVSIQh/b3+IZE3/kJPMMVuF0NFoL5DQnUJfLhmdhZV0QHQr1tvJoQr3E+bOtNElKmJ"
                   "wyZUyoCYn4ADWv+sP8rZTMcRoFka7lqoKXqO88dcvDcmReJtFbXe9TLilWpRxKxwbD2q6JgNPqSk2ZRlynfZVVVmu3wG1wxZn"
                   "1mAxTlPMR2VQvPRkWH2iN2nuftP4BPleZBvfMVXU9tTPxNpl72yVYGOZQtl3AGwttCJ40C2usy2dfmXahZQbRsr8QQnBLmloK"
                   "r0nXqlkrJoKVYVJArOlYR61Im2yOHVOgHw6vyvegFtK8Z3wkvr3tzj8OpxqjIj4P9YQwMjudVn8q/8m3zDKwSL2+1NDsebSHY"
                   "juTyeqtooaJChEu1KkGwaD6hZxlGTyKpnyU4Gwa6OVtHTSv7Z7Zugy08ehYP07/5lsccdiDVRNg2doS54j9evmfVumBG41iIP"
                   "6m7xxfcnTFrkJa8rtda5DaBPiWcd5yfWzhW9ab3u55SGN1/pq7VC+MAoSv0LUEpCCksRMhay9FHFq4lxAs2hNW1L5pbXkmx1y"
                   "H5AIaWXDLKu+qXK2WcutNl+GGDJJvmfvilz3H6P7Oic90ts8AMMptaY6I+znzUsTYmRke8FR80Ioa8Uenl1j/U0QFOnaeLwrj"
                   "+j3nEr3mL/2ibdqsfG0tpM+yjFePOYTkiP9Lh2S0zwk0KpEtDF9O2hDZAZJu7XiNg32XcYKaq6jjfyvnbOldKnJ5RpZD68xyy"
                   "LUSYXW0P1Axd85xlJHU0oT+S6q6GnYAEohU3dGWI9yiTEjtJ1b5PiLYPz3rxMGwXVKcn6WNWe9wugUF2i2DwRYt5bjuXCNkOO"
                   "70XOS7xbJlQpoCK0F0y38VwF0oEyFY9GG2W2ZJa6gHazqBMniVYetJqR9PwaGj7Z3rNRuITu+yJYNH7pGSbLUucg5tPqrttG6"
                   "TBWUF1OZaq3vpOiZoHniSouUJMwUCJ4DsPHvK1nJh5FSUsbUQAtTtHaCPYK4jTIJY0XHo/uqNe8bMBCzCQRrWKSgvWOYKBnyb"
                   "lScGoDMvZnuZG+I7DFa8bRdBmbwCW7cDhlT0wRobax9ADggpG9yQ6b0lMJ42MtR/axFpusCYF1dHTywtos8+2+Refj1C5FHWM"
                   "6FIYBCSIjS+SXgHYm0nUfM20oMg4p4C4YnGcuTeU5vdNdsc//YSN9ivatjzMMQ4g+9upjVMlOJ57mDlRKnZ6bvGc2af4qU/kD"
                   "Nj3FN5VntlLvInpyFVz5Ytik/TNLalzywo+o5sYsFk/RlnAwyoSsfMFdZnEATnHTF+IBI1KNjkmOEC4MMnXUtQr59DEKgyUUO"
                   "dKUIoGDOCS5Onv4F6dcw6CGBWcA8+f6TTQ48fsHd0Qvud471+XaTLHJK42Pwn1++XmDTvL0cywadk9WbzT9arlX6uIC+K5FWL"
                   "YqaYGB+jgakCTVyy1Vh1Lo60uR6AVjg++vF+2OuiFmPH7eXD2YwECYbh5ngGFBrF5Qt53GqWCGXi/PX5apDJDj9HZ/Kbadg+h"
                   "bjJQmLX/WVq1LfiRZlT9KTTfOfDdIV6/Z4b0UKLFYnwibAp7Fl4XWi6NGhLB7p93fXM9MjAK7az5xhqQfwf79o2WD1hB+n/A/"
                   "SOPU5uqUYib+j9Pv6WxekJmKRq4uwPrvwjtWVKsLQHlNpY9fl/sGuE692IQaQ2IiWdJ9R4D0T53yv9WZ0BUue5YNoo888pVAt"
                   "X211S7knFUxqXMjtI+XfgRu/q4IusDOwS1tFQrnI0LzzZoCMFih8q4lh/DmWV4K5Qwl4n1dvUPqsQU32pf0lKnEZUIZwYg4iG"
                   "8TFTUh6ki0+lCP/xX6kL5MfCLPRcOLfIBglLFQph+xVjZvfhPUeDyYZwamS11Nv6N19Dq3nBhyMia2x5UwxHoy7Lmnj3y9dFk"
                   "D3bNa3hgo17u1LVSmUZR0kUIj8ACAkAezLxTLe8LdOkW07xGeZekWYqmchSs2StUaA3poBf/KQn5YwIOZRxmAEps3yZ55Wceg"
                   "hGOVMAlXZtTyBMWufGaRPEFUPbdo3BS9RWehau4nrQslfio8r1+6rXKvCtd/E3yRKzZqTaglGXwVWMwEDLMKQnDZSnmFrSyb4"
                   "yFVlExhlP9FsQWQyM0VAE6seHL55dKtrceUWtWCYVahlU9c0g1eeK4PR5cxyG99EOKowFhJYXlTS38UlefpEXNhjeExeT5hgh"
                   "k56vZiqnOpNcvM6hOATflZem1rpKA6nt9V2reDTX+A4V8xHi0gxZU/GNZeT9U/A7m7RTPj5Ix1xoh/BDF3pUUpjSK1mjZzjzi"
                   "tJqmJTLS6bKmpb87Jfm+b2RmHPnsF51uBgWsVa1ZHM9YscveEdHOPX0EmOZH8WIwV2JAf8h+n8REuxFTeZe9odGUBB3haiA40"
                   "ATwy8D9cxDLEwKkTFBEOrlKB33TkqLtE6d8cMRInPcxbIva7sg+P/Odwcj5reLEkBTnbPaEexjPOHGvV336VKFr4XNgyAO74d"
                   "CgyyVEh+drf3t8u7ZfHHfCpf0tQnNK9wnzyd4O77E2BsllNY18EGyuw9kF7eWXPwlUJUlDVtGMO0/QzQYeXq29h5h9nEKH/GK"
                   "vJ6V1ncJ8exlP6NYt4bF+QVbBJNQ9LwKebLmLMLImi8JmpK9qBNwHXsoJWqwAIRvFPt4vOMISRqFIENK0J0FCfx7Va7JqKLsL"
                   "wpz1obUOJksFUdljivum6MhpZlwuGJxKqZiW97+ik6YP1Dq43quSIRBYp1rVS36YTRRlqYUS2ana5TiKBYQ8OheNruzQGj7ds"
                   "NNJqt94Nm/hpjOOk5Q7tggqruCgYiLHQ9nz69qcrkW3Mxl1VvrM5kmv1HCafqyoq/VjgU05M1sksy6rwp32gft+C/i4GN31Et"
                   "JkHQ3ZGXRj/RHCdDD+VKm0E7QN6HfTk+ZB6nUEDbmTrIXfYxyMh4jWuQVhWKBkLHWxyuvrAIMFnQ7x2XRdcDKTXJw+mLOr02G"
                   "ZvfuBRInG5vVR47jbbUw1+8DiMdgPpNP7ig9OfDkSmCqMI9SjDN6+zOQxm7rRnaCOj+RO+9MzNXPLA0V1a0WH2xv9YV/KKSXu"
                   "9DS8MOpXkKKY5MWDgzUEB0TVX5/zfVKgNDiN/BJL5hoJADMKTIePWhABcv/tHYk1fBNMiHHgQLZ/ui5+VP+MN4ESDk02UEigC"
                   "uD0lH4YEk5gLC8U0uMJJFiS0BDI9e74P9RMr3OeITTE86Tga9PEkvxYL+AoggZBjkJ0AFdgzKZgiWpUEZvTsOAVHkPcjqzql9"
                   "87PaNEiHeTWd/aBYT4ZJOq5Tiy0jDxJq1KODjVdzUkG24Jygr0KTlLu9gxPZeL/BKy9k8cnHFXhs9sDf4YvWFeCkZ3XjUN0S8"
                   "MDEkCSY1lh4mZUrtmAwiLjs79aVRp+Z2jCkf94AkkT7lqQG49mJp8Hi6QcUM+sYyHZonWFtRH6Nkqob3GQ4JIXmKre8aQD0a9"
                   "PWI/NF2vWcfk33UanMAx/ltDJX85n5DGUYQx1sf/Yff13j8iSa66QJk8Ox3uDTs0ZLpcoqTR8cj/xM/cqiC25uuW/OLeNwXJX"
                   "8HHAd1/fXiIDXQA89w/yAc9O1TSsgNY8dAZYhoRa7FCdr+SSYLdJWEXq+cMyka6Xb97qn0v0jAVyeM7ZSmo00/fGrsQTrhgjD"
                   "OorzfstHkCsyc6jI7WFXoU2X1jvTDDdFZa+j2kaIpSWvn5SOl5N4viverF7FDtVFcRL10cWSQWcMrt6vP8R5qM2fC+0zwrBqR"
                   "dcB1GshBV08YqJvXYY83wNIPCwFqmO/9NVm5PqNAEPdlH8WPnk6onXbwenFB1J",
    }

    @staticmethod
    def get_fake_ms_token(key="msToken", size=107) -> dict:
        base_str = digits + ascii_uppercase + ascii_lowercase
        length = len(base_str) - 1
        return {key: "".join(base_str[randint(0, length)]
                             for _ in range(size))}

    @classmethod
    def get_real_ms_token(cls) -> str:
        payload = dumps(cls.DATA | {"tspFromClient": int(time() * 1000)})
        response = requests.request("POST", cls.API, headers=cls.HEADERS, data=payload)
        mstoken = cls.extract(response.headers, "msToken")
        return mstoken.get("msToken")

    @staticmethod
    def generate_mstoken():
        ms = base64.b64encode(os.urandom(random.randrange(91, 100))) \
            .decode().replace('+', '9').replace('/', '9').rstrip('=')
        if len(ms) <= 128:
            ms += '=='
        while len(ms) < 132:
            i = random.randrange(128)
            c = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            p = random.choice('-_')
            ms = ms[:i] + ms[i:].replace(c, c + p, 1)
        return ms

    @staticmethod
    def extract(headers, key: str) -> dict | None:
        if c := headers.get("Set-Cookie"):
            cookie_jar = cookies.SimpleCookie()
            cookie_jar.load(c)
            if v := cookie_jar.get(key):
                return {key: v.value}

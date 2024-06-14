from base64 import b64encode
from hashlib import md5
from time import time
from typing import List
from urllib.parse import urlencode

USERAGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


class XBogus:
    """
    This class is responsible for generating the x-bogus header used in TikTok requests.
    """
    __string = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="
    __array = [None for _ in range(
        48)] + list(range(10)) + [None for _ in range(39)] + list(range(10, 16))
    __canvas = 3873194319

    def get_x_bogus(
            self,
            query: dict,
            user_agent=USERAGENT,
            time_to_take: int = None):
        if time_to_take is not None:
            timestamp = int(time_to_take)
        else:
            timestamp = int(time())
        query = self._process_url_path(urlencode(query))
        return self._generate_x_bogus(query, 8, user_agent, timestamp)

    @staticmethod
    def _disturb_array(a: List[int]) -> List[int]:
        return [
            a[0], a[2], a[4], a[6], a[8],
            a[10], a[12], a[14], a[16], a[18],
            a[1], a[3], a[5], a[7], a[9],
            a[11], a[13], a[15], a[17]
        ]

    @staticmethod
    def _generate_garbled_str_1(a: List[int]) -> str:
        disturbed_array = [
            a[0], a[10], a[1], a[11], a[2],
            a[12], a[3], a[13], a[4], a[14],
            a[5], a[15], a[6], a[16], a[7],
            a[17], a[8], a[18], a[9]
        ]
        return "".join(map(chr, map(int, disturbed_array)))

    @staticmethod
    def _generate_num_from_garbled(text: str) -> List[int]:
        return [
            ord(text[i]) << 16 | ord(text[i + 1]) << 8 | ord(text[i + 2]) << 0
            for i in range(0, 21, 3)
        ]

    @staticmethod
    def _generate_garbled_str_2(a, b) -> str:
        d: List[int] = list(range(256))
        c = 0
        f = ""
        for b_idx in range(256):
            c = (c + d[b_idx] + ord(a[b_idx % len(a)])) % 256
            e = d[b_idx]
            d[b_idx] = d[c]
            d[c] = e
        t = 0
        c = 0
        for b_idx in range(len(b)):
            t = (t + 1) % 256
            c = (c + d[t]) % 256
            e = d[t]
            d[t] = d[c]
            d[c] = e
            f += chr(ord(b[b_idx]) ^ d[(d[t] + d[c]) % 256])
        return f

    @staticmethod
    def _generate_garbled_str_3(a: int, b: int, c: str) -> str:
        return chr(a) + chr(b) + c

    def _calculate_md5(self, input_string: str | list) -> str:
        if isinstance(input_string, str):
            array = self._md5_to_array(input_string)
        elif isinstance(input_string, list):
            array = input_string
        else:
            raise TypeError

        md5_hash = md5()
        md5_hash.update(bytes(array))
        return md5_hash.hexdigest()

    def _md5_to_array(self, md5_str):
        if isinstance(md5_str, str) and len(md5_str) > 32:
            return [ord(char) for char in md5_str]
        else:
            return [
                (self.__array[ord(md5_str[index])] << 4)
                | self.__array[ord(md5_str[index + 1])]
                for index in range(0, len(md5_str), 2)
            ]

    def _process_url_path(self, url_path):
        return self._md5_to_array(
            self._calculate_md5(self._md5_to_array(self._calculate_md5(url_path)))
        )

    def _generate_str(self, num):
        string = [num & 16515072, num & 258048, num & 4032, num & 63]
        string = [i >> j for i, j in zip(string, range(18, -1, -6))]
        return "".join([self.__string[i] for i in string])

    @staticmethod
    def _handle_ua(a, b):
        da: List = list(range(256))
        c = 0
        result = bytearray(len(b))

        for i in range(256):
            c = (c + da[i] + ord(a[i % len(a)])) % 256
            da[i], da[c] = da[c], da[i]

        t = 0
        c = 0

        for i in range(len(b)):
            t = (t + 1) % 256
            c = (c + da[t]) % 256
            da[t], da[c] = da[c], da[t]
            result[i] = b[i] ^ da[(da[t] + da[c]) % 256]

        return result

    def _generate_ua_array(self, user_agent: str, params: int) -> list:
        ua_key = ['\u0000', '\u0001', chr(params)]
        value = self._handle_ua(ua_key, user_agent.encode("utf-8"))
        value = b64encode(value)
        return list(md5(value).digest())

    def _generate_x_bogus(
            self,
            query: list,
            params: int,
            user_agent: str,
            timestamp: int):
        ua_array = self._generate_ua_array(user_agent, params)
        array = [
            64,
            0.00390625,
            1,
            params,
            query[-2],
            query[-1],
            69,
            63,
            ua_array[-2],
            ua_array[-1],
            timestamp >> 24 & 255,
            timestamp >> 16 & 255,
            timestamp >> 8 & 255,
            timestamp >> 0 & 255,
            self.__canvas >> 24 & 255,
            self.__canvas >> 16 & 255,
            self.__canvas >> 8 & 255,
            self.__canvas >> 0 & 255,
            None,
        ]
        zero = 0
        for i in array[:-1]:
            if isinstance(i, float):
                i = int(i)
            zero ^= i
        array[-1] = zero
        garbled_1 = self._generate_garbled_str_1(self._disturb_array(array))
        garbled_2 = self._generate_garbled_str_2("ÿ", garbled_1)
        garbled_3 = self._generate_garbled_str_3(2, 255, garbled_2)
        return "".join(self._generate_str(i) for i in self._generate_num_from_garbled(garbled_3))

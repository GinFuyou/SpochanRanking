from random import randint

from checkdigit import verhoeff
from django.utils import timezone
from unidecode import unidecode

# from simple_history.models import HistoricalRecords
DIGITS = {c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyz'.upper())}
BASE_YEAR = timezone.datetime(1920, 1, 1)
ENC_BASE = len(DIGITS)


class ChanCode():
    template = "{initial}{check}{version}{randnum:0>4}{enc_year}"
    RANDNUM_LIMITS = (0, 9999)
    VALID_VERSIONS = (1, )

    def __init__(self, profile=None, first_name='', last_name='', date_of_birth=None):

        self.year_offset = None
        self.first_name = ""
        self.last_name = ""
        if profile:
            if profile.date_of_birth:
                self.year_offset = profile.date_of_birth.year - BASE_YEAR.year
            self.first_name = profile.first_name
            self.last_name = profile.last_name

        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if date_of_birth:
            self.year_offset = date_of_birth.year - BASE_YEAR.year

        self._encoded = ""
        self._encoded_name = ""
        self._encoded_year = ""
        self._randnum = 0

    @property
    def is_filled(self):
        return all([self.year_offset, self.first_name, self.last_name])  # WARNING consider unique human name systems

    def encode(self, version=1):
        if version not in self.VALID_VERSIONS:
            raise NotImplementedError(f"ChanCode version {version} is not implemented")

        if not self.is_filled:
            raise RuntimeError("Tried to encode not fully filled ChanCode")

        if not self._encoded:
            self._encoded_year = self.encode_year_offset()
            self._encoded_name = self.encode_name()
            if not self._randnum:
                self._randnum = randint(*self.RANDNUM_LIMITS)

            check_string = f"{version}{self._randnum:0>4}{self.year_offset}"
            check = verhoeff.calculate(check_string)
            # print(f"check: {check} for {check_string}")  # TESTING

            self._encoded = self.template.format(
                initial=self._encoded_name,
                version=version,
                randnum=self._randnum,
                check=check,
                enc_year=self._encoded_year
            )

        return self._encoded

    @staticmethod
    def format_static(string):
        return f"{string[:2]}-{string[2:4]}-{string[4:8]}-{string[8:]}"

    def format(self):
        string = self.encode()
        return ChanCode.format_static(string)

    def encode_name(self):
        string = unidecode(self.first_name)[0] if self.first_name else 'X'
        string += unidecode(self.last_name)[0] if self.last_name else 'X'
        return string

    def encode_year_offset(self):
        number = self.year_offset // ENC_BASE
        remainder = self.year_offset % ENC_BASE
        encoded_offset = [chr(remainder + ord('A'))]
        while number > 0:
            year_offset = number
            number = year_offset // ENC_BASE
            remainder = year_offset % ENC_BASE
            encoded_offset.insert(0, chr(remainder + ord('A')))
        return "".join(encoded_offset)

        # number = reversed(number.upper())
        # return BASE_YEAR.year + sum(DIGITS[digit] * (base ** i) for i, digit in enumerate(number))

    @staticmethod
    def decode_year_offset(string):
        ord_shift = ord('A')
        number = (ord(string[-1]) - ord_shift)
        counter = 0
        while len(string) > 1:
            string = string[:-1]
            counter += 1

            number += (ord(string[-1]) - ord_shift) * (ENC_BASE**counter)
        return number

    @staticmethod
    def validate(string):
        string = string.replace("-", "").replace(" ", "").upper()
        year_offset = ChanCode.decode_year_offset(string[-2:])
        check_digit = string[2]
        string = string[3:-2] + str(year_offset) + check_digit
        print(f"verhoeff code: {string}")
        return verhoeff.validate(string)

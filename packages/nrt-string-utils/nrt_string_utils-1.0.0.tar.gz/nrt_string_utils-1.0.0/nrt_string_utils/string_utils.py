import base64
import json
import re
from typing import Optional


class StringUtil:

    @staticmethod
    def decode_base64(encoded_text: str) -> str:
        utf_8 = encoded_text.encode('utf-8')
        utf_8 = base64.b64decode(utf_8)
        return utf_8.decode('utf-8')

    @staticmethod
    def encode_base64(text: str) -> str:
        utf_8 = text.encode('utf-8')
        base_64 = base64.b64encode(utf_8)
        return base_64.decode('utf-8')

    @staticmethod
    def get_char_and_ascii_number_pairs(text: str) -> list:
        return [(char, ord(char)) for char in text]

    @staticmethod
    def get_emails(text: str) -> list:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        return list(set(emails))

    @staticmethod
    def get_last_char(s: str) -> str:
        return s[-1] if len(s) else ''

    @staticmethod
    def get_urls(text: str) -> list:
        pattern = \
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]'\
            '|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(pattern, text)
        return list(set(urls))

    @classmethod
    def is_decimal(cls, s: Optional[str]) -> bool:
        if s is None:
            return False

        if s != s.strip():
            return False

        if cls.get_last_char(s) == '.':
            return False

        try:
            float(s)
        except ValueError:
            return False

        return True

    @staticmethod
    def is_int(s: Optional[str]) -> bool:
        if s is None:
            return False

        if s != s.strip():
            return False

        try:
            int(s)
        except ValueError:
            return False

        return True

    @staticmethod
    def is_json(text) -> bool:
        try:
            json.loads(text)
        except ValueError:
            return False

        return True

    @classmethod
    def is_positive_decimal(cls, s: Optional[str]) -> bool:
        return float(s) > 0 if cls.is_decimal(s) else False

    @classmethod
    def is_positive_int(cls, s: Optional[str]) -> bool:
        return int(s) > 0 if cls.is_int(s) else False

    @classmethod
    def is_unsigned_decimal(cls, s: Optional[str]) -> bool:
        return float(s) >= 0 if cls.is_decimal(s) else False

    @staticmethod
    def is_unsigned_int(s: Optional[str]) -> bool:
        return s.isdigit() if s is not None else False

    @staticmethod
    def sub_string(
            text: str,
            start_delimiter: str,
            end_delimiter: Optional[str] = None) -> str:

        if end_delimiter is None:
            pattern = re.escape(start_delimiter) + '(.*)'
        else:
            pattern = re.escape(start_delimiter) + '(.*?)' + re.escape(end_delimiter)

        matches = re.finditer(pattern, text)
        match = next(matches, None)
        return match.group(1) if match else ''

    @staticmethod
    def sub_string_list(
            text: str, start_delimiter: str, end_delimiter: str) -> list:

        pattern = re.escape(start_delimiter) + '(.*?)' + re.escape(end_delimiter)
        matches = re.findall(pattern, text)
        return matches

    @staticmethod
    def to_ascii(text: str) -> str:
        return text.encode('ascii', 'ignore').decode('ascii')

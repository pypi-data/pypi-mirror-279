import hashlib
import re

from src.cjlutils.models.StandardEncodings import StandardEncodingsEnum


def contains(string: str, sub: str) -> bool:
    """
    判断字符串是否包含子串
    :param string: 字符串
    :param sub: 子串
    :return: 是否包含
    """
    if string is None or sub is None:
        return False
    return string.find(sub) != -1


def from_bytes(b: bytes, encode: str | StandardEncodingsEnum = StandardEncodingsEnum.UTF_8) -> None | str:
    """
    字节流转字符串
    :param b: 字节流
    :param encode: 编码
    :return:
    """
    if b is None:
        return None
    encode_str = ''
    if isinstance(encode, StandardEncodingsEnum):
        encode_str = encode.value.get_name()
    elif isinstance(encode, str):
        encode_str = encode
    return b.decode(encode_str)


def index_of_first(string: str, substring: str) -> int:
    """
    获取字符串中第一个子串的索引
    :param string: 字符串
    :param substring: 子串
    :return: 第一个子串的索引
    """
    if string is None or substring is None:
        return -1
    return string.find(substring)


def index_of_first_number(string: str) -> int:
    """
    获取字符串中第一个数字的索引
    :param string: 字符串
    :return: 第一个数字的索引
    """
    if string is None:
        return -1
    for i in range(len(string)):
        if string[i].isdigit():
            return i
    return -1


def index_of_first_small_case_alpha(string: str) -> int:
    """
    获取字符串中第一个小写字母的索引
    :param string: 字符串
    :return: 第一个小写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string)):
        if string[i].islower():
            return i
    return -1


def index_of_first_big_case_alpha(string: str) -> int:
    """
    获取字符串中第一个大写字母的索引
    :param string: 字符串
    :return: 第一个大写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string)):
        if string[i].isupper():
            return i
    return -1


def index_of_last(string: str, substring: str) -> int:
    """
    获取字符串中最后一个子串的索引
    :param string: 字符串
    :param substring: 子串
    :return: 最后一个子串的索引
    """
    if string is None or substring is None:
        return -1
    return string.rfind(substring)


def index_of_last_number(string: str) -> int:
    """
    获取字符串中最后一个数字的索引
    :param string: 字符串
    :return: 最后一个数字的索引
    """
    if string is None:
        return -1
    for i in range(len(string) - 1, -1, -1):
        if string[i].isdigit():
            return i
    return -1


def index_of_last_small_case_alpha(string: str) -> int:
    """
    获取字符串中最后一个小写字母的索引
    :param string: 字符串
    :return: 最后一个小写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string) - 1, -1, -1):
        if string[i].islower():
            return i
    return -1


def index_of_last_big_case_alpha(string: str) -> int:
    """
    获取字符串中最后一个大写字母的索引
    :param string: 字符串
    :return: 最后一个大写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string) - 1, -1, -1):
        if string[i].isupper():
            return i
    return -1


def is_empty(string: None | str) -> bool:
    """
    判断字符串是否为空，None或者长度为0
    :param string: 字符串
    :return: 是否为空
    """
    return string is None or len(string) <= 0


def md5(string: str) -> str:
    hash_object = hashlib.md5(string.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


def to_bytes(string: None | str, encode: StandardEncodingsEnum | str = StandardEncodingsEnum.UTF_8) -> None | bytes:
    """
    字符串转字节流
    :param string: 字符串
    :param encode: 编码类型， 见https://docs.python.org/3.13/library/codecs.html#standard-encodings
    :return: 字节流
    """
    if string is None:
        return None
    encode_str = ''
    if isinstance(encode, StandardEncodingsEnum):
        encode_str = encode.value.get_name()
    elif isinstance(encode, str):
        encode_str = encode
    return string.encode(encode_str)


def to_camel_case(string: None | str) -> None | str:
    """
    下划线格式转换为驼峰格式
    :param string: 下划线格式字符串
    :return: 驼峰格式字符串
    """
    if string is None:
        return None
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_int(string: None | str) -> None | int:
    """
    字符串转整数
    :param string: 字符串
    :return: 整数
    """
    if string is None:
        return None
    try:
        return int(string)
    except ValueError:
        return None


def to_snake_case(string: None | str) -> None | str:
    """
    驼峰格式转换为下划线格式
    :param string: 驼峰格式字符串
    :return: 下划线格式字符串
    """
    if string is None:
        return None
    # 大写字母前面是大小写字母或者数字时，在大写字母前加上下划线
    s1 = re.sub('([A-Za-z0-9])([A-Z])', r'\1_\2', string)
    # 上面匹配两个字符，导致连续两个大写字母之间可能不会被下划线分割，需要再做一次。
    s1 = re.sub('([A-Za-z0-9])([A-Z])', r'\1_\2', s1)
    return s1.lower()

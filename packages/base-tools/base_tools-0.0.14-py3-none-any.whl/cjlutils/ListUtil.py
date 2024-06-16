def classify(l: list, classifier: callable) -> dict:
    result = dict()
    for data in l:
        data_type = classifier(data)
        if result.__contains__(data_type):
            result[data_type].append(data)
        else:
            result[data_type] = [data]
    return result


def find_all(l: list, predicate: callable) -> list:
    result = list()
    for data in l:
        if predicate(data):
            result.append(data)
    return result


def firstElement(l: list) -> any:
    if l is None or len(l) == 0:
        return None
    return l[0]


def get_distribution(l: list[tuple[any, any]]) -> dict[any, int]:
    result = dict()
    if l is None or l.__len__() == 0:
        return result
    for entry in l:
        if entry.__len__() != 2:
            continue
        key = entry[0]
        if result.__contains__(key):
            result[key] += 1
        else:
            result[key] = 1
    return result


def lastElement(l: list) -> any:
    if l is None or len(l) == 0:
        return None
    return l[-1]


def random_order(l: list) -> list:
    import random
    random.shuffle(l)
    return l


def to_string(l: list, separator: str = ',', prefix: str = '', suffix: str = '', transformer: callable = None) -> str:
    if l is None or l.__len__() == 0:
        return ''
    separator = '' if separator is None else separator
    prefix = '' if prefix is None else prefix
    suffix = '' if suffix is None else suffix

    result = ''
    for data in l:
        result += separator + str(transformer(data) if transformer is not None else data)
    return f'{prefix}{result[len(separator):]}{suffix}'


def transform(l: list, transformer: callable) -> list:
    result = list()
    for data in l:
        result.append(transformer(data))
    return result
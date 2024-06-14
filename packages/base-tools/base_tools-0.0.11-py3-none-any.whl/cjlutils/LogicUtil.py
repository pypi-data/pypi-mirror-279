def get_union_of_line_segment_int(l: list[tuple[int, int]]) -> tuple[int, int]:
    """
    获取线段的并集
    :param l: 线段列表，线段的首尾分别由一个整数表示，为半必半开区间
    :return: 线段的并集，半必半开区间
    """
    if l is None or len(l) == 0:
        return tuple()
    start = l[0][0]
    stop = l[0][1]
    for i in range(1, len(l)):
        if l[i][0] < start:
            start = l[i][0]
        if l[i][1] > stop:
            stop = l[i][1]
    return start, stop


def get_intersection_of_line_segment_int(l: list[tuple[int, int]]) -> tuple[int, int]:
    """
    获取线段的交集
    :param l: 线段列表，线段的首尾分别由一个整数表示，为半必半开区间
    :return: 线段的交集，半必半开区间
    """
    if l is None or len(l) == 0:
        return tuple()
    start = l[0][0]
    stop = l[0][1]
    for i in range(1, len(l)):
        if l[i][0] > start:
            start = l[i][0]
        if l[i][1] < stop:
            stop = l[i][1]
        if start >= stop:
            return tuple()
    return start, stop

from textwrap import wrap
from bisect import bisect_left


def format_long_link(link, width=15):
    splitted = wrap(link, width=width)
    result = ""
    for item in splitted:
        result += item + "\n"
    return result


def count_availability(statuses):
    statuses = sorted(statuses)
    count = bisect_left(statuses, 400) - bisect_left(statuses, 200)
    return count / len(statuses)

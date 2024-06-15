from __future__ import print_function
from datetime import datetime
from time import time
import medatetime

RFC3339_DATE = '2016-07-18'
RFC3339_TIME = '12:58:26.485897+02:00'
RFC3339_DATE_TIME = RFC3339_DATE + 'T' + RFC3339_TIME
RFC3339_DATE_TIME_DTLIB = RFC3339_DATE_TIME[:-6]
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
DATETIME_OBJ = datetime.strptime(RFC3339_DATE_TIME_DTLIB, DATE_TIME_FORMAT)
TIME = time()


def benchmark_parse():
    def datetime_strptime():
        datetime.strptime(RFC3339_DATE_TIME_DTLIB, DATE_TIME_FORMAT)

    def medatetime_parse():
        medatetime.from_string(RFC3339_DATE_TIME)

    return (datetime_strptime, medatetime_parse)


def benchmark_format():
    def datetime_strftime():
        DATETIME_OBJ.strftime(DATE_TIME_FORMAT)

    def medatetime_format():
        medatetime.to_string(DATETIME_OBJ)

    return (datetime_strftime, medatetime_format)


def benchmark_utcnow():
    def datetime_utcnow():
        datetime.utcnow()

    def medatetime_utcnow():
        medatetime.utcnow()

    return (datetime_utcnow, medatetime_utcnow)


def benchmark_now():
    def datetime_now():
        datetime.now()

    def medatetime_now():
        medatetime.now()

    return (datetime_now, medatetime_now)


def benchmark_utcnow_to_string():
    def datetime_utcnow_to_string():
        datetime.utcnow().strftime(DATE_TIME_FORMAT)

    def medatetime_utcnow_to_string():
        medatetime.utcnow_to_string()

    return (datetime_utcnow_to_string, medatetime_utcnow_to_string)


def benchmark_now_to_string():
    def datetime_now_to_string():
        datetime.now().strftime(DATE_TIME_FORMAT)

    def medatetime_now_to_string():
        medatetime.now_to_string()

    return (datetime_now_to_string, medatetime_now_to_string)


def benchmark_fromtimestamp():
    def datetime_fromtimestamp():
        datetime.fromtimestamp(TIME)

    def medatetime_fromtimestamp():
        medatetime.fromtimestamp(TIME)

    return (datetime_fromtimestamp, medatetime_fromtimestamp)


def benchmark_utcfromtimestamp():
    def datetime_utcfromtimestamp():
        datetime.utcfromtimestamp(TIME)

    def medatetime_utcfromtimestamp():
        medatetime.utcfromtimestamp(TIME)

    return (datetime_utcfromtimestamp, medatetime_utcfromtimestamp)

if __name__ == '__main__':
    import timeit

    benchmarks = [
        benchmark_parse,
        benchmark_format,

        benchmark_utcnow,
        benchmark_now,

        benchmark_utcnow_to_string,
        benchmark_now_to_string,

        benchmark_fromtimestamp,
        benchmark_utcfromtimestamp,
    ]

    print('Executing benchmarks ...')

    for k in benchmarks:
        print('\n============ %s' % k.__name__)
        mins = []

        for func in k():
            times =\
                timeit.repeat('func()', setup='from __main__ import func')
            t = min(times)
            mins.append(t)

            print(func.__name__, t)

        win = False
        if mins[0] > mins[1]:
            win = True

        mins = sorted(mins)
        diff = mins[1] / mins[0]

        if win:
            print('medatetime is %.01f times faster' % diff)
        else:
            print('medatetime is %.01f times slower' % diff)

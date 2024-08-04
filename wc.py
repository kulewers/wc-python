#!/usr/bin/python3

import getopt, sys
from collections import OrderedDict

options = 'clwm'


def main():
    try:
        optlist, rest = getopt.getopt(sys.argv[1:], options)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    print_counts = []

    if len(optlist) == 0:
        optlist, _ = getopt.getopt(['-c', '-l', '-w'], options)

    for o, _ in optlist:
        if o == '-l':
            print_counts.append('lines')
        elif o == '-w':
            print_counts.append('words')
        elif o == '-c':
            print_counts.append('bytes')
        elif o == '-m':
            print_counts.append('chars')
        else:
            assert False, 'unsupported option'
    filenames = rest

    if len(rest) == 0:
        input = sys.stdin
        results = analyze_input_stream(input)
        for key, value in results.items():
            if key in print_counts:
                print(str(value).rjust(6, ' '), end=' ')
        print('\n', end='')
        sys.exit(0)

    total = OrderedDict()
    total['lines'] = 0
    total['words'] = 0
    total['bytes'] = 0
    total['chars'] = 0

    for filename in filenames:
        with open(filename, 'r', newline='\n') as input:
            results = analyze_input_stream(input)
            for key, value in results.items():
                total[key] += value
                if key in print_counts:
                    print(str(value).rjust(6, ' '), end=' ')
            print(filename)
    if len(filenames) > 1:
        for key, value in total.items():
            if key in print_counts:
                print(str(value).rjust(6, ' '), end=' ')
        print('total')

    sys.exit(0)


def analyze_input_stream(stream):
    results = OrderedDict()
    results['lines'] = 0
    results['words'] = 0
    results['bytes'] = 0
    results['chars'] = 0
    wordlen = 0
    while True:
        c = stream.read(1)
        if not c:
            break
        if c == '\n':
            results['lines'] += 1
        if c.isspace():
            if wordlen > 0:
                results['words'] += 1
            wordlen = 0
        else:
            wordlen += 1
        results['bytes'] += len(c.encode('utf-8'))
        results['chars'] += 1
    return results


if __name__ == "__main__":
    main()
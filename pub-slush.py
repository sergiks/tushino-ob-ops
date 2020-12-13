#!/bin/python
# -*- coding: utf-8 -*-

files = {
  '494/20': 'ZaklucheniePZZ-02397-2020-EOO02-11-202018_13(0).txt',
  '526/20': 'ZaklucheniePPT-003085-EOO05-11-202014_16(0)(1).txt', 
  '527/20': 'ZaklucheniePPT-003082-EOO05-11-202009_32(0).txt',    
  '528/20': 'ZaklucheniePZZ-02395-2020-EOO02-11-202018_33(0).txt',
}


def analyze_file(id, filename):
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    expect = 1
    cursor = 0
    result = {
        "yes-ok" : 0,
        "yes-but": 0,
        "not"    : 0,
        "not-ids": [],
    }

    def get_line(n):
        if len(lines) <= n:
            return ''
        return lines[n].strip()

    def log(cursor, text):
        print("{}: {}".format(cursor, text)) 


    while True: 
        cursor += 1
        if cursor >= len(lines):
            break

        # wait for response number alone on the line
        text = get_line(cursor)
        if text == str(expect):
            expect = expect + 1
            cursor += 2

            text = get_line(cursor)

            if text == "Поддерживаю":
                text = get_line(cursor + 2)
                if text == "Рекомендовано":
                    result['yes-ok'] += 1
                    cursor += 2
                else:
                    result['yes-but'] += 1
            else:
                result['not'] += 1
                result['not-ids'].append(expect - 1)
                # print("  №{} строка {}: {}".format(expect-1, text, cursor))

    print("\nОбсуждение {}\nПротив: {}, за: {} + {} с замечаниями".format(id, result['not'], result['yes-ok'], result['yes-but']))
    print("Номера замечаний «против»: {}".format(' '.join(map(str, result['not-ids']))))


# Main run
for id in files:
    analyze_file(id, files[id])


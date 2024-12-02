import common

if __name__ != '__main__':
    raise Exception('This file is not meant to be imported')


def main():
    input = common.read_file("input.txt")
    safe_report_count = 0
    for line in input:
        if is_report_safe(line):
            print("true")
            safe_report_count += 1
            continue
        print('false')
    print(safe_report_count)



def is_report_safe(report: str)-> bool:
    if not len(report):
        return False
    report = sanitize_report(report)

    for i in range(len(report) - 1):
        diff = abs(report[i + 1] - report[i])
        if not 1 <= diff <= 3:
            return False

    sorted_report = sorted(report)

    if report == sorted_report:
        return True
    if report == sorted_report[::-1]:
        return True
    return False

def sanitize_report(report: str)-> list[int]:
    sanitized = report.split(' ')
    return [int(x) for x in sanitized]


main()
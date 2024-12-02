import common

if __name__ != '__main__':
    raise Exception('This file is not meant to be imported')


def main():
    input = common.read_file("input.txt")
    safe_report_count = 0

    reports = sanitize_reports(input)

    unsafe_reports = []
    for line in reports:
        if is_report_safe(line):
            safe_report_count += 1
            continue
        unsafe_reports.append(line)
    print("There is a total of ", safe_report_count, "safe reports without any error")

    for report in unsafe_reports:
        if is_report_safe_with_one_error(report):
            safe_report_count += 1

    print("There is a total of ", safe_report_count, "safe reports with one error")



def is_report_safe(report: list[int])-> bool:

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

def is_report_safe_with_one_error(report: list[int]) -> bool:
    for i in range(len(report)):
        tem_report = report[:i] + report[i+1:]
        if is_report_safe(tem_report):
            return True
    return False


def sanitize_report(report: str)-> list[int]:
    sanitized = report.split(' ')
    return [int(x) for x in sanitized]

def sanitize_reports(input: list[str]) -> list[list[int]]:
    sanitized_reports = []
    for report in input:
        if not len(report):
            continue
        sanitized_reports.append(sanitize_report(report))
    return sanitized_reports

main()
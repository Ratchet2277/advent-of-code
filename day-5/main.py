import re

import common

if __name__ != '__main__':
    raise Exception('This file is not meant to be imported')


class Page:
    page_number: int
    sort_rules: list[tuple[int, int]] = []

    def __init__(self, page_number: int):
        self.page_number = page_number

    def __cmp__(self, other):
        for sort in Page.sort_rules:
            if self.page_number not in sort:
                continue
            if other.page_number not in sort:
                continue

            if self.page_number == sort[0]:
                return -1
            if self.page_number == sort[1]:
                return 1
        return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0


def main():
    data = common.read_file("input.txt")
    page_data = []
    sort_data = []
    for i in range(len(data)):
        if not data[i].strip():
            sort_data = data[:i + 1]
            page_data = data[i:]
            break
    Page.sort_rules = parse_sort_data(sort_data)
    page_data = parse_page_data(page_data)

    ordered_pages = []
    non_ordered_pages = []

    for pages in page_data:
        if check_order_rule(pages):
            ordered_pages.append(pages)
            continue
        non_ordered_pages.append(sorted(pages))

    print("Sum of middle pages of ordered updates", sum([get_middle_value(pages) for pages in ordered_pages]))
    print("Sum of middle pages of unordered updates after sorting",
          sum([get_middle_value(pages) for pages in non_ordered_pages]))


def get_middle_value(pages: list[Page]) -> int:
    middle_index = int((len(pages) - 1) / 2)
    return pages[middle_index].page_number


def check_order_rule(pages: list[Page]) -> bool:
    for i in range(len(pages) - 1):
        for rule in Page.sort_rules:
            if pages[i].page_number != rule[1]:
                continue
            if rule[0] in [page.page_number for page in pages[i:]]:
                return False
    return True


def parse_sort_data(data: list[str]) -> list[tuple[int, int]]:
    output = []
    data = "".join(data)
    regex = re.compile(r"(\d+)\|(\d+)")
    for match in regex.finditer(data):
        output.append((int(match.group(1)), int(match.group(2))))
    return output


def parse_page_data(data: list[str]) -> list[list[Page]]:
    output = []
    regex = re.compile(r"(\d+)")
    for line in data:
        page_order = []
        for match in regex.finditer(line):
            page_order.append(Page(int(match.group(1))))
        if not len(page_order):
            continue
        output.append(page_order)
    return output


main()

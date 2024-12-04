def read_file(path: str) -> list[str]:
    file = open(path)
    output = []
    while True:
        line = file.readline()
        if not line:
            break
        output.append(line)
    return output


def strip_end_of_line(lines: list[str]) -> list[str]:
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '').replace('\r', '')
    return lines

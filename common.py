def read_file(path: str) -> list[str]:
    file = open(path)
    output = []
    while True:
        line = file.readline()
        if not line:
            break
        output.append(line)
    return output
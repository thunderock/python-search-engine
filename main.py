from engine import engine

def read_lines(filepath):
    with open(filepath) as f:
        content = f.readlines()
        return [x.strip() for x in content]


def create_doc_strings(doc_string, doc_count):
    assert doc_string[0] == 'P'
    return ("P" + str(doc_count), doc_string[2:])


def create_query_string(query_string, query_count):
    assert query_string[0] == 'Q'
    return ("Q" + str(query_count), query_string[2:])


if __name__ == "__main__":
    # reads from input.txt
    lines = read_lines('input.txt')
    doc_strings = []
    query_strings = []
    doc_count = 0
    query_count = 0
    for line in lines:
        if line[0] == 'P':
            doc_count += 1
            doc_strings.append(create_doc_strings(line, doc_count))
        elif line[0] == 'Q':
            query_count += 1
            query_strings.append(create_query_string(line, query_count))

    engine = engine.Engine()
    engine.index(doc_strings)
    for query in query_strings:
        # print("query ", query[1])
        print(query[0], engine.search(query[1]))


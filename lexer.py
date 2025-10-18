def atomic_components(statement: str) -> set[str]:
    components = set()

    def __atomic_components(statement: str) -> None:
        parenteses_count = 0
        for char in statement:
            if char == "(":
                parenteses_count += 1
                new_statement = get_parenteses_statements(statement, parenteses_count)
                __atomic_components(new_statement)
        statement += ")" * (statement.count("(") - statement.count(")"))
        if not statement == "":
            components.add(statement)

    __atomic_components(statement)
    components.remove(statement)
    return components


def get_parenteses_statements(statement: str, parenteses_count: int) -> str:
    start = 0
    end = 0
    open_count = parenteses_count
    close_count = parenteses_count
    for i in range(len(statement)):
        if statement[i] == "(":
            if open_count == 1:
                start = i
            open_count -= 1
            continue
        if statement[i] == ")":
            if close_count == 1:
                end = i
            close_count -= 1
        if close_count == 0:
            break
    return statement[start:end]

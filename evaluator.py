from lexer import atomic_components
from operators import biconditional, disjunction, conditional, conjunction


def get_variables_letters(statement: str) -> set[str]:
    letters = set()
    for i in range(ord("A"), ord("Z")):
        if i == ord("V"):
            continue
        if chr(i) in statement:
            letters.add(chr(i))
    return letters


def truth_table_rows(statement: str) -> list[list[str]]:
    variables = get_variables_letters(statement)
    total_variables = len(variables)
    total_rows = 2**total_variables
    variable_row = [variable for variable in sorted(variables)]
    rows = []
    for _ in range(total_rows):
        rows.append([])
    for i in range(1, total_variables + 1):
        parts = 2**i
        part_len = total_rows // parts
        switch = False
        index = 0
        for j in range(parts):
            for _ in range(part_len):
                if switch:
                    rows[index].append("F")
                else:
                    rows[index].append("T")
                index += 1
            switch = not switch
    rows.insert(0, variable_row)
    return rows


def replace_variable_by_value(
    statement: str, config_row: list[str], row: list[str]
) -> str:
    new_statement = statement
    for i in range(len(row)):
        new_statement = new_statement.replace(config_row[i], row[i])
    new_statement = new_statement.replace("~T", "F")
    new_statement = new_statement.replace("~F", "T")
    return new_statement


def evaluate_statement(statement: str) -> list[list[str]]:
    truth_table = truth_table_rows(statement)
    config_row = truth_table[0]
    index = 1
    for row in truth_table[1::]:
        new_statement = replace_variable_by_value(statement, config_row, row)
        result = solve_statement(new_statement)
        if result:
            result = "T"
        else:
            result = "F"
        truth_table[index].append(result)
        index += 1
    truth_table[0].append("Result")
    return truth_table


def solve_statement(statement: str) -> bool:
    atomic_statements = atomic_components(statement)
    for atomic in atomic_statements:
        atomic_result = resolve_statement(atomic)
        if atomic_result:
            atomic_result = "T"
        else:
            atomic_result = "F"
        statement = statement.replace(atomic, atomic_result)
        statement = statement.replace("~F", "T")
        statement = statement.replace("~T", "F")
        statement = statement.replace("~(T)", "F")
        statement = statement.replace("~(F)", "T")
    return resolve_statement(statement)


def resolve_statement(statement: str) -> bool:
    statement = statement.removeprefix("(")
    statement = statement.removesuffix(")")
    symbol = get_symbol(statement)
    a = statement[0]
    b = statement[-1]
    if a == "T":
        a = True
    else:
        a = False
    if b == "T":
        b = True
    else:
        b = False
    if symbol == "<->":
        return biconditional(a, b)
    if symbol == "->":
        return conditional(a, b)
    if symbol == "V":
        return disjunction(a, b)
    if symbol == "*":
        return conjunction(a, b)
    raise "Error"


def get_symbol(statement: str) -> str:
    if "->" in statement:
        return "->"
    if "<->" in statement:
        return "<->"
    if "*" in statement:
        return "*"
    if "V" in statement:
        return "V"
    raise "Error"


def is_equivalent(statement_one: str, statement_two: str) -> bool:
    truth_table_one = evaluate_statement(statement_one)
    truth_table_two = evaluate_statement(statement_two)
    return truth_table_one == truth_table_two


def is_contradictory(statement_one: str, statement_two: str) -> bool:
    truth_table_one = evaluate_statement(statement_one)
    truth_table_two = evaluate_statement(statement_two)
    if truth_table_one[0] != truth_table_two[0] or len(truth_table_one) != len(
        truth_table_two
    ):
        return False
    truth_table_len = len(truth_table_one)
    result_index = len(truth_table_one[0]) - 1
    for i in range(1, truth_table_len):
        if truth_table_one[i][result_index] == truth_table_two[i][result_index]:
            return False
    return True


def is_consistent(statement_one: str, statement_two: str) -> bool:
    truth_table_one = evaluate_statement(statement_one)
    truth_table_two = evaluate_statement(statement_two)
    if is_equivalent(statement_one, statement_two) or is_contradictory(
        statement_one, statement_two
    ):
        return False
    if len(truth_table_one) != len(truth_table_two):
        return False
    truth_table_len = len(truth_table_one)
    result_index = len(truth_table_one[0]) - 1
    for i in range(1, truth_table_len):
        if truth_table_one[i][result_index] == truth_table_two[i][result_index] == "T":
            return True
    return False


def is_inconsistent(statement_one: str, statement_two: str) -> bool:
    truth_table_one = evaluate_statement(statement_one)
    truth_table_two = evaluate_statement(statement_two)
    if is_consistent(statement_one, statement_two):
        return False
    return True


def is_tautology(statement: str) -> bool:
    truth_table = evaluate_statement(statement)
    result_index = len(truth_table[0]) - 1
    for i in range(1, len(truth_table)):
        if truth_table[i][result_index] == "F":
            return False
    return True


def is_contradiction(statement: str) -> bool:
    truth_table = evaluate_statement(statement)
    result_index = len(truth_table[0]) - 1
    for i in range(1, len(truth_table)):
        if truth_table[i][result_index] == "T":
            return False
    return True


def is_contingent(statement: str) -> bool:
    return not is_tautology(statement) and not is_contradiction(statement)

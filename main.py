from evaluator import (
    is_contradictory,
    is_inconsistent,
    is_consistent,
    is_equivalent,
    is_tautology,
    is_contingent,
    is_contradiction,
)


print(is_tautology("A V ~A"))
print(is_contradiction("A * ~A"))
print(is_contingent("A -> B"))
print(is_equivalent("A -> B", "~A V B"))
print(is_contradictory("A -> B", "~A -> ~B"))
print(is_consistent("A -> B", "B -> A"))
print(is_inconsistent("A -> B", "A -> ~B"))

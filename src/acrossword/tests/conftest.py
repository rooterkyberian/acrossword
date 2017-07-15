import difflib

from acrossword import crossword


def pytest_assertrepr_compare(op, left, right):
    if (
            isinstance(left, crossword.Crossword) and
            isinstance(right, crossword.Crossword) and
            op == "=="
    ):
        return [
            'Comparing Crossword instances:',
        ] + [
            line for line in difflib.context_diff(
                crossword.dumps(left).splitlines(True),
                crossword.dumps(right).splitlines(True),
            )
        ]

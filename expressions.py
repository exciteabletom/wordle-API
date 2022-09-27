import itertools
import logging
from random import shuffle
from typing import List, Optional, Tuple, Iterable

from const import EXPRESSION_LENGTH

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

operators = [*"+-*/"]


def generate_expressions() -> List[Tuple[str, int]]:
    allowed_vals = list(range(10)) + operators

    # generate all possible expressions, including invalid ones
    filtered = itertools.product(allowed_vals, repeat=EXPRESSION_LENGTH)  # cartesian product
    filtered = map(lambda x: "".join(str(y) for y in x), filtered)
    filtered = filter_expressions(filtered)
    filtered = map(lambda x: (x, evalute_expression(x)), filtered)
    filtered = filter(lambda x: x[1] is not None, filtered)

    filtered = list(filtered)
    shuffle(filtered)
    logger.info(f"Generated {len(filtered)} expressions")
    return filtered


def filter_expressions(filtered: Iterable) -> Iterable:
    """Filter invalid mathematical expressions"""
    filtered = filter(lambda x: x[0] not in operators, filtered)  # starts with an operator
    filtered = filter(lambda x: x[-1] not in operators, filtered)  # ends with an operator
    filtered = filter(lambda x: "00" not in x, filtered)  # contains 00
    filtered = filter(lambda x: any(o in x for o in operators), filtered)  # doesnt contain an operator

    # contains two consecutive operators
    double_operators = list(map(lambda x: "".join(x), itertools.product(operators, repeat=2)))
    filtered = filter(lambda x: not any(o in x for o in double_operators), filtered)
    return filtered


def is_valid_expression(expression: str) -> bool:
    filtered = list(filter_expressions([expression]))
    if not filtered:
        return False
    return True


def evalute_expression(expression: str) -> Optional[int]:
    """Evaluate the expression and ensure that the equation compiles and evaluates to an int"""
    try:
        answer = eval(expression)
        if not float(answer).is_integer():
            return None
        return int(answer)
    except Exception:
        return None

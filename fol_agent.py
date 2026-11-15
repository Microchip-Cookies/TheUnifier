# The Unifier
# Programmer: Valerie Armstrong
# Portfolio Project for CS 331, Intro to AI
# Professor Nauman Chaudhry
# Oregon State University
# Fall 2026

from typing import Any

def unify(symbols: dict, expr_1: list[Any], expr_2: list[Any], subs: list[Any]) -> bool:
    """Unify expr_1 and expr_2. Add all substitutions to the argument subs. Assumes all inputs valid and
    expr_1 and expr_2 are already standardized apart.

    Args:
      symbols: A dictionary with 4 properties containing the symbols used in expr_1 and expr_2.
      expr_1: The first expression.
      expr_2: The second expression.
      subs: A list, initially empty. If the unification is successful, your code
          must populate subs with the substitutions corresponding to an MGU for
          the 2 expressions.

    Returns:
      True if unification succeeds, False otherwise.
    """
    # No unifier is needed if both expressions are empty
    if expr_1 == [] and expr_2 == []:
        return True
    # If only one of the expressions is empty, they cannot be unified
    if expr_1 == [] or expr_2 == []:
        return False

    term_1 = expr_1[0]
    term_2 = expr_2[0]
    if term_1 == term_2:
        return True
    # If either of the terms is a string, get the unifier
    unifier = []
    if type(term_1) is str or type(term_2) is str:
        unifier += _get_unifier(term_1, term_2, symbols)
    if unifier[0] is None:
        return False

    # Modify subs to incorporate new unifier term
    _substitute(unifier, subs)
    return unify(symbols, expr_1[1:], expr_2[1:], subs)

def _substitute(new_sub: list[str], subs_list: list[Any]) -> None:
    """
    Within the subs_list, replaces the term new_sub[0] with the term new_sub[1] within the subs_list.
    :param new_sub: a list of two strings
                    new_sub[0] is the variable to replace
                    new_sub[1] is the value with which to replace it
    :param subs_list: a list representing the current unifier, may contain layers of nested lists of strings
    :return: None
    """
    for term in subs_list:
        if type(term[1]) is list:
            _substitute(new_sub, [term[1]])
        elif term[1] == new_sub[0]:
            term[1] = new_sub[1]

    for i, term in enumerate(subs_list):
        if term[0] == term[1]:
            del(subs_list[i])

    subs_list.append[new_sub]

def _get_unifier(term_1: str | list[Any], term_2: str | list[Any], symbols: dict) -> list[str] | None:
    """

    :param term_1: a term in a FOL statement
    :param term_2: a term in a FOL statement
    :return: the unifier, if one exists in the form [to_be_replaced, value_to_replace_with]
    """
    type_1 = _symbol_type(term_1, symbols)
    type_2 = _symbol_type(term_2, symbols)
    match type_1, type_2:
        case 'variable', 'variable':
            return [term_1, term_2]
        case 'variable', 'constant':
            return [term_1, term_2]
        case 'constant', 'variable':
            return [term_2, term_1]
        case 'variable', 'function':
            if term_1 in term_2:  # TODO: Replace this with a valid test
                return None
            return [term_1, term_2]
        case 'function', 'variable':
            if term_2 in term_1:  # TODO: Replace this with a valid test
                return None
            return [term_2, term_1]
        # case 'constant', 'function':
        #     return None
        # case 'function', 'constant':
        #     return None

    return None


def _symbol_type(symbol: str, symbols: dict) -> str:
    """
    Symbol types include 'predicates', 'functions', 'variables', and 'constants'. If string, symbol must be
    found as a value in symbols. If list, symbol's first element must be a string found in symbols.
    :param symbol: str, the symbol to type
    :param symbols: dict with symbol types as keys and lists of symbols as values
    :return: str, type name of symbol
    """

    if symbol in symbols['variables']:
        return 'variable'
    if symbol in symbols['constants']:
        return 'constant'
    if type(symbol) is not list:
        raise ValueError('Term not found in symbols')
    # symbol is in the form of a list, use first term in list to determine if it is a predicate or function
    if symbol[0] in symbols['functions']:
        return 'function'
    if symbol[0] in symbols['predicates']:
        return 'predicate'

    raise ValueError('Term not found in symbols')

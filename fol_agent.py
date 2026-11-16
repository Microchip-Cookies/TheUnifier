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
        return unify(symbols, expr_1[1:], expr_2[1:], subs)
    # If either of the terms is a string, get the unifier
    unifier = []
    if type(term_1) is str or type(term_2) is str:
        unifier += _get_unifier(term_1, term_2, symbols)
    if unifier[0] is None:
        return False

    # Modify subs and remainder of expressions to incorporate new unifier term
    _compose_subs(unifier, subs)
    tail_1 = expr_1[1:]
    tail_2 = expr_2[1:]
    _substitute(unifier, tail_1)
    _substitute(unifier, tail_2)
    return unify(symbols, tail_1, tail_2, subs)

def _substitute(new_sub:list[str], expr: list[Any]) -> None:
    """
    Seeks the given target value in the expression and replaces it in the expression with the replacement value.
    :param new_sub: list of two strings in the form [target_val, replacement_val]
    :param expr: partial or complete FOL expression as list, which may contain string and nested lists
    :return: None
    """
    for i, element in enumerate(expr):
        if type(element) is list:
            _substitute(new_sub, element)
        elif element == new_sub[0]:
            expr[i] = new_sub[1]


def _compose_subs(new_sub: list[str], subs_list: list[Any]) -> None:
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
            _compose_subs(new_sub, [term[1]])
        elif term[1] == new_sub[0]:
            term[1] = new_sub[1]

    for i, term in enumerate(subs_list):
        if term[0] == term[1]:
            del(subs_list[i])

    if new_sub:
        subs_list.append(new_sub)

def _get_unifier(term_1: str | list[Any], term_2: str | list[Any], symbols: dict) -> list[str] | None:
    """
    Constructs and returns a unifier. Assumes that term_1 and term_2 are not empty, term_1 != term_2, and at least
    one of the terms is a string.
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
            return None if _contains_var(term_1, term_2) else [term_1, term_2]
        case 'function', 'variable':
            return None if _contains_var(term_2, term_1) else [term_2, term_1]
        case 'variable', 'predicate':
            return None if _contains_var(term_1, term_2) else [term_1, term_2]
        case 'predicate', 'variable':
            return None if _contains_var(term_2, term_1) else [term_2, term_1]

    return None

def _contains_var(var: str, term_list: list[Any]) -> bool:
    """

    :param var: a variable name
    :param term_list: a list of FOL terms which may or may not include the variable, may contain nested lists
    :return: True if var in term_list, False otherwise
    """
    for term in term_list:
        if var == term:
            return True
        if type(term) is list:
            if _contains_var(var, term): return True
    return False

def _symbol_type(symbol: str | list[Any], symbols: dict) -> str:
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

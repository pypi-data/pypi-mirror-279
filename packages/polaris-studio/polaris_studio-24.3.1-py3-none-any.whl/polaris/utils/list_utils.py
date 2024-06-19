import types


def first_and_only(a_list: list):
    if isinstance(a_list, (filter, types.GeneratorType)):
        a_list = list(a_list)
    if len(a_list) == 0:
        raise RuntimeError("Expected a single thing, but there was nothing")
    if len(a_list) > 1:
        raise RuntimeError("Expected a single thing, but there were many")
    return a_list[0]


def zero_or_one(a_list: list):
    if isinstance(a_list, (filter, types.GeneratorType)):
        a_list = list(a_list)
    if len(a_list) == 0:
        return None
    if len(a_list) > 1:
        raise RuntimeError("Expected no more than a single thing, but there were many")
    return a_list[0]

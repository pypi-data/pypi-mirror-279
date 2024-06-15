from typing import List, Any, Iterable, Dict


def convert_lines(lines: List[str]) -> str:
    return "\n".join(lines)


def convert_list_to_dicts_list(inputs: Iterable[Any], shared_key: str) -> List[Dict[str, str]]:
    kwargs = [{shared_key: input} for input in inputs]
    return kwargs


def add_prefix(
    text: str,
    prefix: str = " " * 4,
):
    """
    Parameters
    ----------
    text: str,
        Text to convert
    prefix: str = " " * 4
        Prefix to be added to all the lines
    """
    split = text.split("\n")
    text = prefix + f"\n{prefix}".join(split)
    return text


def convert_dict_of_lists_to_list_of_dicts(
    dict_of_lists: Dict[str, List[str]],
) -> List[Dict[str, str]]:
    if not _is_dict_of_lists_valid(dict_of_lists):
        raise ValueError("All lists in dict_of_lists must have the same length")

    count = len(next(iter(dict_of_lists.values())))
    list_of_dicts = [{key: value_list[i] for key, value_list in dict_of_lists.items()} for i in range(count)]
    return list_of_dicts


def convert_list_of_dicts_to_dict_of_lists(
    list_of_dicts: List[Dict[str, str]],
) -> Dict[str, List[str]]:
    if not list_of_dicts:
        return {}

    keys = list_of_dicts[0].keys()
    dict_of_lists = {key: [] for key in keys}

    for d in list_of_dicts:
        for key in keys:
            dict_of_lists[key].append(d[key])

    return dict_of_lists


def cut_end_lines(text: str) -> str:
    split = text.splitlines()[1:-1]
    return convert_lines(split)


def _is_dict_of_lists_valid(
    kwargs_many: Dict[str, List[str]],
) -> bool:
    lengths = iter(len(args) for args in kwargs_many.values())
    first_length = next(lengths, None)
    return all(length == first_length for length in lengths)

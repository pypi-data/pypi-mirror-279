from crimson.templator.utils import generate_combinations_dict_list, generate_combinations_list_tuple


def test_generate_combination_dict_list():
    data = {
        "crimson-data-class": ["0.1.3", "0.1.0"],
        "crimson-templator": ["0.1.4", "0.1.1"],
    }

    all_combination = generate_combinations_dict_list(data, "module_name", "version")

    expected = [
        {"module_name": ["crimson-templator", "crimson-data-class"], "version": ["0.1.4", "0.1.3"]},
        {"module_name": ["crimson-templator", "crimson-data-class"], "version": ["0.1.4", "0.1.0"]},
        {"module_name": ["crimson-templator", "crimson-data-class"], "version": ["0.1.1", "0.1.3"]},
        {"module_name": ["crimson-templator", "crimson-data-class"], "version": ["0.1.1", "0.1.0"]},
    ]

    assert all_combination == expected, f"Expected {expected}, but got {all_combination}"


def test_generate_combinations_list_tuple():
    data = {
        "crimson-data-class": ["0.1.3", "0.1.0"],
        "crimson-templator": ["0.1.4", "0.1.1"],
    }

    all_combination = generate_combinations_list_tuple(data)

    expected = [
        [("crimson-templator", "0.1.4"), ("crimson-data-class", "0.1.3")],
        [("crimson-templator", "0.1.4"), ("crimson-data-class", "0.1.0")],
        [("crimson-templator", "0.1.1"), ("crimson-data-class", "0.1.3")],
        [("crimson-templator", "0.1.1"), ("crimson-data-class", "0.1.0")],
    ]

    assert all_combination == expected, f"Expected {expected}, but got {all_combination}"


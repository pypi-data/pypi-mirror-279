from typing import Dict, List, Tuple, Any


class _GenerateCombinations:

    @classmethod
    def _generate_combinations(
        cls, data, current_combination: List[Any] = [], all_combinations: List[Any] = []
    ) -> List[List[Tuple[str, str]]]:
        if not data:  # 모든 라이브러리에 대한 조합을 생성한 경우
            all_combinations.append(current_combination)
            return

        library_name, versions = data.popitem()  # 현재 라이브러리 정보 가져오기
        for version in versions:
            cls._generate_combinations(
                data=data.copy(),  # data 복사본 전달 (원본 유지)
                current_combination=current_combination + [(library_name, version)],  # 현재 조합에 추가
                all_combinations=all_combinations,
            )

    @classmethod
    def generate_combinations_list_tuple(cls, data: Dict[Any, List[Any]]) -> List[List[Tuple[Any, Any]]]:
        all_combinations = []
        cls._generate_combinations(data=data.copy(), all_combinations=all_combinations)

        return all_combinations

    @classmethod
    def generate_combinations_dict_list(
        cls, data: Dict[Any, List[Any]], key_name: str, value_name: str
    ) -> List[Dict[str, List[Any]]]:
        _all_combinations = cls.generate_combinations_list_tuple(data)

        all_combinations = []
        for one_case in _all_combinations:
            one_cace = cls._convert_list_tuple_to_list_dict(one_case, key_name, value_name)
            all_combinations.append(one_cace)
        return all_combinations

    @classmethod
    def _convert_list_tuple_to_list_dict(
        cls, data: List[Tuple[Any, Any]], key_name: str, value_name: str
    ) -> Dict[str, List[Any]]:
        _data = {
            key_name: [],
            value_name: [],
        }
        for module_name, version in data:
            _data[key_name].append(module_name)
            _data[value_name].append(version)
        return _data

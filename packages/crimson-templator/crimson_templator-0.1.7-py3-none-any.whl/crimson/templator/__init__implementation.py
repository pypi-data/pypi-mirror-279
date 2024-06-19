import re
from typing import List, Dict, Tuple


class _RemoveLines:
    @classmethod
    def _extract_keywords(cls, template: str, open: str, close: str) -> List[str]:
        pattern = rf"{re.escape(open)}(.*?){re.escape(close)}"
        matches = re.findall(pattern, template)
        filtered_matches = [match for match in matches if not match.endswith("\\")]
        return filtered_matches

    @classmethod
    def _extract_keywords_with_brackets(cls, template: str, open: str, close: str) -> List[str]:
        pattern = rf"{re.escape(open)}(.*?){re.escape(close)}"
        matches = re.findall(pattern, template)
        filtered_matches = [open + match + close for match in matches if not match.endswith("\\")]
        return filtered_matches

    @classmethod
    def _extract_line_indexes_including_keyword(
        cls, template: str, open: str, close: str, clean_brackets: bool = True
    ) -> Dict[str, int]:
        keywords_with_brackets = cls._extract_keywords_with_brackets(template, open, close)

        line_indexes = {}

        for keyword_with_bracket in keywords_with_brackets:
            for i, line in enumerate(template.splitlines()):
                if line.find(keyword_with_bracket) != -1:
                    if clean_brackets:
                        keyword_with_bracket = keyword_with_bracket.replace(open, "")
                        keyword_with_bracket = keyword_with_bracket.replace(close, "")
                    line_indexes[keyword_with_bracket] = i

        return line_indexes

    @classmethod
    def _parse_remove_keyword(cls, remove_keyword: str) -> Tuple[str, int]:
        remove_direction, num_to_remove = remove_keyword.split(":")
        return remove_direction, int(num_to_remove)

    @classmethod
    def _extract_line_indexes_to_remove(cls, template, open: str = r"\(", close: str = r"\)"):
        line_indexes: Dict[str, int] = cls._extract_line_indexes_including_keyword(template, open, close)

        line_indexes_to_remove = []

        for remove_keyword, line_index in line_indexes.items():
            remove_direction, num_to_remove = cls._parse_remove_keyword(remove_keyword)

            if remove_direction == "remove_below":
                start = line_index
                end = line_index + num_to_remove + 1
            elif remove_direction == "remove_above":
                end = line_index + 1
                start = line_index - num_to_remove

            line_indexes_to_remove = line_indexes_to_remove + list(range(start, end))

        return line_indexes_to_remove

    @classmethod
    def remove_lines(cls, template: str, open: str = r"\(", close: str = r"\)"):
        template += "empty_guard"

        line_indexes_to_remove = cls._extract_line_indexes_to_remove(template, open, close)
        lines = []
        for i, line in enumerate(template.splitlines()):
            if i not in line_indexes_to_remove:
                lines.append(line)

        template = "\n".join(lines)
        # remove empty_guard
        template = template[:-11]

        return template

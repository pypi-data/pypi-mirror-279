# altercase

import sys
from dataclasses import dataclass, field
from enum import IntEnum, auto
from functools import lru_cache
from typing import Iterable, List, Optional, Protocol, runtime_checkable


class CharCaseEnum(IntEnum):
    INVALID = auto()
    LOWER = auto()
    UPPER = auto()
    DIGIT = auto()

    def __repr__(self):
        match self:
            case CharCaseEnum.INVALID:
                return "-"
            case CharCaseEnum.LOWER:
                return "L"
            case CharCaseEnum.UPPER:
                return "U"
            case CharCaseEnum.DIGIT:
                return "D"
        raise NotImplementedError()


class Char:
    def __init__(self, c: str, case: CharCaseEnum = CharCaseEnum.INVALID) -> None:
        assert len(c) == 1
        self.c = c
        self.case = case

    def __repr__(self) -> str:
        return self.c

    def __str__(self) -> str:
        return self.c

    def inside(self, it: Iterable[str]) -> bool:
        return self.c in it

    def isdigit(self) -> bool:
        return self.case == CharCaseEnum.DIGIT

    def islower(self) -> bool:
        return self.case == CharCaseEnum.LOWER

    def isupper(self) -> bool:
        return self.case == CharCaseEnum.UPPER


@lru_cache(maxsize=256)
def get_char(c: str) -> Char:
    assert len(c) == 1
    is_char_alpha = c.isalpha()
    is_char_lower = is_char_alpha and c.islower()
    is_char_upper = is_char_alpha and c.isupper()
    is_char_digit = c.isdigit()
    if is_char_lower:
        case = CharCaseEnum.LOWER
    elif is_char_upper:
        case = CharCaseEnum.UPPER
    elif is_char_digit:
        case = CharCaseEnum.DIGIT
    else:
        case = CharCaseEnum.INVALID
    return Char(c=c, case=case)


@dataclass
class Word:
    case: CharCaseEnum = CharCaseEnum.INVALID
    chars: List[Char] = field(default_factory=lambda: [])
    separated: bool = False

    def __len__(self) -> int:
        return len(self.chars)

    def __repr__(self) -> str:
        return "{chars} ({case})".format(
            case=repr(self.case),
            chars="".join(char.c for char in self.chars) if self.chars else "-",
        )

    def __str__(self) -> str:
        return "".join(char.c for char in self.chars)

    def append(self, char: Char) -> None:
        if self.case != char.case:
            raise ValueError("{expected} != {actual}", self.case, char.case)
        self.chars.append(char)

    def init(self, char: Char) -> None:
        self.case = char.case
        self.chars.append(char)

    def isdigit(self) -> bool:
        return self.case == CharCaseEnum.DIGIT

    def islower(self) -> bool:
        return self.case == CharCaseEnum.LOWER

    def isupper(self) -> bool:
        return self.case == CharCaseEnum.UPPER


def is_empty_string(s: Optional[str]) -> bool:
    return s is None or s == "" or s.isspace()


@runtime_checkable
class StringSplitter(Protocol):
    def __call__(self, s: Optional[str], /) -> List[str]: ...


class DefaultStringSplitter:
    def __call__(self, s: Optional[str], /) -> List[str]:
        if is_empty_string(s):
            return [""]

        # 1st Pass
        temp: List[Word] = [Word()]
        for c in s:
            char = get_char(c)
            curr_buff = temp[-1]
            if len(curr_buff) == 0:
                if char.case != CharCaseEnum.INVALID:
                    curr_buff.init(char)
            else:
                if curr_buff.case == char.case:
                    curr_buff.append(char)
                else:
                    temp.append(Word())
                    next_buff = temp[-1]
                    if char.case == CharCaseEnum.INVALID:
                        next_buff.separated = True
                    else:
                        next_buff.init(char)

        # 2nd Pass
        words: List[Word] = []
        for curr_word in temp:
            if len(curr_word) == 0:
                continue
            prev_word: Optional[Word] = (
                words[-1] if not curr_word.separated and len(words) > 0 else None
            )
            if prev_word is not None:
                prev_word_len = len(prev_word)
                curr_word_len = len(curr_word)
                assert prev_word_len > 0
                # "V2" -> ["V2"]
                if (
                    prev_word_len == 1
                    and prev_word.chars[0].inside("vV")
                    and curr_word.isdigit()
                ):
                    curr_word.chars.insert(0, prev_word.chars[0])
                    words.pop(-1)
                # "WiFi" -> ["Wi", "Fi"]
                elif (
                    prev_word_len == 1
                    and prev_word.isupper()
                    and curr_word_len == 1
                    and curr_word.islower()
                ):
                    curr_word.chars = [prev_word.chars[0], curr_word.chars[0]]
                    words.pop(-1)
                # "Foo" -> ["Foo"]
                # "JWTToken" -> ["JWT", "Token"]
                # "XYZabc" -> ["XY", "Zabc"]
                # "XYZ abc" -> ["XYZ", "abc"]
                elif prev_word.isupper() and curr_word_len > 1 and curr_word.islower():
                    last_char = prev_word.chars.pop(-1)
                    curr_word.chars.insert(0, last_char)
                    if len(prev_word.chars) == 0:
                        words.pop(-1)
            words.append(curr_word)
        return [str(word) for word in words]


assert isinstance(
    DefaultStringSplitter, StringSplitter
), "DefaultStringSplitter is not of StringSplitter type."

split_string: StringSplitter = DefaultStringSplitter()


def camel_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    words = []
    for i, word in enumerate(splitter(s)):
        if i == 0:
            words.append(word.lower())
        else:
            words.append(word if word.isupper() else word.capitalize())
    return "".join(words)


def kebab_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    return "-".join(splitter(s)).lower()


def pascal_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    return "".join(
        word if word.isupper() else word.capitalize() for word in splitter(s)
    )


def hazard_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    return "_".join(splitter(s)).upper()


def sentence_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    words = []
    for i, word in enumerate(splitter(s)):
        if i == 0:
            words.append(word if word.isupper() else word.capitalize())
        else:
            words.append(word if word.isupper() else word.lower())
    return " ".join(words)


def snake_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    return "_".join(splitter(s)).lower()


def title_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    return " ".join(
        word if word.isupper() else word.capitalize() for word in splitter(s)
    )


def train_case(s: Optional[str], splitter: Optional[StringSplitter] = None) -> str:
    if is_empty_string(s):
        return ""
    splitter = splitter if splitter is not None else split_string
    return "-".join(splitter(s)).upper()


# noinspection PyShadowingBuiltins
def run() -> None:
    case_map = {
        "camel": camel_case,
        "pascal": pascal_case,
        "snake": snake_case,
        "hazard": hazard_case,
        "kebab": kebab_case,
        "train": train_case,
        "title": title_case,
        "sentence": sentence_case,
    }

    help_text = f"""Usage: altercase [OPTIONS] CASE INPUT

  Convert strings into different cases. (version: {__version__})

Options:
  -h/--help   Show this message and exit.

Arguments:
  CASE        Accepts one of {tuple(case_map.keys())}.
  INPUT       String(s) to convert."""

    argv_len = len(sys.argv)
    if argv_len == 1 or "-h" in sys.argv or "--help" in sys.argv:
        print(help_text)
        exit(0)

    if argv_len < 2:
        exit("missing 'CASE' argument")
    case = sys.argv[1].lower()
    if case not in case_map:
        exit("invalid value for 'case' argument")

    inputs = []
    if argv_len > 2:
        inputs.extend(arg.strip() for arg in sys.argv[2:])
    else:
        inputs.extend(arg.strip() for arg in sys.stdin)
    if len(inputs) == 0:
        exit("missing 'INPUT' argument")

    for input in inputs:
        print(case_map[case](input))


__name__ = "altercase"
__version__ = "0.1.0"
__all__ = [
    "__name__",
    "__version__",
    "split_string",
    "camel_case",
    "hazard_case",
    "kebab_case",
    "pascal_case",
    "snake_case",
    "title_case",
    "train_case",
    "run",
]

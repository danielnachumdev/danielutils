"""file with math symbols constants"""
import platform
from typing import Union, Dict as t_dict
if platform.python_version() >= "3.9":
    from builtins import dict as t_dict
# https://unicode-table.com/en/sets/mathematical-signs/
SPECIAL_DOUBLE_N = "ℕ"
SPECIAL_DOUBLE_Q = "ℚ"
SPECIAL_DOUBLE_R = "ℝ"
SPECIAL_DOUBLE_Z = "ℤ"
SPECIAL_DOUBLE_C = "ℂ"
SPECIAL_RPAB = "〉"  # right pointing angle bracket
SPECIAL_LPAB = "〈"  # left pointing angle bracket
SPECIAL_FORALL = "∀"
SPECIAL_EXISTS = "∃"
SPEICAL_VL = "|"
SPECIAL_SIGMA = "∑"
SPECIAL_PI = "∏"
SPECIAL_CIRCLED_PLUS = "⊕"
SPECIAL_NE = "≠"
SPECIAL_EQUIV = "≡"
SPECIAL_LAMBDA = "λ"
SPECIAL_SQRT = "√"
SPECIAL_CUBE_ROOT = "∛"
SPECIAL_4TH_ROOT = "∜"


SUPERSCRIPT_SMALL_LETTERS = ['ᵃ', 'ᵇ', 'ᶜ', 'ᵈ', 'ᵉ', 'ᶠ', 'ᵍ', 'ʰ', 'ⁱ', 'ʲ', 'ᵏ', 'ˡ', 'ᵐ', 'ⁿ',
                             'ᵒ', 'ᵖ', '𐞥', 'ʳ', 'ˢ', 'ᵗ', 'ᵘ', 'ᵛ', 'ʷ', 'ˣ', 'ʸ', 'ᶻ']

# superscript_big_case_a = 'ⁱ'
# superscript_big_case_b = 'ⁱ'
# superscript_big_case_c = 'ⁱ'
# superscript_big_case_d = 'ⁱ'
# superscript_big_case_e = 'ⁱ'
# superscript_big_case_f = 'ⁱ'
# superscript_big_case_g = 'ⁱ'
# superscript_big_case_h = 'ⁱ'
# superscript_big_case_i = 'ⁱ'
# superscript_big_case_j = 'ⁱ'
# superscript_big_case_k = 'ⁱ'
# superscript_big_case_l = 'ⁱ'
# superscript_big_case_m = 'ⁱ'
# superscript_big_case_n = 'ⁱ'
# superscript_big_case_o = 'ⁱ'
# superscript_big_case_p = 'ⁱ'
# superscript_big_case_q = 'ⁱ'
# superscript_big_case_r = 'ⁱ'
# superscript_big_case_s = 'ⁱ'
# superscript_big_case_t = 'ⁱ'
# superscript_big_case_u = 'ⁱ'
# superscript_big_case_v = 'ⁱ'
# superscript_big_case_w = 'ⁱ'
# superscript_big_case_x = 'ⁱ'
# superscript_big_case_y = 'ⁱ'
# superscript_big_case_z = 'ⁱ'


superscript_dict: t_dict[Union[str, int], str] = {}
superscript_dict.update(
    {chr(i+ord('a')): SUPERSCRIPT_SMALL_LETTERS[i] for i in range(26)}
)
superscript_digits = ["⁰", "¹", "²", "³",
                      "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
superscript_dict.update(
    {i: superscript_digits[i] for i in range(len(superscript_digits))}
)
superscript_dict.update({
    "+": "⁺",
    "-": "⁻",
    "=": "⁼",
    "(": "⁽",
    ")": "⁾",
})

SUBSCRIPT_SMALL_LETTERS = ['ₐ', '', '', '', 'ₑ', '', '', 'ₕ', 'ᵢ', 'ⱼ', 'ₖ', 'ₗ', 'ₘ',
                           'ₙ', 'ₒ', 'ₚ', '', 'ᵣ', 'ₛ', 'ₜ', 'ᵤ', 'ᵥ', '', 'ₓ', '', '']
# subscript_big_case_a = 'ⁱ'
# subscript_big_case_b = 'ⁱ'
# subscript_big_case_c = 'ⁱ'
# subscript_big_case_d = 'ⁱ'
# subscript_big_case_e = 'ⁱ'
# subscript_big_case_f = 'ⁱ'
# subscript_big_case_g = 'ⁱ'
# subscript_big_case_h = 'ⁱ'
# subscript_big_case_i = 'ⁱ'
# subscript_big_case_j = 'ⁱ'
# subscript_big_case_k = 'ⁱ'
# subscript_big_case_l = 'ⁱ'
# subscript_big_case_m = 'ⁱ'
# subscript_big_case_n = 'ⁱ'
# subscript_big_case_o = 'ⁱ'
# subscript_big_case_p = 'ⁱ'
# subscript_big_case_q = 'ⁱ'
# subscript_big_case_r = 'ⁱ'
# subscript_big_case_s = 'ⁱ'
# subscript_big_case_t = 'ⁱ'
# subscript_big_case_u = 'ⁱ'
# subscript_big_case_v = 'ⁱ'
# subscript_big_case_w = 'ⁱ'
# subscript_big_case_x = 'ⁱ'
# subscript_big_case_y = 'ⁱ'
# subscript_big_case_z = 'ⁱ'
subscript_dict: t_dict[Union[str, int], str] = {}
subscript_dict.update(
    {chr(i+ord('a')): SUBSCRIPT_SMALL_LETTERS[i]
     for i in range(len(SUBSCRIPT_SMALL_LETTERS))}
)

subscript_digits = ["\u2080", "\u2081", "\u2082", "\u2083",
                    "\u2084", "\u2085", "\u2086", "\u2087", "\u2088", "\u2089"]
subscript_dict.update(
    {f'{i}': subscript_digits[i] for i in range(len(subscript_digits))}
)
subscript_dict.update({
    "+": "\u208A",
    "-": "\u208B",
    "=": "\u208C",
    "(": "\u208D",
    ")": "\u208E",
})
__all__ = [
    "subscript_dict",
    "subscript_dict",
]

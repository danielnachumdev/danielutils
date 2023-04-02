# https://unicode-table.com/en/sets/mathematical-signs/
special_double_n = "ℕ"
special_double_q = "ℚ"
special_double_r = "ℝ"
special_double_z = "ℤ"
special_double_c = "ℂ"
special_rpab = "〉"  # right pointing angle bracket
special_lpab = "〈"  # left pointing angle bracket
special_forall = "∀"
special_exists = "∃"
special_vl = "|"
special_sigma = "∑"
special_pi = "∏"
special_circled_plus = "⊕"
special_ne = "≠"
special_equiv = "≡"
special_lambda = "λ"
special_square_root = "√"
special_cube_root = "∛"
special_forth_root = "∜"


superscript_small_case_a = 'ᵃ'
superscript_small_case_b = 'ᵇ'
superscript_small_case_c = 'ᶜ'
superscript_small_case_d = 'ᵈ'
superscript_small_case_e = 'ᵉ'
superscript_small_case_f = 'ᶠ'
superscript_small_case_g = 'ᵍ'
superscript_small_case_h = 'ʰ'
superscript_small_case_i = 'ⁱ'
superscript_small_case_j = 'ʲ'
superscript_small_case_k = 'ᵏ'
superscript_small_case_l = 'ˡ'
superscript_small_case_m = 'ᵐ'
superscript_small_case_n = 'ⁿ'
superscript_small_case_o = 'ᵒ'
superscript_small_case_p = 'ᵖ'
superscript_small_case_q = '𐞥'
superscript_small_case_r = 'ʳ'
superscript_small_case_s = 'ˢ'
superscript_small_case_t = 'ᵗ'
superscript_small_case_u = 'ᵘ'
superscript_small_case_v = 'ᵛ'
superscript_small_case_w = 'ʷ'
superscript_small_case_x = 'ˣ'
superscript_small_case_y = 'ʸ'
superscript_small_case_z = 'ᶻ'

superscript_small_letters = [
    superscript_small_case_a, superscript_small_case_b, superscript_small_case_c,
    superscript_small_case_d, superscript_small_case_e, superscript_small_case_f,
    superscript_small_case_g, superscript_small_case_h, superscript_small_case_i,
    superscript_small_case_j, superscript_small_case_k, superscript_small_case_l,
    superscript_small_case_m, superscript_small_case_n, superscript_small_case_o,
    superscript_small_case_p, superscript_small_case_q, superscript_small_case_r,
    superscript_small_case_s, superscript_small_case_t, superscript_small_case_u,
    superscript_small_case_v, superscript_small_case_w, superscript_small_case_x,
    superscript_small_case_y, superscript_small_case_z
]

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


superscript_dict = dict()
superscript_dict.update(
    {chr(i+ord('a')): superscript_small_letters[i] for i in range(26)}
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

subscript_small_case_a = 'ₐ'
subscript_small_case_b = 'ᵇ'
subscript_small_case_c = ''
subscript_small_case_d = 'ᵈ'
subscript_small_case_e = 'ₑ'
subscript_small_case_f = ''
subscript_small_case_g = 'ᶢ'
subscript_small_case_h = 'ₕ'
subscript_small_case_i = 'ᵢ'
subscript_small_case_j = 'ⱼ'
subscript_small_case_k = 'ₖ'
subscript_small_case_l = 'ₗ'
subscript_small_case_m = 'ₘ'
subscript_small_case_n = 'ₙ'
subscript_small_case_o = 'ₒ'
subscript_small_case_p = 'ₚ'
subscript_small_case_q = ''
subscript_small_case_r = 'ᵣ'
subscript_small_case_s = 'ₛ'
subscript_small_case_t = 'ₜ'
subscript_small_case_u = 'ᵤ'
subscript_small_case_v = 'ᵥ'
subscript_small_case_w = ''
subscript_small_case_x = 'ₓ'
subscript_small_case_y = ''
subscript_small_case_z = ''
subscript_small_letters = [subscript_small_case_a, subscript_small_case_b, subscript_small_case_c, subscript_small_case_d, subscript_small_case_e, subscript_small_case_f, subscript_small_case_g, subscript_small_case_h, subscript_small_case_i, subscript_small_case_j, subscript_small_case_k, subscript_small_case_l,
                           subscript_small_case_m, subscript_small_case_n, subscript_small_case_o, subscript_small_case_p, subscript_small_case_q, subscript_small_case_r, subscript_small_case_s, subscript_small_case_t, subscript_small_case_u, subscript_small_case_v, subscript_small_case_w, subscript_small_case_x, subscript_small_case_y, subscript_small_case_z]
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
subscript_dict = dict()
subscript_dict.update(
    {chr(i+ord('a')): subscript_small_letters[i]
     for i in range(len(subscript_small_letters))}
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

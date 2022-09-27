from ..danielutils.Text import *
from ..danielutils.Testing import *


def test_is_matching():
    results = [
        noerr(is_matching, "", "", expected=True),
        noerr(is_matching, "", "*", expected=True),
        noerr(is_matching, "123456789", "123456789", expected=True),
        noerr(is_matching, "123456789", "*", expected=True),
        noerr(is_matching, "123456789", "123*9", expected=True),
        noerr(is_matching, "123456789", "*456*", expected=True),
        noerr(is_matching, "123456789", "*23*8*", expected=True),
        noerr(is_matching, "123456789", "12345678", expected=False),
        noerr(is_matching, "123456789", "12346789", expected=False),
        noerr(is_matching, "", "", expected=True),
        noerr(is_matching, "", "", expected=True),
        noerr(is_matching, "", "", expected=True),
    ]
    assert all(results), results

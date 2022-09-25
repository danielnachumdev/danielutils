def noerr(call_able, *args, expected=None, ** kwargs, ) -> bool:
    if not callable(call_able):
        raise TypeError("all_able must return True for callable(call_able)")
    try:
        res = call_able(*args, **kwargs)
    except:
        return False
    if expected is None:
        return True
    return res == expected


def err(call_able, *args, expected=None, ** kwargs) -> bool:
    if not callable(call_able):
        raise TypeError("all_able must return True for callable(call_able)")
    try:
        res = call_able(*args, **kwargs)
    except:
        if expected is None:
            return True
        return res == expected
    return False


def test(functor, inputs, outputs) -> None:
    if not callable(functor):
        raise TypeError("functor must return true for callable(functor)")

    if len(inputs) != len(outputs):
        raise ValueError("Amount of inputs and outputs is diffrent")

    for input, output in zip(inputs, outputs):
        res = functor(*input[0], **input[1])

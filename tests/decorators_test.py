from ..danielutils.Decorators import *
from ..danielutils.Testing import *
from ..danielutils.Time import measure


def test_NotImplemented():
    @NotImplemented
    def f():
        pass
    results = [
        err(f),
        err(f,),
        err(f, 1),
        err(f, 1.6),
        err(f, ""),
        err(f, a=2),
        err(f, "asd", b=46),
    ]
    assert all(results), results


def test_PartallyImplemented():
    @PartallyImplemented
    def f(a):
        pass
    results = [
        err(f),
        err(f,),
        noerr(f, 1),
        noerr(f, 1.6),
        noerr(f, ""),
        noerr(f, a=2),
        err(f, "asd", b=46),
        err(f,  b=46),
    ]
    assert all(results), results


def test_memo():
    def fib(n) -> int:
        if n in [0, 1]:
            return 1
        return fib(n-2)+fib(n-1)

    @memo
    def fib2(n) -> int:
        if n in [0, 1]:
            return 1
        return fib2(n-2)+fib2(n-1)

    results = [measure(fib2, i) <= measure(fib, i) for i in range(5, 30)]
    assert all(results), results


def test_validate():
    count = 0

    def m():
        return f"test {count}"

    # two functions with the same name, should fail regardless of types
    has_failed = False
    try:
        @validate(int)
        def a():
            pass

        @validate(str)
        def a():
            pass
    except:
        has_failed = True
    assert has_failed, m()

    # use case 1
    count += 1

    @validate(int)
    def f1(v):
        pass

    results = [
        noerr(f1, 1),
        err(f1, 5.2),
        err(f1, 5.2, 3),
        err(f1, str, 3),
        err(f1),
    ]
    assert results, m()

    count += 1

    @validate(str)
    def f2(v):
        pass

    results = [
        noerr(f2, ""),
        noerr(f2, "asdasd"),
        err(f2, 1),
        err(f2, 5.2),
        err(f2, 5.2, 3),
        err(f2, str, 3),
        err(f2),
    ]
    count += 1
    # use case 2
    del f2

    @validate([])
    def f3():
        pass

    # results[
    #     has_failed1,
    # ]
    assert results, m()


def test_overload():
    # regular use
    @overload(int)
    def a(a):
        return 1

    @overload(float)
    def a(a):
        return 2
    # multiple types use

    @overload([int, float])
    def b(a):
        return 3

    @overload(str)
    def b(a):
        return 4

    @overload((bool))
    def b(a):
        return 5
    # use skip

    @overload(None, (int, float), None)
    def c(_, a, __):
        return 6

    @overload(None, [str], None)
    def c(_, a, __):
        return 7

    @overload(int)
    def return_two(v):
        return v, v

    @overload(str)
    def return_two(v):
        return v, v
    results = [
        noerr(a, 1, expected=1),
        noerr(a, -5, expected=1),
        noerr(a, 1.2, expected=2),
        noerr(a, 0.0, expected=2),
        err(a,),
        err(a),
        err(a, ""),
        noerr(b, 5, expected=3),
        noerr(b, 5.0, expected=3),
        noerr(b, "5.0", expected=4),
        noerr(b, True, expected=5),
        noerr(c, 1, 5.0, 1, expected=6),
        noerr(c, 2.3, 5.0, None, expected=6),
        noerr(c, "1", 5.0, "1", expected=6),
        noerr(c, 1, "5.0", 1, expected=7),
        noerr(return_two, 1, expected=(1, 1)),
        noerr(return_two, "1", expected=("1", "1")),
    ]
    assert all(results), results


def test_abstractmethod():
    @abstractmethod
    def a():
        pass

    @purevirtual
    def b():
        pass

    results = [
        err(a),
        err(a, ""),
        err(a, x=0),
        err(b),
        err(b, ""),
        err(b, x=0),
    ]
    assert all(results), results


def test_deprecate():
    @deprecate
    def foo(x):
        return x

    results = [
        noerr(foo, 10, expected=10)
    ]
    assert all(results), results
